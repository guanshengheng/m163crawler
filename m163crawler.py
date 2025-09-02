import os
import re
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

class musicu:
    def __init__(self, config_file="config.json"):
        # 读取配置（UA 与 Cookie）
        self.config = self._load_config(config_file)
        # 指定爬取的歌单地址
        self.URL = "https://music.163.com/#/playlist?id=10174055666"

        # 歌词保存目录
        self.lyrics_dir = "lyrics"
        os.makedirs(self.lyrics_dir, exist_ok=True)

        # 封面保存目录
        self.cover_dir = "images"
        os.makedirs(self.cover_dir, exist_ok=True)

        # 设置浏览器参数（模拟正常用户环境）
        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument(f"user-agent={self.config['User-Agent']}")
        options.add_argument("--disable-gpu")

        # 启动 Chrome 浏览器
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

        # 注入 Cookie 并刷新页面，确保登录态生效
        self.driver.get("https://music.163.com/")
        self._add_cookies(self.config["Cookie"])
        self.driver.refresh()
        self.driver.get(self.URL)

    def _load_config(self, config_file):
        # 从配置文件中读取 UA 与 Cookie
        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def _add_cookies(self, cookie_str):
        # 将 Cookie 字符串转为字典并逐条注入浏览器
        cookies = cookie_str.split("; ")
        for c in cookies:
            if "=" in c:
                k, v = c.split("=", 1)
                self.driver.add_cookie({"name": k, "value": v})

    def _clean_soil(self, element):
        # 移除网页中多余的“soil”干扰节点（避免影响提取）
        self.driver.execute_script("""
            let elems = arguments[0].querySelectorAll("div.soil");
            elems.forEach(e => e.remove());
        """, element)

    def download_lyrics(self, music_id):
        # 通过网易云 API 请求获取歌词
        lrc_url = f'http://music.163.com/api/song/lyric?id={music_id}&lv=1&kv=1&tv=-1'
        try:
            r = requests.get(lrc_url, timeout=10)
            j = r.json()
            if 'lrc' in j and 'lyric' in j['lrc']:
                # 去掉时间戳等标记，保留纯歌词
                lrc = j['lrc']['lyric']
                lrc = re.sub(r'\[.*?\]', '', lrc).strip()
                return lrc
        except Exception:
            pass
        return ""

    def save_lyrics_to_file(self, song_title, lyrics):
        # 将歌词保存为 txt 文件，如果存在则不重复写入
        safe_title = re.sub(r'[\\/*?:"<>|]', "_", song_title)
        filepath = os.path.join(self.lyrics_dir, f"{safe_title}.txt")
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(lyrics)
        return filepath

    def download_cover(self, cover_url, song_title):
        # 下载歌曲封面图片并保存本地
        if not cover_url:
            return ""
        safe_title = re.sub(r'[\\/*?:"<>|]', "_", song_title)
        filepath = os.path.join(self.cover_dir, f"{safe_title}.jpg")
        if not os.path.exists(filepath):
            try:
                r = requests.get(cover_url, timeout=10)
                with open(filepath, "wb") as f:
                    f.write(r.content)
            except Exception:
                return ""
        return filepath

    def _get_songs(self):
        # 抓取歌单页面中的所有歌曲信息
        songs_data = []
        try:
            rows = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located(
                    (By.XPATH, '//table[contains(@class, "m-table")]/tbody/tr')
                )
            )
        except TimeoutException:
            print("未找到任何歌曲行")
            return songs_data

        # 遍历每一首歌曲行
        for row in rows:
            try:
                # 歌曲名与链接
                song_links = row.find_elements(
                    By.XPATH, './/td[2]//a[contains(@href, "/song?id=")]'
                )
                if not song_links:
                    continue

                song_a = song_links[0]
                song_url = song_a.get_attribute("href")
                self._clean_soil(song_a)
                song_title = song_a.get_attribute("title") or song_a.text.strip()

                music_id = song_url.split("id=")[-1]

                # 歌词保存路径（避免重复下载）
                safe_title = re.sub(r'[\\/*?:"<>|]', "_", song_title)
                lyrics_path_full = os.path.join(self.lyrics_dir, f"{safe_title}.txt")
                if os.path.exists(lyrics_path_full):
                    lyrics_path = lyrics_path_full
                else:
                    lyrics = self.download_lyrics(music_id)
                    lyrics_path = ""
                    if lyrics:
                        lyrics_path = self.save_lyrics_to_file(song_title, lyrics)

                # 歌曲时长
                duration = row.find_element(By.XPATH, ".//td[3]").text.strip()

                # 歌手信息
                artist_a = row.find_element(
                    By.XPATH, './/td[4]//a[contains(@href, "/artist?id=")]'
                )
                self._clean_soil(artist_a)
                artist_name = artist_a.get_attribute("title") or artist_a.text.strip()
                artist_url = artist_a.get_attribute("href")

                # 专辑信息
                album_a = row.find_element(
                    By.XPATH, './/td[5]//a[contains(@href, "/album?id=")]'
                )
                self._clean_soil(album_a)
                album_name = album_a.get_attribute("title") or album_a.text.strip()
                album_url = album_a.get_attribute("href")

                # 获取封面 URL 并下载保存
                cover_url = ""
                cover_path = ""
                try:
                    song_page_resp = requests.get(song_url, headers={"User-Agent": self.config["User-Agent"]})
                    soup = BeautifulSoup(song_page_resp.text, "html.parser")
                    ld_json = soup.find("script", type="application/ld+json")
                    if ld_json:
                        data = json.loads(ld_json.string)
                        if "images" in data and isinstance(data["images"], list):
                            cover_url = data["images"][0]
                            cover_path = self.download_cover(cover_url, song_title)
                except Exception:
                    cover_path = ""

                # 整合单首歌曲信息
                songs_data.append({
                    "song_url": song_url,
                    "song_title": song_title,
                    "duration": duration,
                    "artist_name": artist_name,
                    "artist_url": artist_url,
                    "album_name": album_name,
                    "album_url": album_url,
                    "lyrics_path": lyrics_path,
                    "cover_path": cover_path
                })
            except Exception:
                continue

        return songs_data

    def save_to_json(self, data, filename="songs.json"):
        # 将所有歌曲信息保存为 JSON 文件
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def run(self):
        # 主执行流程
        try:
            # 进入 iframe（网易云歌单内容在 g_iframe 中）
            iframe = WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.ID, "g_iframe"))
            )
            self.driver.switch_to.frame(iframe)

            # 等待歌曲表格加载完成
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//table[contains(@class, "m-table")]/tbody/tr')
                )
            )

            # 抓取歌曲并保存
            songs = self._get_songs()
            self.save_to_json(songs)
            print(f"成功提取 {len(songs)} 首歌曲")
        finally:
            # 退出浏览器
            self.driver.quit()


if __name__ == "__main__":
    # 入口：运行爬虫
    m163 = musicu()
    m163.run()
