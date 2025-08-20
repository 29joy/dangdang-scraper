"""
config.py

Module Description:
This module contains the base configuration for the crawler project, including:
- Search keyword and target website
- Network request and retry configuration (used in image processing module)
- Product page parsing parameters
- File name sanitization rules
- Image validation and download settings

All configurations are global constants and can be imported in other project modules.

模块说明：
该模块存放整个爬虫项目的基础配置，包括：
- 搜索关键词与目标网站
- 网络请求和重试配置（用于图片处理模块）
- 解析产品页面的参数配置
- 文件名清理规则
- 图片验证和下载相关配置

所有配置均为全局常量，可在项目各模块中导入使用。
"""

# Search configuration
SEARCH_KEYWORD: str = "AI"  # The keyword for search
TARGET_SITE: str = "https://www.dangdang.com/"  # The target website URL

# Network request configuration
# headers = {
#     'User-Agent': 'Mozilla/5.0',
#     'Referer': 'https://www.dangdang.com'
# }
# Session and retry mechanism can prevent occasional network errors

# Product page parsing configuration
PARSE_PRODUCT_CONFIG: dict[str, int] = {
    "total_pages": 3,  # Total number of pages to scrape
    "wait_time": 10    # Explicit wait time in seconds
}

# File name sanitization rules
SANITIZE_RULES: dict[str, int | str] = {
    "replace_space": "_",        # Replace spaces with underscore
    "allowed_chars": "-_()[]{}", # Allowed special characters
    "max_length": 20,            # Maximum length of file name
    "max_words_cn": 3,           # Max number of words for Chinese titles
    "max_words_en": 5,           # Max number of words for English titles
}

# Image validation configuration
IMAGE_VALIDATION_CONFIG: dict[str, int] = {
    "max_retries": 3,            # Max retry times if validation fails
    "min_image_file_size": 1024, # Minimum image file size in bytes
    "total_num_of_retry": 3      # Total retry attempts
    # Placeholder for image keyword filtering can be added later
}

# Image download configuration
IMAGE_DOWNLOAD_CONFIG: dict[str, int] = {
    "session_max_retries": 3,    # Max retry times if download fails
    "total_num_of_retry": 3      # Total retry attempts
}
