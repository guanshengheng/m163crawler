# 🎵 网易云音乐爬虫

本项目可以自动化爬取 **网易云音乐歌单** 中的所有歌曲信息，并将歌词和封面保存到本地，同时生成一个统一的 JSON 文件，方便后续处理或分析。

---

## 功能介绍

### 1. 歌曲信息抓取

* 自动进入指定歌单页面，解析所有歌曲条目。
* 获取每首歌的：

  * **歌曲标题**
  * **歌曲链接**
  * **时长**
  * **歌手名称与链接**
  * **专辑名称与链接**

### 2. 歌词下载

* 通过网易云公开 API 获取歌词。
* 自动去除歌词中的时间戳，仅保留纯净歌词文本。
* 歌词会以 `.txt` 文件的形式保存到 `lyrics/` 文件夹中。
* 如果歌词文件已存在，程序会自动跳过，不会重复下载。

### 3. 封面下载

* 自动解析歌曲页面中的 **封面图片地址**。
* 将封面图片下载到本地 `images/` 文件夹，文件名与歌曲标题对应。
* 如果图片已存在，本地不会重复下载。

### 4. 统一结果保存

* 所有歌曲的信息会整合到一个 JSON 文件 `songs.json`，每首歌包含以下字段：

  ```json
  {
      "song_url": "https://music.163.com/song?id=123456",
      "song_title": "示例歌曲",
      "duration": "04:12",
      "artist_name": "示例歌手",
      "artist_url": "https://music.163.com/artist?id=654321",
      "album_name": "示例专辑",
      "album_url": "https://music.163.com/album?id=111111",
      "lyrics_path": "lyrics/示例歌曲.txt",
      "cover_path": "images/示例歌曲.jpg"
  }
  ```

---

## 📂 运行结果

运行完成后，你将得到以下目录结构：

```
.
├── songs.json          # 歌单完整信息
├── lyrics/             # 歌词保存目录
│   ├── 歌曲1.txt
│   ├── 歌曲2.txt
│   └── ...
├── images/             # 封面图片保存目录
│   ├── 歌曲1.jpg
│   ├── 歌曲2.jpg
│   └── ...
```

---

## ⚙️ 使用流程说明

### 1. 安装依赖

请确保已安装 Python 3，然后安装依赖库：

```bash
pip install requests beautifulsoup4 selenium webdriver-manager
```

### 2. 准备浏览器环境

* 安装 **Google Chrome**（最新版）。
* `chromedriver` 由 `webdriver-manager` 自动下载，无需手动配置。

### 3. 配置 `config.json`

在项目根目录新建 `config.json` 文件，内容如下：

```json
{
    "User-Agent": "你的浏览器UA",
    "Cookie": "你的网易云登录Cookie"
}
```

#### 获取 UA 和 Cookie 的方法：

1. 打开 [网易云音乐官网](https://music.163.com)，并使用账号登录。
2. 按 `F12` 打开开发者工具 → 进入 `Network` 标签。
3. 刷新页面，点击任意一个请求。
4. 在 `Headers` 中找到：

   * **User-Agent**（请求头）
   * **Cookie**（请求头）
5. 复制并粘贴到 `config.json`。

⚠️ 注意：

* **Cookie 有效期有限**，过期后需要重新获取。
* 必须是已登录账号的 Cookie，否则可能无法访问部分歌曲或歌词。

### 4. 运行程序

在项目目录下运行：

```bash
python main.py
```

### 5. 查看结果

* 歌词会保存到 `lyrics/` 文件夹
* 封面会保存到 `images/` 文件夹
* 完整数据会保存到 `songs.json`

---

## 📝 应用场景

* **歌词与封面备份**：保存喜欢的歌单数据到本地，避免丢失。
* **数据分析**：对歌词进行文本分析，或统计歌手、专辑数据。
* **二次开发**：基于 `songs.json` 开发音乐推荐、歌词可视化等功能。

---

本readme.md文档由chatgpt生成，请注意甄别。如有问题可联系qq:3406702953.
