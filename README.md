# 当当图书爬虫 · Book Scraper for dangdang.com

🚀 一个基于 Selenium 自动化的图书信息提取工具，当前版本可抓取特定关键词（如 “AI”）的搜索结果图书数据，并保存为 Excel 文件，封面图下载至本地。  
A simple yet effective book information scraper for [dangdang.com](https://www.dangdang.com/) using Selenium. It extracts book data from search results and saves them into Excel with cover images.

## 📌 功能 Features

- 自动爬取指定关键词的图书信息（当前关键词为 “AI”）
  Automatically crawl book information for specified keywords (the current keyword is "AI")
- 支持翻页抓取前多页数据
  Support for crawling multiple pages by turning pages
- 保存为 Excel 文件，字段包括标题、作者、出版社、价格等
  Save as an Excel file, with fields including title, author, publisher, price, etc.
- 同步下载封面图片，保存在本地 `output/images/` 文件夹中
  Synchronously download cover images and save them in the local `output/images/` folder

## 💻 环境要求 Environment

- Python 3.9+
- Google Chrome 浏览器（建议使用最新版）
  Google Chrome Browser (recommended to use the latest version)

## ⚙️ 安装依赖 Install Dependencies

pip install -r requirements.txt

## ▶️ 运行方式 How to Run

python src/scraper.py

当前版本固定搜索关键词为 “AI”。程序将自动抓取搜索结果前几页图书数据，并保存至 Excel 文件，并下载封面图。
The current version scrapes search results for the keyword **"AI"**. Results will be saved to an Excel file and corresponding cover images will be downloaded.

## 🌐 浏览器驱动说明 Browser Driver

本项目自动处理浏览器驱动，无需手动下载 ChromeDriver。首次运行时可能稍有等待，请保持网络畅通。
No need to manually install or configure ChromeDriver. The project handles browser driver setup automatically.

## 📁 文件结构说明 File Structure

dangdang-scraper/
├── src/ # 主程序文件
│ ├── scraper.py # 爬虫主逻辑
│ ├── utils.py # 辅助工具函数
├── output/ # 输出结果
│ └── images/ # 封面图像保存位置（含 .gitkeep 占位）
├── requirements.txt # Python 依赖
├── README.md # 项目说明
├── CHANGELOG.md # 更新日志

> ⚠️ 注意：Git 默认不会追踪空文件夹，`output/images/` 中添加了 `.gitkeep` 文件以保留文件夹结构。
> Note: Git doesn't track empty folders. We include a `.gitkeep` file under `output/images/` to preserve the folder structure.

## 📝 后续版本计划 TODO

- [ ] 支持用户自定义输入关键词
- [ ] 增加抓取图书简介/评分信息
- [ ] 支持并发优化封面图下载
- [ ] 增加 CLI 参数控制（如页数、文件名、输出目录等）

## 🧑‍💻 作者 Author

Joy · [@29joy](https://github.com/29joy)

## 📄 License

本项目仅供学习用途，严禁用于商业用途。请遵守目标网站的 Robots 协议及相关法律法规。
For educational use only. Do not use for commercial purposes. Please respect the target site's robots.txt and local laws.
