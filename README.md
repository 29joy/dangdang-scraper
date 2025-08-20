# 当当图书爬虫 · Book Scraper for dangdang.com

🚀 一个基于 Selenium 自动化的图书信息提取工具，当前版本可抓取特定关键词（如 “AI”）的搜索结果图书数据，并保存为 Excel 文件，封面图下载至本地。  
A simple yet effective book information scraper for [dangdang.com](https://www.dangdang.com/) using Selenium. It extracts book data from search results and saves them into Excel with cover images.

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Selenium](https://img.shields.io/badge/Selenium-Automation-green)
![Excel](https://img.shields.io/badge/Excel-Data%20Export-yellow)
![Web Scraping](https://img.shields.io/badge/Web-Scraping-orange)

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

python src/main.py

当前版本固定搜索关键词为 “AI”。程序将自动抓取搜索结果前几页图书数据，并保存至 Excel 文件，并下载封面图。
The current version scrapes search results for the keyword **"AI"**. Results will be saved to an Excel file and corresponding cover images will be downloaded.

## 🌐 浏览器驱动说明 Browser Driver

本项目自动处理浏览器驱动，无需手动下载 ChromeDriver。首次运行时可能稍有等待，请保持网络畅通。
No need to manually install or configure ChromeDriver. The project handles browser driver setup automatically.

## 📁 文件结构说明 File Structure

```
dangdang-scraper/
├── src/                        # 主程序文件 / Source code of the scraper
│   ├── main.py                 # 爬虫主逻辑入口 / Main entry point of the scraper
│   ├── config.py               # 配置文件 / Global configuration file
│   ├── context.py              # 运行上下文管理 / Runtime context management
│   ├── image_process.py        # 图像处理功能（下载/重命名/校验）/ Image processing utilities
│   ├── parse_module.py         # 页面解析模块 / HTML parsing module
│   ├── product_selectors.py    # 页面元素选择器 / Product selectors for scraping
│   ├── request_module.py       # 网络请求模块 / Network request handling
│   ├── storage_module.py       # 数据存储模块（Excel/文件）/ Data storage utilities
│   ├── logger.py               # 日志记录模块 / Logger module
│
├── output/                     # 输出结果目录 / Output directory
│   └── images/                 # 封面图像保存位置（含 .gitkeep 占位）/ Folder for cover images (with .gitkeep placeholder)
│
├── docs/                       # 项目文档 / Project documentation
│   ├── pseudocode/             # 伪代码文件夹 / Pseudocode drafts
│   ├── flowcharts/             # 流程图文件夹 / Flowcharts
│   ├── mindmaps/               # 思维导图文件夹 / Mind maps
│   ├── architecture_diagrams/  # 模块关系图文件夹 / Architecture diagrams
│   └── README_docs.md          # docs 目录说明 / Documentation folder guide
│
├── dev_logs/                   # 开发日志 / Development logs
│   └── README_dev_logs.md      # 开发日志说明文档 / Guide for development logs
│
├── logs/                       # 全局运行日志 / Global runtime logs
│
├── tests/                      # 测试代码目录（单元/集成测试）/ Unit and integration tests
│
├── README.md                   # 项目说明文档 / Project README
├── CHANGELOG.md                # 更新日志 / Changelog
├── CONFIG.md                   # 配置说明文档 / Configuration guide
├── LICENSE                     # 项目许可证 / Project license
├── requirements.txt            # Python 依赖 / Python dependencies
```

> ⚠️ 注意：Git 默认不会追踪空文件夹，`output/images/` 中添加了 `.gitkeep` 文件以保留文件夹结构。
> Note: Git doesn't track empty folders. We include a `.gitkeep` file under `output/images/` to preserve the folder structure.

## 📝 后续版本计划 TODO

Core Enhancements / 核心功能增强

- [ ] Add API scraping mode (to reduce reliance on Selenium)
      增加 API 抓取模式（减少对 Selenium 的依赖）
- [ ] Add multi-keyword batch scraping
      增加多关键词批量抓取功能
- [ ] Add quick scraping version using requests + BeautifulSoup for simpler pages
      增加 requests + BeautifulSoup 简易页面快速爬取版本
- [ ] Add fake headers / proxy IP support to bypass anti-scraping measures
      增加伪造 headers / 代理 IP 功能，应对反爬机制
- [ ] Add multi-threaded image downloading for efficiency
      增加多线程图片下载，提高效率

Quality & Reliability / 稳定性与质量

- [ ] Add unit tests
      增加单元测试
- [ ] Auto-generate crawl reports (success count, failure count, logs)
      自动生成爬取报告（成功数、失败数、日志）

Deployment & CI/CD / 部署与自动化

- [ ] Add Docker deployment support (optional, for containerized environments)
      增加 Docker 部署支持（可选，用于容器化环境）
- [ ] Add CI/CD integration (automatic testing and release)
      增加 CI/CD 集成（自动测试与发布）

Expansion / 功能扩展

- [ ] Support more websites
      支持更多网站

## 🧑‍💻 作者 Author

Joy · [@29joy](https://github.com/29joy)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.  
You are welcome to use, modify, and contribute under the terms of this license.

本项目基于 MIT 协议开源 - 详细信息请参阅 [LICENSE](./LICENSE) 文件。  
欢迎在遵守该协议的前提下使用、修改和贡献本项目。
