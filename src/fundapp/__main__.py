import threading
import sys
import os
import toga
from toga.style import Pack
from flask import Flask

# 修复路径问题，确保能找到原来的代码
sys.path.append(os.path.dirname(__file__))

# 尝试导入原本的网页服务
try:
    from fund_server import app as flask_app
except ImportError:
    # 就算出错了，也弄个假 App 防止闪退
    flask_app = Flask(__name__)
    @flask_app.route('/')
    def index():
        return "启动出错了，请检查代码"

class FundApp(toga.App):
    def startup(self):
        # 创建一个全屏窗口
        self.main_window = toga.MainWindow(title=self.formal_name)
        # 创建一个浏览器组件
        self.webview = toga.WebView(style=Pack(flex=1))
        # 指向刚才启动的 Flask 网页
        self.webview.url = 'http://127.0.0.1:8311/fund'
        
        self.main_window.content = self.webview
        self.main_window.show()
        
        # 在后台偷偷启动 Flask 网页服务
        threading.Thread(target=self.run_flask, daemon=True).start()

    def run_flask(self):
        # 强制运行在 8311 端口
        flask_app.run(host='127.0.0.1', port=8311, debug=False, use_reloader=False)

def main():
    return FundApp()

if __name__ == '__main__':
    main().main_loop()
