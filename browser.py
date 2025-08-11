from PyQt5.QtWidgets import (QApplication, QMainWindow, QTabWidget, QLineEdit, 
                            QToolBar, QAction, QMenu, QStyle)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5.QtCore import QUrl, Qt, QSettings
from PyQt5.QtGui import QIcon, QColor
import sys
import json
from datetime import datetime

class BrowserTab(QWebEngineView):
    def __init__(self, parent=None, private=False):
        super().__init__(parent)
        self.parent = parent
        self.private = private
        self.history = []
        self.current_history_index = -1

    def createWindow(self, windowType):
        if windowType == QWebEngineView.WebBrowserTab:
            return self.parent.add_new_tab(private=self.private)
        return super().createWindow(windowType)
    
    def add_to_history(self, url):
        if self.private:
            return
            
        history_entry = {
            'url': url.toString(),
            'title': self.title(),
            'timestamp': datetime.now().isoformat()
        }
        
        if self.current_history_index < len(self.history) - 1:
            self.history = self.history[:self.current_history_index + 1]
        
        self.history.append(history_entry)
        self.current_history_index = len(self.history) - 1
        
    def title(self):
        return self.page().title() if self.page() else "Yeni Sekme"

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tarayıcı")
        self.resize(1024, 768)
        
        self.settings = QSettings("MyBrowser", "BrowserApp")
        self.dark_mode = self.settings.value("dark_mode", False, type=bool)
        
        self.history_data = []
        self.load_history()
        
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.setDocumentMode(True)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.setCentralWidget(self.tabs)
        
        self.apply_dark_mode()
        self.create_toolbar()
        
        profile = QWebEngineProfile.defaultProfile()
        profile.setPersistentCookiesPolicy(QWebEngineProfile.ForcePersistentCookies)
        
        self.add_new_tab(QUrl("https://www.google.com"))
        
    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        menu_btn = QAction("☰", self)
        menu_btn.setMenu(self.create_main_menu())
        toolbar.addAction(menu_btn)
        
        back_btn = QAction(self.style().standardIcon(QStyle.SP_ArrowBack), "Geri", self)
        back_btn.triggered.connect(lambda: self.current_browser().back())
        toolbar.addAction(back_btn)
        
        forward_btn = QAction(self.style().standardIcon(QStyle.SP_ArrowForward), "İleri", self)
        forward_btn.triggered.connect(lambda: self.current_browser().forward())
        toolbar.addAction(forward_btn)
        
        reload_btn = QAction(self.style().standardIcon(QStyle.SP_BrowserReload), "Yenile", self)
        reload_btn.triggered.connect(lambda: self.current_browser().reload())
        toolbar.addAction(reload_btn)
        
        home_btn = QAction(self.style().standardIcon(QStyle.SP_ComputerIcon), "Ana Sayfa", self)
        home_btn.triggered.connect(self.navigate_home)
        toolbar.addAction(home_btn)
        
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        toolbar.addWidget(self.url_bar)
        
        new_tab_btn = QAction("+", self)
        new_tab_btn.triggered.connect(lambda: self.add_new_tab())
        toolbar.addAction(new_tab_btn)
        
        private_tab_btn = QAction(QIcon.fromTheme("private-browsing"), "Gizli", self)
        private_tab_btn.triggered.connect(lambda: self.add_new_tab(private=True))
        toolbar.addAction(private_tab_btn)
    
    def create_main_menu(self):
        menu = QMenu(self)
        
        history_menu = menu.addMenu("Geçmiş")
        for item in reversed(self.history_data[-10:]):
            action = QAction(item['title'], self)
            action.setData(item['url'])
            action.triggered.connect(lambda _, url=item['url']: self.navigate_to_history(url))
            history_menu.addAction(action)
        
        dark_mode_action = QAction("Dark Mode", self, checkable=True)
        dark_mode_action.setChecked(self.dark_mode)
        dark_mode_action.triggered.connect(self.toggle_dark_mode)
        menu.addAction(dark_mode_action)
        
        clear_history = QAction("Geçmişi Temizle", self)
        clear_history.triggered.connect(self.clear_history)
        menu.addAction(clear_history)
        
        return menu
    
    def add_new_tab(self, url=None, private=False):
        if url is None:
            url = QUrl("https://www.google.com")
        
        browser = BrowserTab(self, private)
        browser.setUrl(url)
        
        tab_title = "Gizli Sekme" if private else "Yeni Sekme"
        i = self.tabs.addTab(browser, tab_title)
        
        if private:
            self.tabs.tabBar().setTabTextColor(i, QColor(150, 150, 150))
        
        self.tabs.setCurrentIndex(i)
        
        browser.urlChanged.connect(lambda url, browser=browser: 
            self.update_urlbar(url, browser))
        
        browser.loadFinished.connect(lambda success, i=i, browser=browser: (
            self.on_page_loaded(success, i, browser),
            self.inject_dark_mode_css(browser) if self.dark_mode else None
        ))
    
    def on_page_loaded(self, success, tab_index, browser):
        if success:
            title = browser.title()
            self.tabs.setTabText(tab_index, title[:15] + "..." if len(title) > 15 else title)
            
            if not browser.private:
                browser.add_to_history(browser.url())
                self.add_to_global_history(browser.url().toString(), title)
    
    def inject_dark_mode_css(self, browser):
        dark_mode_css = """
            html, body {
                background-color: #1e1e1e !important;
                color: #ffffff !important;
            }
            a { color: #4e9af1 !important; }
            img, video {
                filter: brightness(0.8) contrast(1.2);
            }
        """
        browser.page().runJavaScript(f"""
            (function() {{
                var style = document.createElement('style');
                style.innerHTML = `{dark_mode_css}`;
                document.head.appendChild(style);
            }})();
        """)
    
    def close_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)
    
    def current_browser(self):
        return self.tabs.currentWidget()
    
    def current_tab_changed(self, i):
        if i != -1:
            browser = self.tabs.widget(i)
            if browser:
                self.update_urlbar(browser.url(), browser)
    
    def update_urlbar(self, url, browser=None):
        if browser != self.current_browser():
            return
        self.url_bar.setText(url.toString())
        self.url_bar.setCursorPosition(0)
    
    def navigate_to_url(self):
        url_text = self.url_bar.text()
        if not url_text.startswith(("http://", "https://")):
            url_text = "http://" + url_text
        self.current_browser().setUrl(QUrl(url_text))
    
    def navigate_to_history(self, url):
        self.add_new_tab(QUrl(url))
    
    def navigate_home(self):
        self.current_browser().setUrl(QUrl("https://www.google.com"))
    
    def add_to_global_history(self, url, title):
        history_entry = {
            'url': url,
            'title': title,
            'timestamp': datetime.now().isoformat()
        }
        self.history_data.append(history_entry)
        self.save_history()
    
    def save_history(self):
        self.settings.setValue("history", json.dumps(self.history_data[-100:]))
    
    def load_history(self):
        history_json = self.settings.value("history", "[]")
        self.history_data = json.loads(history_json)
    
    def clear_history(self):
        self.history_data = []
        self.save_history()
    
    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode
        self.settings.setValue("dark_mode", self.dark_mode)
        self.apply_dark_mode()
        
        for i in range(self.tabs.count()):
            browser = self.tabs.widget(i)
            if browser:
                if self.dark_mode:
                    self.inject_dark_mode_css(browser)
    
    def apply_dark_mode(self):
        if self.dark_mode:
            self.setStyleSheet("""
                QMainWindow, QToolBar, QTabWidget::pane, QMenu {
                    background-color: #2d2d2d;
                    color: #ffffff;
                    border: none;
                }
                QLineEdit {
                    background-color: #3d3d3d;
                    color: #ffffff;
                    border: 1px solid #555;
                    padding: 5px;
                }
                QTabBar::tab {
                    background-color: #3d3d3d;
                    color: #ffffff;
                    padding: 8px;
                    border: 1px solid #555;
                    border-bottom: none;
                }
                QTabBar::tab:selected {
                    background-color: #1d1d1d;
                }
            """)
        else:
            self.setStyleSheet("")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = Browser()
    browser.show()
    sys.exit(app.exec_())
