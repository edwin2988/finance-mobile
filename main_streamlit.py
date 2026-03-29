# 陈大哥的理财账本 - Streamlit 手机版
# 运行：streamlit run main_streamlit.py

import streamlit as st
import json
import os
from datetime import datetime
from collections import defaultdict

# 设置页面配置（手机友好）
st.set_page_config(
    page_title="陈大哥的理财账本",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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
            st.error(f"加载数据失败：{e}")
            self.data = []
    
    def save_data(self):
        """保存数据"""
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            st.error(f"保存数据失败：{e}")
    
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


def main():
    st.title("陈大哥的理财账本 📊")
    
    # 初始化数据
    if 'finance_data' not in st.session_state:
        st.session_state.finance_data = FinanceData()
    
    finance_data = st.session_state.finance_data
    
    # 侧边栏导航
    menu = ["🏠 首页", "📊 账户总览", "📝 快速录入", "📋 批量录入", "💾 数据管理", "⚙️ 设置"]
    choice = st.sidebar.selectbox("导航", menu)
    
    # ============= 首页 =============
    if choice == "🏠 首页":
        st.header("欢迎使用理财账本")
        
        # 计算总估值
        latest = finance_data.get_latest_values()
        total = sum(r["current_value"] for r in latest.values())
        
        # 显示总估值卡片
        st.metric(
            label="总估值",
            value=f"¥{total:,.0f}",
            delta=None
        )
        
        # 功能快捷入口
        st.markdown("### 功能入口")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 账户总览", use_container_width=True):
                st.session_state.current_page = "账户总览"
                st.rerun()
        with col2:
            if st.button("📝 快速录入", use_container_width=True):
                st.session_state.current_page = "快速录入"
                st.rerun()
        
        col3, col4 = st.columns(2)
        with col3:
            if st.button("📋 批量录入", use_container_width=True):
                st.session_state.current_page = "批量录入"
                st.rerun()
        with col4:
            if st.button("💾 数据管理", use_container_width=True):
                st.session_state.current_page = "数据管理"
                st.rerun()
        
        # 显示最近记录
        if finance_data.data:
            st.markdown("### 最近记录")
            recent = finance_data.data[-5:][::-1]  # 最近 5 条
            for record in recent:
                st.info(f"{record['date']} {record['account']}: ¥{record['current_value']:,.0f}")
    
    # ============= 账户总览 =============
    elif choice == "📊 账户总览":
        st.header("账户总览")
        
        accounts = finance_data.get_accounts()
        
        if not accounts:
            st.warning("暂无数据，快去添加记录吧！")
        else:
            for acc in accounts:
                records = finance_data.get_account_records(acc)
                if records:
                    latest = records[0]
                    with st.expander(f"{acc} - ¥{latest['current_value']:,.0f}"):
                        st.write(f"**记录数**: {len(records)}")
                        st.write(f"**最新日期**: {latest['date']}")
                        
                        # 显示该账户的所有记录
                        st.write("### 历史记录")
                        for r in records:
                            st.write(f"- {r['date']}: ¥{r['current_value']:,.0f}")
    
    # ============= 快速录入 =============
    elif choice == "📝 快速录入":
        st.header("快速录入")
        
        with st.form("quick_entry_form"):
            date = st.date_input("日期", datetime.now())
            account = st.text_input("账户名称")
            value = st.number_input("当前估值", min_value=0.0, step=100.0)
            
            submitted = st.form_submit_button("💾 保存", use_container_width=True)
            
            if submitted:
                if not account:
                    st.error("账户名称不能为空！")
                else:
                    date_str = date.strftime("%Y-%m-%d")
                    finance_data.add_record(date_str, account, value)
                    st.success("保存成功！")
                    st.balloons()
                    st.session_state.finance_data = finance_data  # 更新 session
                    st.rerun()
    
    # ============= 批量录入 =============
    elif choice == "📋 批量录入":
        st.header("批量录入")
        st.info("功能开发中...")
        st.write("提示：可以先用快速录入功能，或稍后完善此功能。")
    
    # ============= 数据管理 =============
    elif choice == "💾 数据管理":
        st.header("数据管理")
        
        # 显示数据统计
        st.write(f"总记录数：{len(finance_data.data)}")
        st.write(f"账户数：{len(finance_data.get_accounts())}")
        
        # 导出功能
        if st.button("导出为 CSV"):
            # 生成 CSV 内容
            csv_content = "date,account,current_value\n"
            for record in finance_data.data:
                csv_content += f"{record['date']},{record['account']},{record['current_value']}\n"
            
            # 提供下载
            st.download_button(
                label="下载 CSV 文件",
                data=csv_content,
                file_name="finance_data.csv",
                mime="text/csv"
            )
        
        # 清空数据
        if st.button("🗑️ 清空所有数据"):
            st.warning("此操作不可恢复！")
            if st.checkbox("确认清空"):
                finance_data.data = []
                finance_data.save_data()
                st.success("数据已清空！")
                st.session_state.finance_data = finance_data
                st.rerun()
    
    # ============= 设置 =============
    elif choice == "⚙️ 设置":
        st.header("设置")
        st.info("功能开发中...")
        st.write(f"数据文件：{DATA_FILE}")
        st.write(f"数据量：{len(finance_data.data)} 条")


if __name__ == "__main__":
    main()
