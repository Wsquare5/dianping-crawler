from DrissionPage import ChromiumPage

class VersionHandler:
    def __init__(self, page):
        # 接收已创建的page对象而不是创建新的
        self.page = page
        
    def is_new_version(self):
        """检查是否是新版页面"""
        try:
            # 检查是否存在新版特有的提示文本
            notice = self.page.ele('css:.shopStatus')
            if notice and "进行PC网页改版" in notice.text:
                print("通过提示文本检测到新版页面")
                return True
            
            print("当前是旧版页面")
            return False
        except Exception as e:
            print(f"检查页面版本时发生错误: {e}")
            return False
            
    def switch_to_old_version(self):
        """切换到旧版"""
        try:
            if not self.is_new_version():
                print("当前已经是旧版页面")
                return True
            
            old_version = self.page.ele('xpath://div[@class="pc-sidebar-icon wx-view" and contains(text(), "返回旧版")]')
            if old_version:
                old_version.click()
                self.page.wait.load_start()
                print("成功切换到旧版")
                return True
            else:
                print("未找到返回旧版按钮")
                return False
                
        except Exception as e:
            print(f"切换版本时发生错误: {e}")
            return False