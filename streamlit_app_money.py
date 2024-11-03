import streamlit as st
import pandas as pd

# 設定頁面配置
st.set_page_config(page_title="軟體管理網頁")

# 設定 CSS
st.markdown("""
    <style>
    body {
        font-family: 'Microsoft JhengHei', sans-serif;
        background-color: #f4f4f4;
    }
    h1 {
        color: #276ac2;  
        font-size: 2.5em;
        text-align: center;
        margin-top: 30px;
    }
    h2 {
        color: #333;
    }
    .sidebar .sidebar-content {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 8px;
    }
    .stButton > button {
        background-color: #276ac2;  
        color: white;
        border-radius: 5px;
        padding: 10px;
        margin-top: 20px;
    }
    .stImage {
        display: block;
        margin: 0 auto;
    }
    </style>
    """, unsafe_allow_html=True)

# 載入資料
@st.cache_data
def load_data():
    return pd.read_csv('money_data.csv')

@st.cache_data
def load_purchase_data():
    return pd.read_csv('date_data.csv')

df = load_data()
purchase_df = load_purchase_data()

# 全局變數存儲查詢結果
filtered_df_global = pd.DataFrame()

# 主頁
def main_page():
    st.title("🏛️ 軟體管理網頁")
    st.markdown('***')
    st.write("##### 歡迎使用軟體管理網頁！請選擇左側目錄中的功能。")
    st.markdown('***')
    st.markdown('#### 【採購聯絡資訊】')
    st.info('【大塚】卓靜萩 Jessica，Tel：02-8964-6668 # 2886')
    st.info('【采威】陳怡馨 Cindy，Tel：04-23265200 #376')
    # 版本和日期
    st.markdown("#### 【版本日期資訊】")
    st.info("版本: 1.0.0。發佈日期: 2024/11/04")
    # 公司版權與製作者
    st.markdown('***')
    st.write('Page Designed by Nan-Xuan. ©')

# 子頁：資料數量統計頁
def stats_page():
    global filtered_df_global  # 使用全局變數

    st.title("📊 軟體價格統計")
    st.markdown('***')

    # 提取廠商和產品列表
    vendors = df['廠商'].unique()
    selected_vendor = st.sidebar.selectbox("選擇廠商", vendors)

    # 根據選擇的廠商篩選數據
    filtered_vendor_df = df[df['廠商'] == selected_vendor]
    
    # 提取產品列表
    products = filtered_vendor_df['產品'].unique()
    selected_product = st.sidebar.selectbox("選擇產品", products)

    # 提取簽約年限列表
    contract_years = filtered_vendor_df['簽約年限'].unique()
    selected_contract_year = st.sidebar.selectbox("選擇簽約年限", contract_years)

    # 查詢按鈕
    if st.sidebar.button("查詢"):
        # 根據選擇的產品和簽約年限篩選數據
        filtered_df = filtered_vendor_df[
            (filtered_vendor_df['產品'] == selected_product) & 
            (filtered_vendor_df['簽約年限'] == selected_contract_year)
        ]

        # 更新全局變數
        filtered_df_global = filtered_df

        # 顯示報價日期的資訊作為表格
        st.write("以下是軟體價格統計資訊：")
        if not filtered_df.empty:
            filtered_df['含稅金額'] = filtered_df['含稅金額'].apply(lambda x: f"${x:,.0f}")
            # 隱藏項次欄位，只顯示必要的欄位
            st.dataframe(filtered_df[['廠商', '產品', '報價日期', '簽約年限', '未稅金額', '稅金', '含稅金額']])

            # 新增下載按鈕
            st.download_button(
                label="下載價格統計資料",
                data=filtered_df.to_csv(index=False).encode('utf-8'),
                file_name='money_data.csv',
                mime='text/csv'
            )
        else:
            st.warning("沒有找到相關報價資料。")

# 子頁：軟體採購紀錄
def purchase_record_page():
    st.title("📆 軟體採購紀錄")
    st.markdown('***')
    st.write("以下是軟體採購紀錄資料：")

    # 檢查是否有採購紀錄資料
    if purchase_df.empty:
        st.warning("沒有找到相關採購紀錄資料。")
    else:
        # 刪除空白欄位
        purchase_df_cleaned = purchase_df.dropna(axis=1, how='all')
        st.dataframe(purchase_df_cleaned, width=2400)
        # 新增下載按鈕
        st.download_button(
            label="下載採購紀錄資料",
            data=purchase_df_cleaned.to_csv(index=False).encode('utf-8'),
            file_name='date_data.csv',
            mime='text/csv'
        )

# 主程式與多頁面應用
st.sidebar.title("軟體管理目錄")
page = st.sidebar.selectbox("選擇頁面", ["主頁", "軟體價格統計", "軟體採購紀錄"])

if page == "主頁":
    main_page()
elif page == "軟體價格統計":
    stats_page()
elif page == "軟體採購紀錄":
    # 在這裡顯示相同的查詢結果
    st.title("📊 軟體價格統計（查詢結果）")
    if not filtered_df_global.empty:
        st.write("以下是軟體價格統計查詢結果：")
        filtered_df_global['含稅金額'] = filtered_df_global['含稅金額'].apply(lambda x: f"${x:,.0f}")
        st.dataframe(filtered_df_global[['廠商', '產品', '報價日期', '簽約年限', '未稅金額', '稅金', '含稅金額']])
    else:
        st.warning("沒有查詢結果。")
