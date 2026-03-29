# 陈大哥的理财账本 - Kivy 手机版
# 用于生成安卓 APK

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.metrics import dp
import json
import os
from datetime import datetime

# 数据文件路径
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'finance_data_v5.json')


class FinanceData:
    """数据管理类"""
    
    def __init__(self):
        self.data = []
        self.load_data()
    
    def load_data(self):
        """加载数据"""
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
        except Exception as e:
            print(f"加载数据失败：{e}")
            self.data = []
    
    def save_data(self):
        """保存数据"""
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存数据失败：{e}")
    
    def add_record(self, date, account, value):
        """添加记录"""
        self.data.append({
            "date": date,
            "account": account,
            "current_value": float(value)
        })
        self.save_data()
    
    def get_accounts(self):
        """获取所有账户"""
        accounts = set()
        for record in self.data:
            accounts.add(record["account"])
        return sorted(list(accounts))
    
    def get_latest_values(self):
        """获取每个账户的最新估值"""
        latest = {}
        for record in self.data:
            account = record["account"]
            if account not in latest or record["date"] > latest[account]["date"]:
                latest[account] = record
        return latest


class MainScreen(Screen):
    """主界面"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.finance_data = FinanceData()
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        # 标题
        title = Label(
            text="陈大哥的理财账本 📊",
            font_size=dp(24),
            size_hint=(1, 0.2)
        )
        
        # 总估值
        latest = self.finance_data.get_latest_values()
        total = sum(r["current_value"] for r in latest.values())
        lbl_total = Label(
            text=f"总估值：¥{total:,.0f}",
            font_size=dp(20),
            size_hint=(1, 0.1)
        )
        
        # 功能按钮
        btn_overview = Button(
            text="📊 账户总览",
            font_size=dp(18),
            size_hint=(1, 0.15)
        )
        btn_overview.bind(on_press=lambda x: self.go_to('overview'))
        
        btn_quick = Button(
            text="📝 快速录入",
            font_size=dp(18),
            size_hint=(1, 0.15)
        )
        btn_quick.bind(on_press=lambda x: self.go_to('quick_entry'))
        
        btn_batch = Button(
            text="📋 批量录入",
            font_size=dp(18),
            size_hint=(1, 0.15)
        )
        btn_batch.bind(on_press=lambda x: self.go_to('batch_entry'))
        
        btn_data = Button(
            text="💾 数据管理",
            font_size=dp(18),
            size_hint=(1, 0.15)
        )
        btn_data.bind(on_press=lambda x: self.go_to('data'))
        
        # 添加组件
        layout.add_widget(title)
        layout.add_widget(lbl_total)
        layout.add_widget(btn_overview)
        layout.add_widget(btn_quick)
        layout.add_widget(btn_batch)
        layout.add_widget(btn_data)
        
        self.add_widget(layout)
        self.screen_manager = None
    
    def go_to(self, screen_name):
        if self.screen_manager:
            self.screen_manager.current = screen_name


class OverviewScreen(Screen):
    """账户总览页"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.finance_data = FinanceData()
        
        layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(5))
        
        title = Label(text="📊 账户总览", font_size=dp(20), size_hint=(1, 0.1))
        
        self.lbl_accounts = Label(
            text="暂无数据",
            font_size=dp(16),
            size_hint=(1, 0.7)
        )
        
        btn_refresh = Button(text="🔄 刷新", font_size=dp(16), size_hint=(1, 0.1))
        btn_refresh.bind(on_press=lambda x: self.refresh())
        
        btn_back = Button(text="🔙 返回", font_size=dp(16), size_hint=(1, 0.1))
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main') if self.manager else None)
        
        layout.add_widget(title)
        layout.add_widget(self.lbl_accounts)
        layout.add_widget(btn_refresh)
        layout.add_widget(btn_back)
        
        self.add_widget(layout)
        self.refresh(None)
    
    def refresh(self, instance):
        accounts = self.finance_data.get_accounts()
        if not accounts:
            self.lbl_accounts.text = "暂无数据，快去添加记录吧！"
        else:
            text = ""
            for acc in accounts:
                latest = self.finance_data.get_latest_values().get(acc, {})
                if latest:
                    text += f"{acc}: ¥{latest['current_value']:,.0f}\n\n"
            self.lbl_accounts.text = text


class QuickEntryScreen(Screen):
    """快速录入页"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        title = Label(text="📝 快速录入", font_size=dp(20), size_hint=(1, 0.1))
        
        self.txt_date = TextInput(
            text=datetime.now().strftime("%Y-%m-%d"),
            font_size=dp(16),
            size_hint=(1, 0.1),
            multiline=False
        )
        
        self.txt_account = TextInput(
            hint_text="输入账户名称",
            font_size=dp(16),
            size_hint=(1, 0.1),
            multiline=False
        )
        
        self.txt_value = TextInput(
            hint_text="输入金额",
            font_size=dp(16),
            size_hint=(1, 0.1),
            multiline=False
        )
        
        btn_save = Button(text="💾 保存", font_size=dp(18), size_hint=(1, 0.1))
        btn_save.bind(on_press=self.save_record)
        
        btn_back = Button(text="🔙 返回", font_size=dp(16), size_hint=(1, 0.1))
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main') if self.manager else None)
        
        layout.add_widget(title)
        layout.add_widget(self.txt_date)
        layout.add_widget(self.txt_account)
        layout.add_widget(self.txt_value)
        layout.add_widget(btn_save)
        layout.add_widget(btn_back)
        
        self.add_widget(layout)
    
    def save_record(self, instance):
        try:
            date = self.txt_date.text
            account = self.txt_account.text
            value = float(self.txt_value.text)
            
            if not date or not account:
                raise ValueError("日期和账户不能为空")
            
            finance_data = FinanceData()
            finance_data.add_record(date, account, value)
            
            self.txt_account.text = ""
            self.txt_value.text = ""
            
            # 显示成功提示
            from kivy.uix.popup import Popup
            popup = Popup(
                title="成功",
                content=Label(text="保存成功！"),
                size_hint=(0.8, 0.3)
            )
            popup.open()
            
        except Exception as e:
            from kivy.uix.popup import Popup
            popup = Popup(
                title="错误",
                content=Label(text=f"保存失败：{e}"),
                size_hint=(0.8, 0.3)
            )
            popup.open()


class BatchEntryScreen(Screen):
    """批量录入页"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        layout.add_widget(Label(text="📋 批量录入", font_size=dp(20), size_hint=(1, 0.1)))
        layout.add_widget(Label(text="功能开发中...", font_size=dp(16)))
        btn_back = Button(text="🔙 返回", font_size=dp(16), size_hint=(1, 0.1))
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main') if self.manager else None)
        layout.add_widget(btn_back)
        self.add_widget(layout)


class DataScreen(Screen):
    """数据管理页"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        layout.add_widget(Label(text="💾 数据管理", font_size=dp(20), size_hint=(1, 0.1)))
        layout.add_widget(Label(text="功能开发中...", font_size=dp(16)))
        btn_back = Button(text="🔙 返回", font_size=dp(16), size_hint=(1, 0.1))
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main') if self.manager else None)
        layout.add_widget(btn_back)
        self.add_widget(layout)


class FinanceAppMobile(App):
    """主应用类"""
    
    def build(self):
        self.title = "陈大哥的理财账本"
        
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(OverviewScreen(name='overview'))
        sm.add_widget(QuickEntryScreen(name='quick_entry'))
        sm.add_widget(BatchEntryScreen(name='batch_entry'))
        sm.add_widget(DataScreen(name='data'))
        
        # 设置屏幕管理器引用
        for screen in sm.screens:
            screen.screen_manager = sm
        
        return sm


if __name__ == '__main__':
    FinanceAppMobile().run()
