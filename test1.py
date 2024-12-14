from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# 配置 Selenium 的 ChromeDriver
chrome_options = Options()
# chrome_options.add_argument("--headless")  # 如果需要显示浏览器界面，注释掉这一行
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# 设置 ChromeDriver 的路径
service = Service('/Applications/chromedriver-mac-arm64/chromedriver')  # 替换为你的 chromedriver 路径

# 启动浏览器
driver = webdriver.Chrome(service=service, options=chrome_options)

# 目标 URL
url = "https://www.dianping.com/dongguan/ch10"

try:
    # 打开页面
    driver.get(url)

    # 等待页面加载（根据需要调整时间）
    time.sleep(30)

    # 如果遇到验证码，手动完成或者可以集成打码平台处理
    print("请检查浏览器是否需要验证码。")

    # 提取餐馆信息
    restaurants = driver.find_elements(By.CSS_SELECTOR, 'div.tit h4')
    for restaurant in restaurants:
      print(restaurant.text)


except Exception as e:
    print(f"发生错误: {e}")

# finally:
#     # 关闭浏览器
#     driver.quit()
