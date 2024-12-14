from DrissionPage import ChromiumPage
import time
from selenium.webdriver.chrome.options import Options
import random
import pandas as pd
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.common.by import By

# 设置浏览器选项
def set_chromium_options():
    options = Options()
    options.add_argument('--remote-debugging-port=9222')  # 开启调试端口
    options.add_argument('--headless=false')  # 禁用无头模式，确保浏览器界面弹出
    return options


# 爬取餐厅列表页面的函数
def get_all_restaurants_on_page(page, base_url):
    # 访问首页，获取所有餐厅的链接
    page.get(base_url)

    #  # 使用显式等待，等待页面加载完成，直到某个元素出现
    # WebDriverWait(page.driver, 20).until(
    #     EC.presence_of_element_located((By.CSS_SELECTOR, 'div.pic a'))  # 选择合适的元素，等待它加载完成
    # )
    time.sleep(random.uniform(15, 20))  # 模拟人类行为，随机等待

    # 确认网页已登录
    if not is_logged_in(page):
        print("Please login first!")
        return []

    # 提取餐厅链接
    restaurant_links = page.eles('div.pic a')  # 选择所有餐厅链接的元素
    links = [link.get_attribute('href') for link in restaurant_links 
             if link.attr('href').startswith("https://www.dianping.com/shop/")]  # 获取链接地址

    # 对每个餐厅链接提取详情
    all_restaurant_details = []
    for link in links:
        details = get_restaurant_details(link)
        all_restaurant_details.append(details)
    
    return all_restaurant_details

# 确认网页是否已登录的函数
def is_logged_in(page):
    try:
        # 判断网页是否显示登录后的特定元素
        # 假设在已登录时会有一个 <a class="item left-split username J-user-trigger"> 的元素
        login_element = page.eles('a.username.J-user-trigger')
        if login_element:
            return True
        else:
            return False
    except Exception as e:
        print(f"Error checking login status: {e}")
        return False

# 爬取餐厅详情页面的函数
def get_restaurant_details(page_url):
    page = ChromiumPage()
    # 访问页面
    page.get(page_url)
    time.sleep(random.uniform(2, 5))  # 模拟人类行为，随机等待

    # 提取信息
    category = page.eles('div.breadcrumb a')[1].text  # 小吃快餐
    district = page.eles('div.breadcrumb a')[2].text  # 莞城街道
    sub_district = page.eles('div.breadcrumb a')[3].text  # 下坝坊
    restaurant_name = page.eles('div.breadcrumb span')[0].text  # UNO·一弄·家庭料理与咖啡

    rating = page.eles('div.star-wrapper .mid-score')[0].text  # 评分 4.1
    avg_price = page.eles('span#avgPriceTitle')[0].text  # 人均价格 46元

    taste_score = page.eles('span#comment_score .item')[0].text.split('：')[1]  # 口味 4.1
    environment_score = page.eles('span#comment_score .item')[1].text.split('：')[1]  # 环境 4.4
    service_score = page.eles('span#comment_score .item')[2].text.split('：')[1]  # 服务 4.3

    address = page.eles('div#J_map-show #address')[0].text  # 地址

    # 返回所有提取的值
    return {
        "category": category,
        "district": district,
        "sub_district": sub_district,
        "restaurant_name": restaurant_name,
        "rating": rating,
        "avg_price": avg_price,
        "taste_score": taste_score,
        "environment_score": environment_score,
        "service_score": service_score,
        "address": address
    }

def save_to_excel(data, file_name):
    # 将数据保存到Excel
    df = pd.DataFrame(data)
    df.to_excel(file_name, index=False)
    print(f"Data saved to {file_name}")

# 主函数
def main():
    # 创建 DrissionPage 实例
    page = ChromiumPage()

    # 设置首页 URL（可更换为实际的首页链接）
    base_url = "https://www.dianping.com/dongguan/ch10"

    # 获取所有餐厅的详细信息
    all_restaurant_details = get_all_restaurants_on_page(page, base_url)

    # 保存到 Excel 文件
    if all_restaurant_details:
        save_to_excel(all_restaurant_details, "restaurants_details.xlsx")
    else:
        print("No data to save.")

if __name__ == "__main__":
    main()
