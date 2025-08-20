"""
image_process.py

Module Description:
This module provides image processing utilities for downloading and validating product images
from the target website. It includes functions to validate image URLs, retry downloads,
sanitize filenames for saving, and maintain logging of failures.

Key functionalities:
- Validate images with URL checks and content checks
- Retry logic for network failures or incomplete images
- Filename sanitization for both Chinese and English titles
- Logging of validation and download failures for debugging and analysis
- Handling placeholder images to avoid saving non-informative graphics

模块说明：
该模块提供了爬取目标网站商品图片的处理工具，包括图片验证、下载重试、
文件名清理、失败日志记录等功能。

主要功能：
- 对图片 URL 及内容进行有效性验证
- 针对网络失败或加载不全图片的重试逻辑
- 中文和英文标题的文件名清理
- 记录验证及下载失败日志，方便调试和分析
- 处理占位图，避免保存无效图片
"""

# ===== Standard Libraries =====
import traceback

import jieba

# ===== Third-Party Libraries =====
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import *

# ===== Project Custom Modules =====
from logger import *

# Keywords for placeholder images
PLACEHOLDER_KEYWORDS = [
    "nofound_o.jpg",
    "default.jpg",
    "noimg.png",
    "placeholder",
    "nopic.jpg",
    "none.jpg",
    "default.png",
    "default_cover.jpg",
    "loading.gif",
    "noimage",
    "cover_default"
]


def is_valid_image(img_url: str, context, config: dict) -> tuple[bool, str, str]:
    """Check if the image URL is valid and content meets requirements.

    Args:
        img_url (str): The URL of the image to validate.
        context: Runtime context object for logging paths.
        config (dict): Configuration for validation, e.g., max retries, min file size.

    Returns:
        tuple[bool, str, str]: (is_valid, normalized_img_url, reason)
    """
    # Normalize URL
    if img_url.startswith("//"):
        img_url = "http:" + img_url
    elif img_url.startswith("/"):
        img_url = "https://www.dangdang.com" + img_url

    # Basic URL validation
    if not img_url or img_url.strip() in ["", "#"]:
        return False, img_url, "Null or Incorrect Link"
    if any(key in img_url for key in PLACEHOLDER_KEYWORDS):
        logger.info(f"{img_url} identified as placeholder image")
        return False, img_url, "Placeholder Graphic"

    # HTTP request and content validation
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Referer': 'https://www.dangdang.com'
    }

    try:
        session = requests.Session()
        retries = Retry(
            total=config.get("max_retries"),
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        response = session.get(img_url, headers=headers, timeout=15)

        if response.status_code == 200:
            content_type = response.headers.get('Content-Type', '')
            if not content_type.startswith("image/"):
                return False, img_url, "Not Image Link"

            if any(key in response.url for key in PLACEHOLDER_KEYWORDS):
                logger.info(f"{img_url} response URL identified as placeholder")
                return False, img_url, "Placeholder Graphic"

            if len(response.content) == 0:
                return False, img_url, "Empty Image"
            elif 0 < len(response.content) < config.get("min_image_file_size"):
                return False, img_url, "Incomplete Image (Retryable)"
            else:
                return True, img_url, "OK"
        else:
            return False, img_url, "Network Response Failed (Retryable)"
    except Exception as e:
        error_msg = traceback.format_exc()
        exception_reason = f"Unhandled Exception: {type(e).__name__} - {str(e)}"
        exception_type = exception_reason.split(" - ")[0].replace("Unhandled Exception: ", "")
        logger.error(f"is_valid_image unknown error: {img_url}: {exception_reason}")
        log_to_json({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "url": img_url,
                     "error": exception_reason, "exception_type": exception_type, "error_msg": error_msg},
                    context.img_not_valid_unhandled_exception_log_path)
        return False, img_url, exception_reason


def validate_image_with_retry(img_url: str, img_path, title: str, price: str, author: str, context, config: dict) -> tuple[bool, str, str]:
    """Validate image with multiple retries if needed.

    Args:
        img_url (str): URL of the image.
        img_path: Local path where image will be saved.
        title (str): Product title.
        price (str): Product price.
        author (str): Product author.
        context: Runtime context for logging.
        config (dict): Validation configuration.

    Returns:
        tuple[bool, str, str]: (is_valid, normalized_img_url, reason)
    """
    total_num_of_retry = config.get("total_num_of_retry")
    is_valid, new_img_url, not_valid_reason = is_valid_image(img_url, context, IMAGE_VALIDATION_CONFIG)

    if not is_valid:
        if not_valid_reason not in ["Network Response Failed", "Incomplete Image"]:
            logger.info(f"{img_path}: {new_img_url} is placeholder or invalid")
        else:
            for num_of_retry in range(1, total_num_of_retry + 1):
                logger.info(f"Retry {num_of_retry}: Image URL not valid due to {not_valid_reason}")
                is_valid, new_img_url, not_valid_reason = is_valid_image(img_url, context, IMAGE_VALIDATION_CONFIG)
                if is_valid:
                    break
                else:
                    if not_valid_reason not in ["Network Response Failed", "Incomplete Image"]:
                        logger.info(f"{img_path}: {new_img_url} identified as invalid")
                        break
                    else:
                        logger.info(f"{img_path}: {new_img_url} retry {num_of_retry} still invalid due to {not_valid_reason}")
                        log_to_json({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                     "url": new_img_url, "retry_count": num_of_retry,
                                     "reason": not_valid_reason}, context.img_not_valid_retry_log_path)
                        if num_of_retry == total_num_of_retry:
                            context.img_validation_fail_list.append({
                                "Title": title,
                                "Price": price,
                                "Author": author,
                                "Img_URL": new_img_url,
                                "Fail_Reason": not_valid_reason,
                                "Retry_Count": num_of_retry
                            })
    return is_valid, new_img_url, not_valid_reason


def truncate_chinese(title: str, max_words: int = 3, max_length: int = 20) -> str:
    """Truncate Chinese title by word segmentation.

    Args:
        title (str): Original title.
        max_words (int): Maximum number of words to keep.
        max_length (int): Maximum length of the final string.

    Returns:
        str: Truncated title.
    """
    clean_title = re.sub(r'[\/:*?"<>|]', '', title)
    words = list(jieba.cut(clean_title))
    truncated = ''.join(words[:max_words])
    if len(truncated) > max_length:
        truncated = truncated[:max_length] + '...'
    return truncated


def truncate_english(title: str, max_words: int = 5, max_length: int = 20) -> str:
    """Truncate English title by word boundaries.

    Args:
        title (str): Original title.
        max_words (int): Maximum number of words to keep.
        max_length (int): Maximum length of the final string.

    Returns:
        str: Truncated title.
    """
    clean_title = re.sub(r'[\/:*?"<>|]', '', title)
    words = clean_title.split()
    truncated = ' '.join(words[:max_words])
    if len(truncated) > max_length:
        truncated = truncated[:max_length]
        if ' ' in truncated:
            truncated = ' '.join(truncated.split(' ')[:-1])
        truncated += '...'
    return truncated


def sanitize_filename(title: str, rules: dict) -> str:
    """Sanitize the title to be used as a valid filename.

    Args:
        title (str): Original title.
        rules (dict): Sanitization rules, e.g., allowed chars, max length.

    Returns:
        str: Sanitized filename.
    """
    allowed_chars = rules.get("allowed_chars", "")
    title = re.sub(f"[^0-9a-zA-Z{re.escape(allowed_chars)}]", "_", title)

    if re.search(r'[\u4e00-\u9fff]', title):
        return truncate_chinese(title, max_words=rules.get("max_words_cn"), max_length=rules.get("max_length"))
    else:
        title = truncate_english(title, max_words=rules.get("max_words_en"), max_length=rules.get("max_length"))
        title = title.replace(" ", rules.get("replace_space", "_"))
        return title


def fail_download_image_add_logging(target_list: list, img_url: str, img_path, title: str, price: str, author: str,
                                    page: int, idx: int, fail_reason: str, error_msg: str, retry_num: int,
                                    retry_flag: bool = False):
    """Log failed image download details into a list.

    Args:
        target_list (list): List to append failure info.
        img_url (str): Image URL.
        img_path: Local image path.
        title (str): Product title.
        price (str): Product price.
        author (str): Product author.
        page (int): Page number.
        idx (int): Image index.
        fail_reason (str): Reason for failure.
        error_msg (str): Error message or traceback.
        retry_num (int): Retry count.
        retry_flag (bool): Whether retry succeeded.
    """
    target_list.append({
        "Title": title,
        "Price": price,
        "Author": author,
        "Page": page,
        "Index": idx,
        "Img_URL": img_url,
        "Img_Path": str(img_path),
        "Fail_Reason": fail_reason,
        "Error_MSG": error_msg,
        "Retry_Count": retry_num,
        "Retry_Success": retry_flag
    })


def download_image(img_url: str, save_path, config: dict) -> tuple[bool, str, str]:
    """Download an image from a URL with session retries and return status.

    Args:
        img_url (str): URL of the image to download.
        save_path: Local path to save the downloaded image.
        config (dict): Download configuration including session_max_retries.

    Returns:
        tuple[bool, str, str]: (success_flag, reason, error_message)
    """
    try:
        # Configure session and retries
        session = requests.Session()
        retries = Retry(
            total=config.get("session_max_retries"),
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount('http://', adapter)
        session.mount('https://', adapter)

        response = session.get(img_url, timeout=5)
        with open(save_path, "wb") as f:
            f.write(response.content)
        return True, "OK", "OK"
    except Exception as e:
        error_msg = traceback.format_exc()
        exception_reason = f"Error downloading: {type(e).__name__} - {str(e)}"
        logger.error(f"Downloading: {save_path}, {img_url}: {exception_reason}")
        return False, exception_reason, error_msg


def process_image(img_url: str, title: str, price: str, author: str, page: int, idx: int, context) -> tuple[str, str]:
    """Process a single image: validate, sanitize filename, and download.

    Args:
        img_url (str): URL of the image to process.
        title (str): Product title.
        price (str): Product price.
        author (str): Product author.
        page (int): Page number.
        idx (int): Image index on the page.
        context: Runtime context containing directories and log paths.

    Returns:
        tuple[str, str]: (image filename or status, image path or status)
    """
    safe_title = sanitize_filename(title, SANITIZE_RULES)
    img_filename = f"page{page}_{idx}_{safe_title}.jpg"
    img_path = context.images_dir / img_filename

    is_valid, new_img_url, not_valid_reason = validate_image_with_retry(
        img_url, img_path, title, price, author, context, IMAGE_VALIDATION_CONFIG
    )

    if is_valid:
        download_success, fail_reason, error_msg = download_image(new_img_url, img_path, IMAGE_DOWNLOAD_CONFIG)
        if download_success:
            return os.path.basename(img_path), img_path
        else:
            fail_download_image_add_logging(
                context.first_download_fail_list, img_url, img_path, title, price, author,
                page, idx, fail_reason, error_msg, 0, False
            )
            return "Download Failed", "No Image"
    else:
        if not_valid_reason not in ["Network Response Failed", "Incomplete Image"]:
            return "No Image or Placeholder", "No Image"
        else:
            return not_valid_reason, "No Image"


def final_download_for_fail_img(all_pages_data: dict, context, config: dict):
    """Retry download for images that failed in the first attempt.

    Args:
        all_pages_data (dict): All scraped page data containing image references.
        context: Runtime context with fail lists and directories.
        config (dict): Download configuration with retry counts.
    """
    total_num_of_retry = config.get("total_num_of_retry")
    if len(context.first_download_fail_list):
        logger.info("Starting second attempt for failed images")

        for num_of_retry in range(1, total_num_of_retry + 1):
            for item in context.first_download_fail_list:
                if not item["Retry_Success"]:
                    download_success, second_fail_reason, error_msg = download_image(
                        item["Img_URL"], item["Img_Path"], IMAGE_DOWNLOAD_CONFIG
                    )
                    item["Retry_Count"] = num_of_retry
                    if download_success:
                        img_status = os.path.basename(item["Img_Path"])
                        entry = all_pages_data["Page"]["Index"]
                        if entry["Title"] == item["Title"]:
                            entry["Cover_Img_Filename"] = img_status
                            entry["Cover_Img_Path"] = item["Img_Path"]
                            item["Retry_Success"] = True
                        else:
                            logger.error("!!! Unknown data recording ERROR, recommend retrying entire data capture process !!!")
                    else:
                        if num_of_retry == total_num_of_retry:
                            logger.info(f"{item['Img_URL']} second download failed, adding to fail summary")
                            fail_download_image_add_logging(
                                context.second_download_fail_list, item["Img_URL"], str(item["Img_Path"]),
                                item["Title"], item["Price"], item["Author"], item["Page"], item["Index"],
                                second_fail_reason, error_msg, num_of_retry
                            )
                                second_fail_reason, error_msg, num_of_retry
                            )
