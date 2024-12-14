from DrissionPage import ChromiumPage, Chromium
from DataRecorder import Recorder
from version_handler import VersionHandler

class DianPingCrawler:
    def __init__(self):
        self.page = ChromiumPage()
        self.version_handler = VersionHandler(self.page)
        self.recorder = Recorder('restaurants_data.csv') 
        self.recorder.set.head(('名称', '评价数量', '评分', '人均消费', 
                               '口味评分', '环境评分', '服务评分', '地址'))
        self.recorder.set.fit_head(True) 

    def crawl_restaurants(self, list_url):
        self.page.get(list_url)
        self.page.wait.load_start()

        # Get the restaurant list
        restaurants = self.page.eles('css:a > h4')
        for restaurant in restaurants:
            restaurant_name = restaurant.text
            print(f"Visiting restaurant: {restaurant_name}")
            restaurant.click()

            self.page.wait.load_start()
            details_page = self.page.latest_tab

            # Ensure using the old version
            self.version_handler = VersionHandler(details_page)
            self.version_handler.switch_to_old_version()

            # Get the restaurant information
            # Get the rating
            rating_element = details_page.ele('css:.star-wrapper .mid-score')
            # Get the review count
            review_count = details_page.ele('css:.brief-info #reviewCount').text
            review_count = int(review_count.replace('条评价', ''))  # 将"1157条评价"转换为1157

            # Get the average price
            avg_price = details_page.ele('#avgPriceTitle').text
            avg_price = int(avg_price.replace('人均：', '').replace('元', ''))  # 将"人均：209元"转换为209

            # Get the score details
            scores = details_page.eles('css:#comment_score .item')
            taste_score = float(scores[0].text.replace('口味：', ''))  # 4.4
            environment_score = float(scores[1].text.replace('环境：', ''))  # 4.6
            service_score = float(scores[2].text.replace('服务：', ''))  # 4.3

            # Get the address
            address = details_page.ele('css:span#address').text

            # Store all information in a dictionary
            self.recorder.add_data([
                    restaurant_name,
                    review_count,
                    float(rating_element.text),
                    avg_price,
                    taste_score,
                    environment_score,
                    service_score,
                    address
                ])
            print(f"已获取餐厅 {restaurant_name} 的信息")

            details_page.close()


        self.recorder.record()
        print("\nAll data has been successfully written to the CSV file")


        
def main():
    crawler = DianPingCrawler()
    
    try:
        # Visit the restaurant list page
        list_url = "https://www.dianping.com/dongguan/ch10"  # Fill in the URL you want to crawl
        crawler.crawl_restaurants(list_url)
    finally:
        print("爬取完成")


if __name__ == "__main__":
    main()