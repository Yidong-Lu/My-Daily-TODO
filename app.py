import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 页面设置 ---
st.set_page_config(page_title="每日办事前置", layout="centered")
st.title("🗓️ 每日待办与结果记录")

# --- 数据存储逻辑 ---
DB_FILE = "todo_data.csv"

def load_data():
    if os.path.exists(DB_FILE):
        return pd.read_csv(DB_FILE)
    return pd.DataFrame(columns=["日期", "任务内容", "状态", "结果备注"])

def save_data(df):
    df.to_csv(DB_FILE, index=False)

data = load_data()

# --- 输入区 ---
with st.form("add_task", clear_on_submit=True):
    new_task = st.text_input("📝 今天打算做什么？", placeholder="例如：给王经理回电话")
    submitted = st.form_submit_button("添加任务")
    
    if submitted and new_task:
        new_row = {
            "日期": datetime.now().strftime("%Y-%m-%d"),
            "任务内容": new_task,
            "状态": "未完成",
            "结果备注": ""
        }
        data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
        save_data(data)
        st.success("任务已添加！")

# --- 任务管理区 ---
st.divider()
st.subheader("📌 待办列表")

if not data.empty:
    # 筛选今天的任务
    today = datetime.now().strftime("%Y-%m-%d")
    today_tasks = data[data["日期"] == today]

    for index, row in today_tasks.iterrows():
        col1, col2, col3 = st.columns([1, 4, 2])
        
        with col1:
            # 完成勾选
            is_done = st.checkbox("完成", key=f"check_{index}", value=(row["状态"] == "已完成"))
        
        with col2:
            # 任务描述
            st.write(f"**{row['任务内容']}**")
            # 结果记录
            note = st.text_input("记录结果", value=row["结果备注"], key=f"note_{index}", placeholder="事情办得怎么样？")
        
        with col3:
            # 更新按钮
            if st.button("更新状态", key=f"btn_{index}"):
                data.at[index, "状态"] = "已完成" if is_done else "未完成"
                data.at[index, "结果备注"] = note
                save_data(data)
                st.rerun()

# --- 历史回顾 ---
st.divider()
if st.checkbox("查看历史记录"):
    st.dataframe(data, use_container_width=True)
