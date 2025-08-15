# 主流程控制
# ===== 标准库模块 =====

# ===== 第三方库 =====

# ===== 项目自定义模块 =====
# from mymodule import myfunction
import context as ctx_mod
import image_process as img_pro
import parse_module as parse_m
import request_module as req_m
import storage_module as sto_m

# ===== 文件夹及文件路径创建 =====
context = ctx_mod.create_context()
# ===== 浏览器操作获取搜索图书页面 =====
driver = req_m.open_search_page("AI", "https://www.dangdang.com/")
# ===== 进入数据获取主流程 =====
all_pages_data, img_validation_fail_list = parse_m.parse_product(driver, context)
# 下载失败的图片统一进行二次下载
second_download_fail_list = img_pro.final_download_for_fail_img(all_pages_data)
# ===== 关闭浏览器 =====
req_m.driver_quit(driver)
# ===== 数据及信息存储 =====
sto_m.save_info(
    all_pages_data, second_download_fail_list, img_validation_fail_list, context
)
# ===== 任务完成输出 =====
print("抓取与保存完成。")
