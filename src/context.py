from dataclasses import dataclass
from typing import List

import storage_module as sto_m


@dataclass
class Context:
    images_dir: str
    excel_path: str
    img_not_valid_retry_log_path: str
    img_not_valid_unhandled_exception_log_path: str
    parsing_error_log_path: str
    img_validation_failures_log_path: str
    download_img_failures_log_path: str
    img_validation_fail_list: List
    second_download_fail_list: List


def create_context() -> Context:
    (
        images_dir,
        excel_path,
        img_not_valid_retry_log_path,
        img_not_valid_unhandled_exception_log_path,
        parsing_error_log_path,
        img_validation_failures_log_path,
        download_img_failures_log_path,
    ) = sto_m.create_file()

    return Context(
        images_dir=images_dir,
        excel_path=excel_path,
        img_not_valid_retry_log_path=img_not_valid_retry_log_path,
        img_not_valid_unhandled_exception_log_path=img_not_valid_unhandled_exception_log_path,
        parsing_error_log_path=parsing_error_log_path,
        img_validation_failures_log_path=img_validation_failures_log_path,
        download_img_failures_log_path=download_img_failures_log_path,
        img_validation_fail_list=[],
        second_download_fail_list=[],
    )
