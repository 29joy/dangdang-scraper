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

## [v1.1.0] - 2025-08-10

### Added / 新增

- 增加开发者维护日志文件夹及相关日志文件。
  Added developer maintenance log folder and files.

- 增加图片 URL 有效性判断的 reason 变量，实现对无效图片的分类管理。
  Introduced a reason variable for image URL validation to categorize invalid images.

- 针对因网络响应超时及图片加载不完整导致无效的图片，增加判断重试机制。
  Implemented retry mechanism for images invalidated due to network timeout and incomplete loading.

- 增加判断过程失败时的异常收集，为长期维护做准备。
  Added exception collection for failures during image validity checks to facilitate long-term maintenance.

- 增加图片下载失败的 reason 变量，收集导致下载失败的异常信息。
  Added reason variable for image download failures with exception tracking.

- 增加网页解析失败的日志收集功能。
  Added log collection for webpage parsing failures.

- 对变量名、日志及路径命名进行规范化，提升代码可读性和维护性。
  Standardized variable names, log messages, and file paths to improve code readability and maintainability.

- 对整体代码流程进行梳理，为后续封装做铺垫。
  Refactored and clarified the overall code workflow to prepare for upcoming code encapsulation.

## [v2.0.0] - 2025-08-20

### Added / 新增

- **config.py**  
  Centralized configuration file, providing a clear entry point for parameter management.  
  配置文件集中管理参数，入口更清晰。

- **logger.py**  
  Introduced logging functionality for better debugging and monitoring.  
  新增日志模块，支持更清晰的调试与运行监控。

- **product_selectors.py**  
  Encapsulated product-related selectors for improved maintainability.  
  新增选择器模块，集中管理网页元素定位，更易维护与扩展。

- **LICENSE & CONFIG.md**  
  Added open-source license and configuration documentation.  
  新增开源许可证与配置文档，提升项目规范性。

### Changed / 变更

- **Refactored project structure**  
  Migrated from a single-file script to a modularized architecture for better scalability.  
  项目由单文件脚本重构为模块化结构，更具可扩展性。

- **main.py → run_pipeline**  
  Upgraded script-style execution to a reusable function with parameter support, enabling unit testing and integration.  
  将脚本式流程升级为可复用的 `run_pipeline`，支持传参，便于单元测试和后续集成。

- **context.py improvements**  
  Replaced string paths with `pathlib.Path` for type safety and readability; added list data into `context` for centralized state management.  
  使用 `pathlib.Path` 替代字符串路径，更直观安全；部分列表加入 `context` 统一管理。

- **WebDriverWait**  
  Substituted `time.sleep()` with `WebDriverWait`, improving stability and efficiency.  
  用 `WebDriverWait` 替代 `time.sleep()`，提高了稳定性与效率。

### Fixed / 修复

- **Logging support**  
  Enhanced runtime visibility by fixing missing log outputs.  
  修复了缺失日志输出的问题，提升运行可观测性。

- **Image validation & download**  
  Improved error handling and robustness of image downloading logic.  
  优化了图片验证与下载逻辑，增强了容错与稳定性。
