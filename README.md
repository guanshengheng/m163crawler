# m163crawler
一个使用selenium实现的对网易云音乐歌单进行爬取的爬虫程序
markdown# 网易云音乐歌单爬虫 (NetEase Music Playlist Crawler)

一个用于爬取网易云音乐歌单信息的Python工具，可以获取歌曲基本信息、歌词和封面图片。

## 功能特性

- 🎵 爬取指定歌单的所有歌曲信息
- 📝 自动下载歌词并保存为文本文件
- 🖼️ 下载歌曲封面图片
- 💾 将所有信息整合保存为JSON文件
- 🔐 支持Cookie登录状态
- 🚀 使用Selenium模拟真实用户行为

## 环境要求

- Python 3.7+
- Chrome浏览器

## 快速开始

### 1. 克隆项目

```bash
git clone <项目地址>
cd netease-music-crawler
2. 安装依赖
bashpip install -r requirements.txt
3. 配置文件
项目已包含 config.json 配置文件模板，请根据需要修改：
json{
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Cookie": "你的网易云音乐Cookie"
}
如何获取Cookie

在浏览器中登录网易云音乐
按F12打开开发者工具
切换到Network标签页
刷新页面
找到music.163.com的请求，复制Cookie值
将Cookie值粘贴到 config.json 文件中

4. 运行程序
bashpython musicu.py
自定义设置
更改目标歌单
修改 musicu.py 中的URL：
pythonself.URL = "https://music.163.com/#/playlist?id=你的歌单ID"
歌单ID可以从网易云音乐歌单页面的URL中获取，例如：

URL: https://music.163.com/playlist?id=123456789
歌单ID: 123456789

自定义保存路径
可以在初始化时修改保存目录：
python# 默认设置
self.lyrics_dir = "lyrics"    # 歌词保存目录
self.cover_dir = "images"     # 封面保存目录
文件结构
project/
├── musicu.py           # 主程序文件
├── config.json         # 配置文件
├── requirements.txt    # 依赖列表
├── songs.json         # 输出的歌曲信息（运行后生成）
├── lyrics/            # 歌词文件夹（运行后生成）
│   ├── 歌曲1.txt
│   └── 歌曲2.txt
└── images/            # 封面图片文件夹（运行后生成）
    ├── 歌曲1.jpg
    └── 歌曲2.jpg
输出说明
songs.json 数据结构
json[
    {
        "song_url": "https://music.163.com/#/song?id=123456",
        "song_title": "歌曲标题",
        "duration": "03:45",
        "artist_name": "艺术家名称",
        "artist_url": "https://music.163.com/#/artist?id=789",
        "album_name": "专辑名称",
        "album_url": "https://music.163.com/#/album?id=456",
        "lyrics_path": "lyrics/歌曲标题.txt",
        "cover_path": "images/歌曲标题.jpg"
    }
]
主要功能模块
核心类: musicu

__init__(config_file) - 初始化配置和浏览器
run() - 主执行方法
_get_songs() - 抓取歌单中的所有歌曲
download_lyrics(music_id) - 通过API下载歌词
download_cover(cover_url, song_title) - 下载封面图片
save_to_json(data, filename) - 保存数据到JSON文件

辅助方法

_load_config(config_file) - 加载配置文件
_add_cookies(cookie_str) - Cookie注入
_clean_soil(element) - 清理页面干扰元素
save_lyrics_to_file(song_title, lyrics) - 保存歌词文件

使用示例
pythonfrom musicu import musicu

# 使用默认配置文件
crawler = musicu()
crawler.run()

# 使用自定义配置文件
crawler = musicu("my_config.json")
crawler.run()
注意事项
⚠️ 重要提醒

合规使用: 请遵守网易云音乐的使用条款和robots.txt规定
Cookie更新: Cookie可能会过期，请定期更新config.json中的Cookie值
网络稳定: 确保网络连接稳定，避免请求中断
请求频率: 程序已包含适当的等待时间，请勿频繁运行
版权限制: 部分歌曲可能因版权限制无法获取完整信息
文件覆盖: 程序会自动跳过已存在的歌词和封面文件

故障排除
常见问题
Q: 程序运行后没有找到歌曲
A: 检查以下几点：
- Cookie是否有效且未过期
- 歌单ID是否正确
- 网络连接是否正常
- 歌单是否为公开状态
Q: Chrome浏览器启动失败
A: 确保：
- 已安装Chrome浏览器
- webdriver-manager能正常下载ChromeDriver
- 系统PATH环境变量正确
Q: 部分歌曲没有歌词或封面
A: 这是正常现象，可能原因：
- 歌曲没有提供歌词
- 需要VIP权限
- 网络请求失败
- 版权限制
调试模式
如需调试，可以修改Chrome选项：
python# 显示浏览器窗口（去掉 headless 模式）
options.add_argument("--disable-gpu")  # 保留这行
# options.add_argument("--headless")   # 注释这行来显示浏览器
更新日志

v1.0.0 - 初始版本

支持歌单信息爬取
歌词和封面下载
JSON数据导出



免责声明
本工具仅供学习和研究使用。使用者应当：

遵守相关法律法规和网站服务条款
不得用于商业用途
不得进行大规模爬取影响网站正常运行
尊重音乐版权，合理使用获取的内容

因使用本工具产生的任何法律责任，均由使用者自行承担。
