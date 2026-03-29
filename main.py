# 陈大哥的理财账本 - 手机版
# 主程序入口

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.listview import ListView
from kivy.core.window import Window
import json
import os
from datetime import datetime
from collections import defaultdict

# 设置窗口大小（模拟手机）
Window.size = (360, 640)

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
    
    def delete_record(self, index):
        """删除记录"""
        if 0 <= index < len(self.data):
            self.data.pop(index)
            self.save_data()
    
    def get_accounts(self):
        """获取所有账户"""
        accounts = set()
        for record in self.data:
            accounts.add(record["account"])
        return sorted(list(accounts))
    
    def get_account_records(self, account):
        """获取指定账户的所有记录"""
        records = [r for r in self.data if r["account"] == account]
        records.sort(key=lambda x: x["date"], reverse=True)
        return records
    
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
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # 标题
        title = Label(
            text="陈大哥的理财账本 📊",
            font_size='24sp',
            size_hint=(1, 0.2)
        )
        
        # 功能按钮
        btn_overview = Button(
            text="📊 账户总览",
            font_size='18sp',
            size_hint=(1, 0.15)
        )
        btn_overview.bind(on_press=self.go_to_overview)
        
        btn_quick = Button(
            text="📝 快速录入",
            font_size='18sp',
            size_hint=(1, 0.15)
        )
        btn_quick.bind(on_press=self.go_to_quick_entry)
        
        btn_batch = Button(
            text="📋 批量录入",
            font_size='18sp',
            size_hint=(1, 0.15)
        )
        btn_batch.bind(on_press=self.go_to_batch_entry)
        
        btn_data = Button(
            text="💾 数据管理",
            font_size='18sp',
            size_hint=(1, 0.15)
        )
        btn_data.bind(on_press=self.go_to_data)
        
        btn_settings = Button(
            text="⚙️ 设置",
            font_size='18sp',
            size_hint=(1, 0.15)
        )
        btn_settings.bind(on_press=self.go_to_settings)
        
        # 总估值显示
        latest = self.finance_data.get_latest_values()
        total = sum(r["current_value"] for r in latest.values())
        lbl_total = Label(
            text=f"总估值：¥{total:,.0f}",
            font_size='20sp',
            size_hint=(1, 0.1)
        )
        
        # 添加组件
        layout.add_widget(title)
        layout.add_widget(btn_overview)
        layout.add_widget(btn_quick)
        layout.add_widget(btn_batch)
        layout.add_widget(btn_data)
        layout.add_widget(btn_settings)
        layout.add_widget(lbl_total)
        
        self.add_widget(layout)
    
    def go_to_overview(self, instance):
        self.manager.current = 'overview'
    
    def go_to_quick_entry(self, instance):
        self.manager.current = 'quick_entry'
    
    def go_to_batch_entry(self, instance):
        self.manager.current = 'batch_entry'
    
    def go_to_data(self, instance):
        self.manager.current = 'data'
    
    def go_to_settings(self, instance):
        self.manager.current = 'settings'


class OverviewScreen(Screen):
    """账户总览页"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.finance_data = FinanceData()
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        # 标题
        title = Label(
            text="📊 账户总览",
            font_size='20sp',
            size_hint=(1, 0.1)
        )
        
        # 账户列表
        self.account_list = ListView(
            item_strings=[],
            size_hint=(1, 0.8)
        )
        
        # 刷新按钮
        btn_refresh = Button(
            text="🔄 刷新",
            font_size='16sp',
            size_hint=(1, 0.1)
        )
        btn_refresh.bind(on_press=self.refresh_list)
        
        # 返回按钮
        btn_back = Button(
            text="🔙 返回",
            font_size='16sp',
            size_hint=(1, 0.1)
        )
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        
        layout.add_widget(title)
        layout.add_widget(self.account_list)
        layout.add_widget(btn_refresh)
        layout.add_widget(btn_back)
        
        self.add_widget(layout)
        self.refresh_list(None)
    
    def refresh_list(self, instance):
        """刷新列表"""
        accounts = self.finance_data.get_accounts()
        items = []
        for acc in accounts:
            records = self.finance_data.get_account_records(acc)
            if records:
                latest = records[0]
                items.append(f"{acc}: ¥{latest['current_value']:,.0f}")
        self.account_list.item_strings = items


class QuickEntryScreen(Screen):
    """快速录入页"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # 标题
        title = Label(
            text="📝 快速录入",
            font_size='20sp',
            size_hint=(1, 0.1)
        )
        
        # 日期输入
        lbl_date = Label(
            text="日期：",
            font_size='16sp',
            size_hint=(1, 0.1)
        )
        today = datetime.now().strftime("%Y-%m-%d")
        self.txt_date = TextInput(
            text=today,
            font_size='16sp',
            size_hint=(1, 0.1),
            multiline=False
        )
        
        # 账户输入
        lbl_account = Label(
            text="账户名称：",
            font_size='16sp',
            size_hint=(1, 0.1)
        )
        self.txt_account = TextInput(
            hint_text="输入账户名称",
            font_size='16sp',
            size_hint=(1, 0.1),
            multiline=False
        )
        
        # 估值输入
        lbl_value = Label(
            text="当前估值：",
            font_size='16sp',
            size_hint=(1, 0.1)
        )
        self.txt_value = TextInput(
            hint_text="输入金额",
            font_size='16sp',
            size_hint=(1, 0.1),
            multiline=False
        )
        
        # 保存按钮
        btn_save = Button(
            text="💾 保存",
            font_size='18sp',
            size_hint=(1, 0.1)
        )
        btn_save.bind(on_press=self.save_record)
        
        # 返回按钮
        btn_back = Button(
            text="🔙 返回",
            font_size='16sp',
            size_hint=(1, 0.1)
        )
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        
        layout.add_widget(title)
        layout.add_widget(lbl_date)
        layout.add_widget(self.txt_date)
        layout.add_widget(lbl_account)
        layout.add_widget(self.txt_account)
        layout.add_widget(lbl_value)
        layout.add_widget(self.txt_value)
        layout.add_widget(btn_save)
        layout.add_widget(btn_back)
        
        self.add_widget(layout)
    
    def save_record(self, instance):
        """保存记录"""
        try:
            date = self.txt_date.text
            account = self.txt_account.text
            value = float(self.txt_value.text)
            
            if not date or not account:
                raise ValueError("日期和账户不能为空")
            
            # 保存数据
            finance_data = FinanceData()
            finance_data.add_record(date, account, value)
            
            # 清空输入框
            self.txt_account.text = ""
            self.txt_value.text = ""
            
            # 提示成功
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
    """批量录入页（简化版）"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=5)
        
        title = Label(text="📋 批量录入", font_size='20sp', size_hint=(1, 0.1))
        
        lbl_info = Label(
            text="批量录入功能开发中...",
            font_size='16sp',
            size_hint=(1, 0.5)
        )
        
        btn_back = Button(
            text="🔙 返回",
            font_size='16sp',
            size_hint=(1, 0.1)
        )
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        
        layout.add_widget(title)
        layout.add_widget(lbl_info)
        layout.add_widget(btn_back)
        
        self.add_widget(layout)


class DataScreen(Screen):
    """数据管理页"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        title = Label(text="💾 数据管理", font_size='20sp', size_hint=(1, 0.1))
        
        lbl_info = Label(
            text="数据管理功能开发中...",
            font_size='16sp',
            size_hint=(1, 0.5)
        )
        
        btn_back = Button(
            text="🔙 返回",
            font_size='16sp',
            size_hint=(1, 0.1)
        )
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        
        layout.add_widget(title)
        layout.add_widget(lbl_info)
        layout.add_widget(btn_back)
        
        self.add_widget(layout)


class SettingsScreen(Screen):
    """设置页"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        title = Label(text="⚙️ 设置", font_size='20sp', size_hint=(1, 0.1))
        
        lbl_info = Label(
            text="设置功能开发中...",
            font_size='16sp',
            size_hint=(1, 0.5)
        )
        
        btn_back = Button(
            text="🔙 返回",
            font_size='16sp',
            size_hint=(1, 0.1)
        )
        btn_back.bind(on_press=lambda x: setattr(self.manager, 'current', 'main'))
        
        layout.add_widget(title)
        layout.add_widget(lbl_info)
        layout.add_widget(btn_back)
        
        self.add_widget(layout)


class ScreenManager(ScreenManager):
    """屏幕管理器"""
    pass


class FinanceAppMobile(App):
    """主应用类"""
    
    def build(self):
        self.title = "陈大哥的理财账本"
        
        # 创建屏幕管理器
        sm = ScreenManager()
        
        # 添加屏幕
        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(OverviewScreen(name='overview'))
        sm.add_widget(QuickEntryScreen(name='quick_entry'))
        sm.add_widget(BatchEntryScreen(name='batch_entry'))
        sm.add_widget(DataScreen(name='data'))
        sm.add_widget(SettingsScreen(name='settings'))
        
        return sm


if __name__ == '__main__':
    FinanceAppMobile().run()
