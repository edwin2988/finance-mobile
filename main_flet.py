# 陈大哥的理财账本 - Flet 版
# 运行：flet run main_flet.py
# 构建 APK: flet build apk main_flet.py

import flet as ft
import json
import os
from datetime import datetime

# 数据文件路径
DATA_FILE = 'finance_data_v5.json'

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
        except:
            self.data = []
    
    def save_data(self):
        """保存数据"""
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存失败：{e}")
    
    def add_record(self, date, account, value):
        """添加记录"""
        self.data.append({
            "date": date,
            "account": account,
            "current_value": float(value)
        })
        self.save_data()
    
    def get_total(self):
        """获取总计"""
        if not self.data:
            return 0
        return sum(r.get('current_value', 0) for r in self.data)
    
    def get_accounts(self):
        """获取账户列表"""
        accounts = {}
        for r in self.data:
            acc = r.get('account', '未知')
            if acc not in accounts:
                accounts[acc] = []
            accounts[acc].append(r)
        return accounts
    
    def get_latest_records(self, limit=10):
        """获取最新记录"""
        sorted_data = sorted(self.data, key=lambda x: x.get('date', ''), reverse=True)
        return sorted_data[:limit]

def main(page: ft.Page):
    page.title = "陈大哥的理财账本"
    page.scroll = "auto"
    page.padding = 20
    
    finance = FinanceData()
    
    # 输入控件
    date_input = ft.TextField(label="日期", value=datetime.now().strftime("%Y-%m-%d"))
    account_input = ft.TextField(label="账户名称")
    value_input = ft.TextField(label="金额", keyboard_type=ft.KeyboardType.NUMBER)
    
    def add_click(e):
        if not account_input.value or not value_input.value:
            page.snack_bar = ft.SnackBar(ft.Text("请填写完整信息"))
            page.snack_bar.open = True
            return
        finance.add_record(date_input.value, account_input.value, value_input.value)
        account_input.value = ""
        value_input.value = ""
        refresh()
        page.snack_bar = ft.SnackBar(ft.Text("保存成功！"))
        page.snack_bar.open = True
    
    def refresh():
        # 更新总计
        total_card.controls[1].value = f"¥{finance.get_total():,.2f}"
        
        # 更新账户列表
        accounts = finance.get_accounts()
        account_list = []
        for name, records in accounts.items():
            latest = max(records, key=lambda x: x.get('date', ''))
            account_list.append(ft.ListTile(title=ft.Text(name), subtitle=ft.Text(f"¥{latest.get('current_value', 0):,.2f}")))
        accounts_section.controls = account_list if account_list else [ft.Text("暂无账户")]
        
        # 更新记录列表
        records = finance.get_latest_records()
        record_list = []
        for r in records:
            record_list.append(ft.ListTile(title=ft.Text(f"{r.get('date', '')} {r.get('account', '')}"), subtitle=ft.Text(f"¥{r.get('current_value', 0):,.2f}")))
        records_section.controls = record_list if record_list else [ft.Text("暂无记录")]
        
        page.update()
    
    # 总计卡片
    total_card = ft.Container(
        content=ft.Column([
            ft.Text("总估值", size=16, color="white"),
            ft.Text("¥0.00", size=32, weight="bold", color="white"),
            ft.Text("今日盈亏：--", size=14, color="white70")
        ], alignment="center"),
        gradient=ft.LinearGradient(colors=["#667eea", "#764ba2"]),
        padding=20,
        border_radius=10,
        margin=ft.margin.only(bottom=20)
    )
    
    # 账户部分
    accounts_section = ft.Column([ft.Text("加载中...")])
    accounts_card = ft.Container(
        content=ft.Column([
            ft.Text("📊 账户总览", size=18, weight="bold"),
            accounts_section
        ]),
        padding=20,
        border_radius=10,
        bgcolor="white",
        margin=ft.margin.only(bottom=20)
    )
    
    # 录入部分
    input_card = ft.Container(
        content=ft.Column([
            ft.Text("📝 快速录入", size=18, weight="bold"),
            date_input,
            account_input,
            value_input,
            ft.ElevatedButton("保存记录", on_click=add_click, width=200)
        ]),
        padding=20,
        border_radius=10,
        bgcolor="white",
        margin=ft.margin.only(bottom=20)
    )
    
    # 记录部分
    records_section = ft.Column([ft.Text("加载中...")])
    records_card = ft.Container(
        content=ft.Column([
            ft.Text("📋 最近记录", size=18, weight="bold"),
            records_section
        ]),
        padding=20,
        border_radius=10,
        bgcolor="white"
    )
    
    page.add(total_card, accounts_card, input_card, records_card)
    refresh()

ft.app(target=main, view=ft.AppView.WEB_BROWSER)
