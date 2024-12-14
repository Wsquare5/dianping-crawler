from DrissionPage import ChromiumPage, Chromium
from DataRecorder import Recorder
from version_handler import VersionHandler

class DianPingCrawler:
    def __init__(self):
        self.page = ChromiumPage()
        self.version_handler = VersionHandler(self.page)
        


def main():
    crawler = DianPingCrawler()
    
    # 访问餐厅列表页
    list_url = "https://www.dianping.com/dongguan/ch10"
    crawler.page.get(list_url)
    crawler.page.wait.load_start()

    # 获取一家餐厅的信息
    restaurant = crawler.page.ele('css:a > h4')
    print(f"正在访问餐厅: {restaurant.text}")
    restaurant.click()
    
    crawler.page.wait.load_start()
    details_page = crawler.page.latest_tab
    
    # 确保使用旧版
    crawler.version_handler = VersionHandler(details_page)
    crawler.version_handler.switch_to_old_version()

    # 获取评分
    rating_element = details_page.ele('css:.star-wrapper .mid-score')
    # 获取评价数量
    review_count = details_page.ele('css:.brief-info #reviewCount').text
    review_count = int(review_count.replace('条评价', ''))  # 将"1157条评价"转换为1157

    # 获取人均消费
    avg_price = details_page.ele('#avgPriceTitle').text
    avg_price = int(avg_price.replace('人均：', '').replace('元', ''))  # 将"人均：209元"转换为209

    # 获取评分详情
    scores = details_page.eles('css:#comment_score .item')
    taste_score = float(scores[0].text.replace('口味：', ''))  # 4.4
    environment_score = float(scores[1].text.replace('环境：', ''))  # 4.6
    service_score = float(scores[2].text.replace('服务：', ''))  # 4.3

    # 将所有信息存入字典
    restaurant_info = {
        'name': restaurant.text,
        'review_count': review_count,  # 1157
        'address': details_page.ele('css:span#address').text,
        'rating': float(rating_element.text),
        'avg_price': avg_price,  # 209
        'taste_score': taste_score,  # 4.4
        'environment_score': environment_score,  # 4.6
        'service_score': service_score  # 4.3
    }

    print(restaurant_info)


if __name__ == "__main__":
    main()


# # 获取所有餐厅的链接
# restaurants = page.eles('css:a > h4') # <a>里面<h4>的元素是餐厅名称
# for restaurant in restaurants:
#     print(restaurant.text)

# # 遍历餐厅链接
# for restaurant in restaurants:
#     restaurant_name = restaurant.text
#     restaurant.click()  # 点击进入餐厅页面

#     # 在新页面获取信息
#     details_page = page.latest_tab

#     restaurant_info = {
#         'name': restaurant_name,
#         'address': details_page.ele('span.address').text or '无地址信息',
#         'rating': details_page.ele('span.rating').text or '无评分信息',
#         # 根据实际页面添加其他字段
#     }
#     print(restaurant_info)

#     details_page.back()
