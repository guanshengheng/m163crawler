# 网易云音乐爬虫工具 🎵

这是一个基于 **Selenium + Requests + BeautifulSoup** 的网易云音乐爬虫脚本。  
主要功能包括：
- 爬取指定歌单中的所有歌曲信息（歌曲名、时长、歌手、专辑等）
- 通过 API 下载歌词（保存为 `.txt` 文件）
- 下载歌曲封面（保存为 `.jpg` 文件）
- 将完整的歌曲信息保存到 `songs.json` 文件中

---

## 功能说明

- **歌词下载**：调用网易云歌词 API，去除时间戳，保存为纯文本格式  
- **封面下载**：解析歌曲页面中的 `application/ld+json` 数据，获取封面图片并保存  
- **数据保存**：所有歌曲信息会整合并存储到 `songs.json` 文件，包含：
  ```json
  {
      "song_url": "歌曲链接",
      "song_title": "歌曲标题",
      "duration": "时长",
      "artist_name": "歌手名称",
      "artist_url": "歌手链接",
      "album_name": "专辑名称",
      "album_url": "专辑链接",
      "lyrics_path": "歌词文件路径",
      "cover_path": "封面图片路径"
  }
项目结构
bash
复制代码
.
├── lyrics/             # 歌词文件保存目录
├── images/             # 封面图片保存目录
├── songs.json          # 所有歌曲信息保存文件
├── config.json         # 配置文件（User-Agent 与 Cookie）
├── crawler.py          # 主爬虫脚本
└── README.md           # 项目说明
环境依赖
请确保安装以下依赖：

bash
复制代码
pip install selenium requests beautifulsoup4 webdriver-manager
配置文件（config.json）
运行前需要准备一个 config.json 文件，存储 User-Agent 与 Cookie 信息：

json
复制代码
{
    "User-Agent": "你的浏览器UA字符串",
    "Cookie": "你的网易云登录Cookie"
}
如何获取 UA 和 Cookie？
打开 网易云音乐 并登录

按 F12 打开开发者工具

进入 Network，刷新页面，随便点一个请求

在 Headers 里找到：

User-Agent

Cookie

将它们复制到 config.json 中

使用方法
克隆或下载本项目到本地

准备 config.json 文件

运行爬虫：

bash
复制代码
python crawler.py
爬取结果会自动保存到：

songs.json：歌曲信息

lyrics/：歌词文件

images/：封面图片

注意事项 ⚠️
网易云可能有反爬机制，建议不要频繁请求

需要保持 Cookie 有效，否则可能无法访问部分数据

爬虫运行时会自动打开一个 Chrome 浏览器窗口

歌词和封面文件如果已存在，不会重复下载

示例运行效果
bash
复制代码
成功提取 20 首歌曲
生成的 songs.json 示例：

json
复制代码
[
    {
        "song_url": "https://music.163.com/song?id=123456",
        "song_title": "告白气球",
        "duration": "04:15",
        "artist_name": "周杰伦",
        "artist_url": "https://music.163.com/artist?id=6452",
        "album_name": "周杰伦的床边故事",
        "album_url": "https://music.163.com/album?id=34567",
        "lyrics_path": "lyrics/告白气球.txt",
        "cover_path": "images/告白气球.jpg"
    }
]
License
本项目仅供学习和研究使用，请勿用于商业用途。
