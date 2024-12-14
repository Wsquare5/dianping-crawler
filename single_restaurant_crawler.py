from DrissionPage import ChromiumPage
from DataRecorder import Recorder
from version_handler import VersionHandler

class DianPingCrawler:
    def __init__(self):
        self.page = ChromiumPage()
        self.version_handler = VersionHandler(self.page)
        # 创建 Recorder 对象，设置表头
        self.recorder = Recorder('single_restaurant.csv')
        self.recorder.set.head(('名称', '评价数量', '地址', '评分', '人均消费', 
                               '口味评分', '环境评分', '服务评分',
    '菜系', '区域', '商圈', 'shop_uuid' ))
        self.recorder.set.fit_head(True) 

    def get_categories(self, details_page):
        try:
            # 通过 breadcrumb 类定位导航栏
            breadcrumb = details_page.ele('css:.breadcrumb')
            
            # 获取所有分类链接
            categories = breadcrumb.eles('tag:a')
            
            # 提取需要的分类（第2、3、4个元素，对应粤菜、虎门镇、威远）
            # 索引1、2、3对应第2、3、4个元素
            cuisine = categories[1].text if len(categories) > 1 else ''  # 粤菜
            district = categories[2].text if len(categories) > 2 else ''  # 虎门镇
            area = categories[3].text if len(categories) > 3 else ''  # 威远
            
            print(f"获取到分类信息：菜系-{cuisine}, 区域-{district}, 商圈-{area}")  # 调试信息
            
            return {
                'cuisine': cuisine,
                'district': district,
                    'area': area
                }
        except Exception as e:
            print(f"获取分类信息时发生错误: {e}")
            return {
                    'cuisine': '',
                    'district': '',
                    'area': ''
                }

    def crawl_single_restaurant(self, restaurant_url):
        try:
            # 访问餐厅页面
            self.page.get(restaurant_url)
            self.page.wait.load_start()

            # 确保使用旧版
            self.version_handler.switch_to_old_version()

            # 获取餐厅信息
            name = self.page.ele('css:h1.shop-name').text

            # 获取 shop_uuid
            details_url = self.page.url
            shop_uuid = details_url[-16:] if len(details_url) >= 16 else ''


            # 获取分类信息
            categories = self.get_categories(self.page)
            
            # 获取评分
            rating_element = self.page.ele('css:.star-wrapper .mid-score')
            
            # 获取评价数量
            review_count = self.page.ele('css:.brief-info #reviewCount').text
            review_count = int(review_count.replace('条评价', ''))

            # 获取人均消费
            avg_price = self.page.ele('#avgPriceTitle').text
            avg_price = int(avg_price.replace('人均：', '').replace('元', ''))

            # 获取评分详情
            scores = self.page.eles('css:#comment_score .item')
            taste_score = float(scores[0].text.replace('口味：', ''))
            environment_score = float(scores[1].text.replace('环境：', ''))
            service_score = float(scores[2].text.replace('服务：', ''))

            # 获取地址
            address = self.page.ele('css:span#address').text

            # 将所有信息存入字典
            restaurant_info = {
                'name': name,
                'review_count': review_count,
                'rating': float(rating_element.text),
                'avg_price': avg_price,
                'taste_score': taste_score,
                'environment_score': environment_score,
                'service_score': service_score,
                'cuisine': categories['cuisine'],      # 添加菜系
                'district': categories['district'],     # 添加区域
                'area': categories['area'], 
                'address': address
            }

            # 记录数据到 CSV
            self.recorder.add_data([
                name,
                review_count,
                address,
                float(rating_element.text),
                avg_price,
                taste_score,
                environment_score,
                service_score,
                categories['cuisine'],
                categories['district'],
                categories['area'],
                shop_uuid
            ])
            print("已获取餐厅信息：", restaurant_info)
            
            # 写入数据
            self.recorder.record()
            print("数据已成功写入 CSV 文件")

        except Exception as e:
            print(f"爬取过程中发生错误: {e}")


def main():
    crawler = DianPingCrawler()
    
    # 这里填入一个具体餐厅的 URL
    restaurant_url = "https://www.dianping.com/shop/k6y5M4wFpOcyMRNj"  # 替换为实际的餐厅URL
    crawler.crawl_single_restaurant(restaurant_url)


if __name__ == "__main__":
    main()
