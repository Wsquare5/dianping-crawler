from DrissionPage import ChromiumPage, Chromium



# # 1. 先检查弹窗是否存在
# def check_popup(page):
#     # 检查整个弹窗容器是否存在
#     popup = page.ele('css:.oap-wide')
#     if popup and popup.attr('style') == 'display: block':  # 确认弹窗是显示状态
#         print("检测到弹窗")
#         return True
#     return False

# # 2. 尝试关闭弹窗
# def close_popup(page):
#     try:
#         # 等待弹窗显示
#         page.wait.ele_displayed('css:.oap-wide', timeout=5)
        
#         # 定位关闭按钮
#         close_button = page.ele('css:.oap-close')
#         if close_button:
#             # 尝试点击关闭按钮
#             close_button.click(by_js=True)
#             print("成功关闭弹窗")
#             return True
#         else:
#             print("找到弹窗但未找到关闭按钮")
#             return False
#     except Exception as e:
#         print(f"关闭弹窗时发生错误: {e}")
#         return False



# # 创建浏览器对象

# page = ChromiumPage()

# # 访问页面
# page.get("https://www.dianping.com/shop/G6eh45csfj9DbYiO")

# page.wait.load_start()

# close_button = page.ele('css:.oap-close')
# print(close_button)


class DianPingBrowser:
    def __init__(self):
        self.page = ChromiumPage()
    
        
    def _check_popup(self):
        """检查是否有弹窗"""
        try:
            print("开始检查弹窗...")
            
            # 等待页面加载
            self.page.wait.load_start()
            
            # 尝试获取弹窗元素
            popup = self.page.ele('css:.oap-wide')
            print("弹窗元素:", popup)
            
            if popup:
                style = popup.attr('style')
                print("弹窗style属性:", style)
                
                if style == 'display: block':
                    print("检测到显示的弹窗")
                    return True
                else:
                    print("弹窗存在但未显示")
                    return False
            else:
                print("未找到弹窗元素")
                return False
                
        except Exception as e:
            print(f"检查弹窗时出错: {e}")
            return False
            
    def _close_popup(self):
        """尝试多种方式关闭弹窗"""
        try:
            # 等待关闭按钮出现
            self.page.wait.ele_displayed('css:.oap-close', timeout=5)
            close_btn = self.page.ele('css:.oap-close')
            
            if close_btn:
                print("找到关闭按钮，尝试点击...")
                
                # 方式1：普通点击
                try:
                    close_btn.click()
                    print("普通点击尝试完成")
                except:
                    print("普通点击失败")
                
                # 方式2：JS点击
                try:
                    close_btn.click(by_js=True)
                    print("JS点击尝试完成")
                except:
                    print("JS点击失败")
                
                # 等待一下看是否关闭成功
                self.page.wait.load_start()
                
                # 检查弹窗是否还在
                if not self._check_popup():
                    print("弹窗已成功关闭")
                    return True
                else:
                    print("弹窗���然存在")
                    return False
            else:
                print("未找到关闭按钮")
                return False
                
        except Exception as e:
            print(f"关闭弹窗时出错: {e}")
            return False

# 测试代码
def test_popup():
    print("开始测试...")
    browser = DianPingBrowser()
    
    print("\n访问页面...")
    browser.page.get("https://www.dianping.com/shop/lal3H9FN9WxJUldB")
    browser.page.wait.load_start()
    
    print("\n检查页面源码...")
    print(browser.page.html)  # 打印页面源码
    
    print("\n检查弹窗...")
    if browser._check_popup():
        print("找到弹窗，尝试关闭...")
        browser._close_popup()
    else:
        print("没有检测到弹窗")

if __name__ == "__main__":
    test_popup()









