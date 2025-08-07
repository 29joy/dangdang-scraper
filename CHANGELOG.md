# CHANGELOG

所有显著更改将在此文档中记录。  
All notable changes to this project will be documented in this file.

该项目遵循 [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)。  
This project adheres to [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

版本编号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。  
Versioning follows [Semantic Versioning](https://semver.org/).

## [v1.0.0] - 2025-08-07

### Added / 新增

- 支持从当当网搜索图书信息并抓取多页数据  
  Support for searching books from dangdang.com and scraping multiple pages of results
- 图书信息包括：标题、作者、价格、出版社、出版日期、封面图链接等  
  Extracted info includes: title, author, price, publisher, publish date, cover image URL, etc.
- 将结果保存为 Excel 文件，并按页分工作表存储  
  Save results as Excel file with one worksheet per page
- 支持下载封面图至 `output/images/` 文件夹  
  Support downloading book cover images into `output/images/`
- 异常处理：封面图下载失败将记录在 Excel 中  
  Exception handling: failed image downloads are marked in Excel
- 自动创建输出文件夹结构（若不存在）  
  Auto-create output folders if not present

### Changed / 变更

- 设置默认搜索关键词为 `AI`（可配置）  
  Default search keyword set to `AI` (can be customized)

### Fixed / 修复

- 修复了图片命名重复与覆盖问题  
  Fixed issue with duplicate image naming and overwriting
- 处理了封面图下载超时等错误  
  Handled image download timeout and other exceptions
