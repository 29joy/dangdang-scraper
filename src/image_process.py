# 图片处理封装
# 图片下载及有效性判断等
# ===== 标准库模块 =====
import json
import os
import re
import traceback
from datetime import datetime

# ===== 第三方库 =====
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# ===== 项目自定义模块 =====
# from mymodule import myfunction

# ===== 常量定义 =====
MIN_IMAGE_FILE_SIZE = 2048
TITLE_MAX_LENGTH = 15
# 占位图关键词
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
    "cover_default",
    # 其他关键词
]

first_download_fail_list = []
second_download_fail_list = []


# is_valid_image 判断img是否有效
def is_valid_image(img_url, context, max_retries=3):
    # img download阶段2：标准化URL(补全http/https等)
    if img_url.startswith("//"):
        img_url = "http:" + img_url
    elif img_url.startswith("/"):
        img_url = "https://www.dangdang.com" + img_url

    # img download阶段阶段 3：初步 URL 判断
    # 阶段3.1: 是否是空链接、错误路径、伪链接(如 /images/none.jpg)
    if not img_url:
        return False, img_url, "Null Link"  # url有问题，不重试
    if img_url.strip() in ["", "#"]:
        return False, img_url, "Incorrect Link"  # url有问题，不重试
    # 阶段3.2: 先基于URL判断明显无效图或占位图
    if any(key in img_url for key in PLACEHOLDER_KEYWORDS):
        print(f"{img_url}进入占位图识别")
        return False, img_url, "Placeholder Graphic"

    # img download阶段4: 发送请求(请求本身的网络层问题)
    # # 阶段4.0: 设置网络请求配置->后续主内容移出到config.py配置项文件
    headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.dangdang.com"}
    try:
        # 阶段4.1: 配置Session和重试机制防止偶发网络错误
        session = requests.Session()
        retries = Retry(
            total=max_retries,
            backoff_factor=1,  # 等待时间：1s, 2s, 4s...
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        response = session.get(img_url, headers=headers, timeout=15)
        # 阶段4.2: 检查响应是否成功
        if response.status_code == 200:  # 响应成功
            # img download阶段5：响应内容校验
            # 阶段5.1：过滤掉伪装成图片的网页、JSON、JS等内容
            content_type = response.headers.get("Content-Type", "")
            if content_type in [
                "image/jpeg",
                "image/png",
                "image/webp",
            ]:  # 正确图片, 保存逻辑
                # 阶段5.2：response.url是否跳转到了占位图
                if any(key in response.url for key in PLACEHOLDER_KEYWORDS):
                    print(f"{img_url}的response: {response}进入占位图识别")
                    return False, img_url, "Placeholder Graphic"  # 占位图，不重试
                # 阶段5.3：内容长度小于设定值说明是空图、错误图片或加载不全
                if len(response.content) > MIN_IMAGE_FILE_SIZE:
                    return True, img_url, "OK"  # valid img
                elif len(response.content) > 0:
                    return (
                        False,
                        img_url,
                        "Incomplete Image",
                    )  # 可能是加载不全，可加入重试列表
                    # 这里是否可以直接作为 "OK" 处理呢, 不可以，只能加入重试, 加载不全直接下载可能会导致以为下载成功了但图片打不开的情况
                else:
                    return False, img_url, "Empty Image"  # 空内容，跳过不重试
            else:  # 记录失败日志
                # print(f"跳过非图片链接: {img_url}，类型: {content_type}")
                return False, img_url, "Not Image Link"  # url有问题，不重试
        else:
            return False, img_url, "Network Response Failed"  # 响应失败，重试
    # 异常发生, 分类处理
    # 观察后续记录，如有常见异常再进行分类处理
    # except requests.exceptions.RequestException as e:
    # 注释一: 占位图可能因某些原因导致网络请求异常，所以暂时注释掉RequestException的情况，避免因占位图引起的不必要的下载失败
    # 后续可能引入图像特征识别来识别“默认封面图”，或者找到更好的解决思路，届时RequestException的分支可以再打开
    #     error_msg = traceback.format_exc()
    #     print(f"[is_valid_image] 网络请求异常: {img_url}:\n{error_msg}\n")
    #     return False, img_url, "Network Exception"
    except Exception as e:
        error_msg = traceback.format_exc()
        exception_reason = f"Unhandled Exception: {type(e).__name__} - {str(e)}"
        exception_type = exception_reason.split(" - ")[0].replace(
            "Unhandled Exception: ", ""
        )
        with open(
            context.img_not_valid_unhandled_exception_log_path, "a", encoding="utf-8"
        ) as log:
            json.dump(
                {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "url": img_url,
                    "error": exception_reason,
                    "异常类型": exception_type,
                    "error_msg": error_msg,
                },
                log,
                ensure_ascii=False,
            )
            log.write("\n")
        print(f"[is_valid_image] 未知错误: {img_url}: {exception_reason}")
        return False, img_url, exception_reason


# 接收清洗过的URL下载图片
def download_image(img_url, save_path, max_retries=3):
    try:
        # 配置 Session 和重试机制
        session = requests.Session()
        retries = Retry(
            total=max_retries,
            backoff_factor=1,  # 等待时间：1s, 2s, 4s...
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET"],
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        response = session.get(img_url, timeout=5)
        with open(save_path, "wb") as f:
            f.write(response.content)
        return True, "OK", "OK"
    except Exception as e:
        error_msg = traceback.format_exc()
        exception_reason = f"Error downloading: {type(e).__name__} - {str(e)}"
        print(
            f"Error downloading{save_path}, {img_url}: {exception_reason}"
        )  # 加了save_path帮助验证是哪张图片
        return False, exception_reason, error_msg  # 下载失败当然要重试
    # 下载函数增加第二个返回值用于增加第二次下载失败的原因，这里整个流程可能还要改，等会儿再加


# sanitize_filename 标题清洗
def sanitize_filename(title: str, max_length: int) -> str:
    # 移除非法字符，保留常用汉字、字母、数字、空格、连字符和下划线
    title = re.sub(r'[\\/*?:"<>|]', "", title)
    title = re.sub(r"\s+", "_", title)  # 将空格换成下划线
    return title.strip()[:max_length]


def process_image(
    img_url, title, price, author, page, idx, img_validation_fail_list, context
):
    total_num_of_retry = 3

    # 第一次img是否有效判断
    is_valid, new_img_url, not_valid_reason = is_valid_image(img_url, context)
    # 标题清洗方便将标题加入图片命名确保图片命名唯一性
    safe_title = sanitize_filename(title, TITLE_MAX_LENGTH)
    img_filename = f"{safe_title}_page{page}_{idx}.jpg"
    img_path = context.images_dir / img_filename
    img_status = None
    # 第一次判断为图片有效，进入图片第一次下载流程
    if is_valid:
        success, download_fail_reason, error_msg = download_image(new_img_url, img_path)
        if success:
            img_status = os.path.basename(img_path)
        else:
            exception_type = download_fail_reason.split(" - ")[0].replace(
                "Error downloading: ", ""
            )
            print("图片下载失败，即将加入first_fail_list")
            img_status = "下载失败"  # 加入下载状态变量
            first_download_fail_list.append(
                {
                    "标题": title,
                    "价格": price,
                    "作者": author,
                    "封面图链接": new_img_url,
                    "封面图路径": str(img_path),
                    "失败原因": download_fail_reason,
                    "异常类型": exception_type,
                    "错误信息": error_msg,
                    "重试次数": 1,
                }
            )  # 下载失败的图片加入first_fail_list
            img_path = "无图片"

    # 第一次判断为图片无效，个别图片进入第二次是否有效判断流程
    else:
        # 确定为无效图的图片，进行相应标记
        if not_valid_reason not in ["Network Response Failed", "Incomplete Image"]:
            # if not_valid_reason not in ["Network Response Failed", "Network Exception", "Incomplete Image"]:    # 见注释一
            print(f"{img_path}: {new_img_url}为无图片或占位图")
            img_status = "无图片或占位图"
            img_path = "无图片"

            # 因网络响应超时和图片加载不全判定为无效图片的，进入第二次是否有效判断流程
        else:
            for num_of_retry in range(
                1, total_num_of_retry + 1
            ):  # 是否为无效图的判断最多循环3次
                print(
                    f"img URL is not valid, not_valid_reason: {not_valid_reason}，即将进行第{num_of_retry}次是否有效图判断重试"
                )
                # ========================加入二次判断流程===============================
                is_valid, new_img_url, not_valid_reason = is_valid_image(
                    img_url, context
                )  # 理论上这里应该简化判断流程
                # 经重试判断为有效的图片，进入下载图片流程
                if is_valid:
                    success, download_fail_reason, error_msg = download_image(
                        new_img_url, img_path
                    )
                    if success:
                        img_status = os.path.basename(img_path)
                    else:
                        exception_type = download_fail_reason.split(" - ")[0].replace(
                            "Error downloading: ", ""
                        )
                        print("图片下载失败，即将加入first_fail_list")
                        img_status = "下载失败"
                        first_download_fail_list.append(
                            {
                                "标题": title,
                                "价格": price,
                                "作者": author,
                                "封面图链接": new_img_url,
                                "封面图路径": str(img_path),
                                "失败原因": download_fail_reason,
                                "异常类型": exception_type,
                                "错误信息": error_msg,
                                "重试次数": 1,
                            }
                        )  # 下载失败的图片加入first_fail_list
                        img_path = "无图片"
                    break  # 一旦判定为有效图片，立即退出循环

                # 经重试判断为无效的图片，将img_status标记为reason
                # 这里是不是需要判定一下重试次数，确保的是，3次之后，仍然是因为网络响应超时和图片加载不全而被判无效的图片
                # status要标记为reason，因为其他情况不需要特殊标记
                else:
                    # 确定为无效图的图片，进行相应标记
                    if not_valid_reason not in [
                        "Network Response Failed",
                        "Incomplete Image",
                    ]:
                        # if not_valid_reason not in ["Network Response Failed", "Network Exception", "Incomplete Image"]:    # 见注释一
                        print(f"{img_path}: {new_img_url}为无图片或占位图")
                        img_status = "无图片或占位图"
                        img_path = "无图片"
                        break  # 一旦判定为无效图片，立即退出循环
                    else:
                        print(
                            f"{img_path}: {new_img_url}第{num_of_retry}次重试后仍因{not_valid_reason}判定为无效图"
                        )
                        # 当失败原因仍然为网络响应失败和图片加载不全时，记录无效图片日志
                        with open(
                            context.img_not_valid_retry_log_path, "a", encoding="utf-8"
                        ) as log:
                            json.dump(
                                {
                                    "timestamp": datetime.now().strftime(
                                        "%Y-%m-%d %H:%M:%S"
                                    ),
                                    "url": new_img_url,
                                    "图片无效重试次数": num_of_retry,
                                    "图片无效原因": not_valid_reason,
                                },
                                log,
                                ensure_ascii=False,
                            )
                            log.write("\n")
                        # 若循环3次仍因为网络响应失败和图片加载不全而被判定为无效，那么该图片暂时被记录并延后确认是否进行统一的重试等
                        if num_of_retry == total_num_of_retry:
                            img_status = f"{not_valid_reason}"  # 最终对Excel中标记为reason的图将单独的考虑
                            img_path = "无图片"
                            img_validation_fail_list.append(
                                {
                                    "标题": title,
                                    "价格": price,
                                    "作者": author,
                                    "封面图链接": new_img_url,
                                    "图片是否有效判断失败原因": not_valid_reason,
                                    "重试次数": num_of_retry,
                                }
                            )  # 最终图片是否有效判定失败的图片加入img_validation_fail_list

    return img_status, img_path


def final_download_for_fail_img(all_pages_data):
    # 二次下载图片
    if len(first_download_fail_list):
        print("开始图片二次下载")
        for item in first_download_fail_list:
            success, second_download_fail_reason, error_msg = download_image(
                item["封面图链接"], item["封面图路径"]
            )
            if success:
                img_status = os.path.basename(item["封面图路径"])
                # 定位到对应的位置，更改封面图文件名和封面图路径
                # 如果用all_pages_data就要在保存进Excel之前，或者可以在这里打开'dangdang_books.xlsx'再操作，这里先用all_pages_data来操作
                for page_data in all_pages_data:
                    for entry in page_data:
                        if entry["标题"] == item["标题"]:
                            entry["封面图文件名"] = img_status
                            entry["封面图路径"] = item["封面图路径"]
                            break
            else:
                exception_type = second_download_fail_reason.split(" - ")[0].replace(
                    "Error downloading: ", ""
                )
                print(f"{item['封面图链接']}图片二次下载失败，即将存入失败汇总页")
                # 内外都是双引号会报错——必须改成 item['封面图链接']
                second_download_fail_list.append(
                    {
                        "标题": item["标题"],
                        "价格": item["价格"],
                        "作者": item["作者"],
                        "封面图文件名": os.path.basename(item["封面图路径"]),
                        "封面图路径": str(item["封面图路径"]),
                        "第一次失败原因": item["失败原因"],
                        "第一次异常类型": item["异常类型"],
                        "第一次错误信息": item["错误信息"],
                        "第二次失败原因": second_download_fail_reason,
                        "第二次异常类型": exception_type,
                        "第二次错误信息": error_msg,
                    }
                )  # 下载失败的图片加入second_fail_list
    return second_download_fail_list
