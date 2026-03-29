# 陈大哥的理财账本 - 手机版 (Flet 版)
# 使用 Flet 框架，支持桌面和安卓

import flet as ft
import json
import os
from datetime import datetime
from collections import defaultdict

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


def main(page: ft.Page):
    """主应用"""
    page.title = "陈大哥的理财账本 📊"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.scroll = "auto"
    
    # 数据管理
    finance_data = FinanceData()
    
    # ============= 主界面 =============
    def main_view():
        # 计算总估值
        latest = finance_data.get_latest_values()
        total = sum(r["current_value"] for r in latest.values())
        
        return ft.Column([
            # 标题
            ft.Container(
                content=ft.Text(
                    "陈大哥的理财账本 📊",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER
                ),
                padding=ft.padding.only(bottom=20),
                alignment=ft.alignment.center
            ),
            
            # 总估值卡片
            ft.Container(
                content=ft.Column([
                    ft.Text("总估值", size=14, color=ft.colors.GREY),
                    ft.Text(f"¥{total:,.0f}", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=ft.colors.BLUE_50,
                border_radius=10,
                padding=20,
                margin=ft.margin.only(bottom=20)
            ),
            
            # 功能按钮
            ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon(ft.icons.ACCOUNT_BALANCE_WALLET, color=ft.colors.WHITE),
                    ft.Text("账户总览", size=18, color=ft.colors.WHITE),
                ], alignment=ft.MainAxisAlignment.CENTER),
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.BLUE,
                    padding=15,
                ),
                on_click=lambda _: navigate('overview'),
                height=50,
            ),
            
            ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon(ft.icons.ADD_CIRCLE_OUTLINE, color=ft.colors.WHITE),
                    ft.Text("快速录入", size=18, color=ft.colors.WHITE),
                ], alignment=ft.MainAxisAlignment.CENTER),
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.GREEN,
                    padding=15,
                ),
                on_click=lambda _: navigate('quick_entry'),
                height=50,
            ),
            
            ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon(ft.icons.LIST_ALT, color=ft.colors.WHITE),
                    ft.Text("批量录入", size=18, color=ft.colors.WHITE),
                ], alignment=ft.MainAxisAlignment.CENTER),
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.ORANGE,
                    padding=15,
                ),
                on_click=lambda _: navigate('batch_entry'),
                height=50,
            ),
            
            ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon(ft.icons.SD_CARD, color=ft.colors.WHITE),
                    ft.Text("数据管理", size=18, color=ft.colors.WHITE),
                ], alignment=ft.MainAxisAlignment.CENTER),
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.PURPLE,
                    padding=15,
                ),
                on_click=lambda _: navigate('data'),
                height=50,
            ),
            
            ft.ElevatedButton(
                content=ft.Row([
                    ft.Icon(ft.icons.SETTINGS, color=ft.colors.WHITE),
                    ft.Text("设置", size=18, color=ft.colors.WHITE),
                ], alignment=ft.MainAxisAlignment.CENTER),
                style=ft.ButtonStyle(
                    bgcolor=ft.colors.GREY_700,
                    padding=15,
                ),
                on_click=lambda _: navigate('settings'),
                height=50,
            ),
        ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    
    # ============= 账户总览页 =============
    def overview_view():
        accounts = finance_data.get_accounts()
        
        if not accounts:
            return ft.Column([
                ft.Text("📊 账户总览", size=24, weight=ft.FontWeight.BOLD),
                ft.Divider(),
                ft.Text("暂无数据，快去添加记录吧！", color=ft.colors.GREY),
                ft.ElevatedButton("返回", on_click=lambda _: navigate('main')),
            ])
        
        items = []
        for acc in accounts:
            records = finance_data.get_account_records(acc)
            if records:
                latest = records[0]
                items.append(
                    ft.Card(
                        content=ft.Container(
                            content=ft.Row([
                                ft.Column([
                                    ft.Text(acc, size=18, weight=ft.FontWeight.BOLD),
                                    ft.Text(f"最新估值：¥{latest['current_value']:,.0f}", size=14),
                                ], expand=True),
                                ft.Column([
                                    ft.Text(f"记录数：{len(records)}", size=12, color=ft.colors.GREY),
                                ], horizontal_alignment=ft.CrossAxisAlignment.END),
                            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                            padding=15,
                        ),
                    )
                )
        
        return ft.Column([
            ft.Text("📊 账户总览", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Column(items, spacing=10),
            ft.ElevatedButton("🔄 刷新", on_click=lambda _: refresh()),
            ft.ElevatedButton("🔙 返回", on_click=lambda _: navigate('main')),
        ])
    
    # ============= 快速录入页 =============
    date_field = ft.TextField(label="日期", value=datetime.now().strftime("%Y-%m-%d"))
    account_field = ft.TextField(label="账户名称")
    value_field = ft.TextField(label="当前估值", keyboard_type=ft.KeyboardType.NUMBER)
    
    def quick_entry_view():
        return ft.Column([
            ft.Text("📝 快速录入", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            date_field,
            account_field,
            value_field,
            ft.ElevatedButton(
                "💾 保存",
                on_click=save_quick_entry,
                bgcolor=ft.colors.BLUE,
                color=ft.colors.WHITE,
            ),
            ft.ElevatedButton("🔙 返回", on_click=lambda _: navigate('main')),
        ])
    
    def save_quick_entry(e):
        try:
            date = date_field.value
            account = account_field.value
            value = float(value_field.value)
            
            if not date or not account:
                raise ValueError("日期和账户不能为空")
            
            finance_data.add_record(date, account, value)
            
            # 清空输入框
            account_field.value = ""
            value_field.value = ""
            page.update()
            
            # 显示成功提示
            page.dialog = ft.AlertDialog(
                title=ft.Text("成功"),
                content=ft.Text("保存成功！"),
                actions=[
                    ft.TextButton("确定", on_click=lambda _: close_dialog()),
                ],
            )
            page.dialog.open = True
            page.update()
            
        except Exception as ex:
            page.dialog = ft.AlertDialog(
                title=ft.Text("错误"),
                content=ft.Text(f"保存失败：{ex}"),
                actions=[
                    ft.TextButton("确定", on_click=lambda _: close_dialog()),
                ],
            )
            page.dialog.open = True
            page.update()
    
    def close_dialog():
        page.dialog = None
        page.update()
    
    # ============= 批量录入页 =============
    def batch_entry_view():
        return ft.Column([
            ft.Text("📋 批量录入", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text("功能开发中...", color=ft.colors.GREY),
            ft.ElevatedButton("🔙 返回", on_click=lambda _: navigate('main')),
        ])
    
    # ============= 数据管理页 =============
    def data_view():
        return ft.Column([
            ft.Text("💾 数据管理", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text("功能开发中...", color=ft.colors.GREY),
            ft.ElevatedButton("🔙 返回", on_click=lambda _: navigate('main')),
        ])
    
    # ============= 设置页 =============
    def settings_view():
        return ft.Column([
            ft.Text("⚙️ 设置", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text("功能开发中...", color=ft.colors.GREY),
            ft.ElevatedButton("🔙 返回", on_click=lambda _: navigate('main')),
        ])
    
    # ============= 导航函数 =============
    def navigate(view_name):
        page.views.clear()
        if view_name == 'main':
            page.views.append(main_view())
        elif view_name == 'overview':
            page.views.append(overview_view())
        elif view_name == 'quick_entry':
            page.views.append(quick_entry_view())
        elif view_name == 'batch_entry':
            page.views.append(batch_entry_view())
        elif view_name == 'data':
            page.views.append(data_view())
        elif view_name == 'settings':
            page.views.append(settings_view())
        page.update()
    
    def refresh():
        page.update()
    
    # 初始化显示主界面
    page.views.append(main_view())
    page.update()


# 运行应用
if __name__ == "__main__":
    ft.app(main)
