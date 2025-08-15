# 数据存储封装
# ===== 标准库模块 =====
import json
from pathlib import Path

# ===== 第三方库 =====
import pandas as pd

# ===== 项目自定义模块 =====
# from mymodule import myfunction


def create_file():
    # 当前文件的路径（src/scraper.py）
    current_file = Path(__file__).resolve()
    # 项目根目录（即 src 的上一级）
    project_root = current_file.parent.parent
    # 输出文件夹：output（在项目根目录下）
    output_dir = project_root / "output"
    images_dir = output_dir / "images"
    excel_path = output_dir / "dangdang_books.xlsx"
    # 创建 output 和 images 文件夹
    images_dir.mkdir(parents=True, exist_ok=True)
    # 开发日志路径
    dev_log_dir = project_root / "dev_logs"
    debug_log_dir = dev_log_dir / "debug_logs"
    debug_log_dir.mkdir(parents=True, exist_ok=True)
    # # 日志路径
    img_not_valid_retry_log_path = debug_log_dir / "img_not_valid_retry.json"
    img_not_valid_unhandled_exception_log_path = (
        debug_log_dir / "img_not_valid_unhandled_exception.json"
    )
    parsing_error_log_path = debug_log_dir / "parsing_error.json"
    img_validation_failures_log_path = dev_log_dir / "img_validation_failures.json"
    download_img_failures_log_path = dev_log_dir / "download_img_failures.json"

    return (
        images_dir,
        excel_path,
        img_not_valid_retry_log_path,
        img_not_valid_unhandled_exception_log_path,
        parsing_error_log_path,
        img_validation_failures_log_path,
        download_img_failures_log_path,
    )


def save_info(
    all_pages_data, second_download_fail_list, img_validation_fail_list, context
):
    # 分页存入 Excel
    with pd.ExcelWriter(context.excel_path) as writer:
        for i, page_data in enumerate(all_pages_data, start=1):
            df = pd.DataFrame(page_data)
            df.to_excel(writer, sheet_name=f"第{i}页", index=False)

        # 判断是否存在second_fail_list需要保存，存在即保存
        if len(second_download_fail_list):
            df_fail = pd.DataFrame(second_download_fail_list)
            df_fail.to_excel(writer, sheet_name=f"失败汇总页", index=False)

    # 判断图片是否有效地失败记录
    if len(img_validation_fail_list):
        with open(context.img_validation_failures_log_path, "w", encoding="utf-8") as f:
            # 将失败项写入json文件，方便后续读取文件进行重试等操作
            json.dump(img_validation_fail_list, f, ensure_ascii=False, indent=2)
        print(
            f"共有 {len(img_validation_fail_list)} 个封面图多次判断是否有效失败，已写入 Excel 与 JSON"
        )
    else:
        print("所有图片是否有效均判断成功，无失败项。")

    # 在所有下载图片失败都处理完之后执行
    if len(second_download_fail_list):
        with open(context.download_img_failures_log_path, "w", encoding="utf-8") as f:
            # 将失败项写入json文件，方便后续读取文件进行重试等操作
            json.dump(second_download_fail_list, f, ensure_ascii=False, indent=2)
        print(
            f"共有 {len(second_download_fail_list)} 个封面图二次下载失败，已写入 Excel 与 JSON"
        )
    else:
        print("所有图片均下载成功，无失败项。")
