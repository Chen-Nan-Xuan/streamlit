import streamlit as st
import pandas as pd
# import matplotlib.pyplot as plt 
import altair as alt

# 設定頁面配置
st.set_page_config(page_title="軟理管理網站")

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
    return pd.read_csv('data_money.csv')

df = load_data()

# 主頁
def main_page():
    st.title("🗂️ 軟體管理網頁")
    st.markdown('***')
    st.write('歡迎使用軟體管理網頁！請選擇左側目錄中的功能。')
    st.markdown('***')
    st.markdown('#### 【聯絡資訊】')
    st.info('大塚-卓靜萩 Jessica，Tel：02-8964-6668 # 2886')
    st.info('采威-陳怡馨 Cindy，Tel：04-23265200 #376')
    # 版本和日期
    st.markdown("#### 【版本資訊】")
    st.info("版本: 1.0.0\n發佈日期: 2024-11-01")
    # 公司版權與製作者
    st.markdown('***')
    st.write('Page Designed by Nan-Xuan ©')

# 子頁：資料數量統計頁
def stats_page():
    st.title("📊 軟體價格統計")
    st.markdown('***')
    st.write("以下是軟體價格統計資訊：")

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

        # 顯示報價日期的資訊作為表格
        if not filtered_df.empty:
            filtered_df['含稅金額'] = filtered_df['含稅金額'].apply(lambda x: f"${x:,.0f}")
            # 隱藏項次欄位，只顯示必要的欄位
            st.dataframe(filtered_df[['廠商', '產品', '報價日期', '簽約年限', '未稅金額', '稅金', '含稅金額']])
        else:
            st.warning("沒有找到相關報價資料。")

# 漲幅數據
data = {
    "項目": [
        "Autodesk3年期折扣從10%調整成5%",
        "Autodesk因美金匯率調漲",
        "Autodesk因美金匯率調漲",
        "Autodesk因美金匯率調漲",
        "Autodesk3年期折扣不再提供5%優惠",
        "Autodesk調整整體商品報價",
        "Autodesk調整整體商品報價",
        "Autodesk大多數1年期的商品上漲",
        "Autodesk1年期&3年期的商品上漲",
        "Autodesk部分1年期的商品無10%優惠"
    ],
        "漲幅%": [
        5,
        3.6,
        6,
        6,
        5,
        6,
        3,
        5,
        5,
        10  # 最後一項是範圍
    ],
    "累積漲幅%": [
        5,
        8.6,
        14.6,
        20.6,
        25.6,
        31.6,
        34.6,
        39.6,
        44.6,
        54.6  # 最後一項是範圍
    ],
    "日期": [
        "20220107",
        "20220401",
        "20220606",
        "20221001",
        "20230107",
        "20230201",
        "20231001",
        "20240207",
        "20240507",
        "20250107"
    ]
}

df_price_increase = pd.DataFrame(data)
df_price_increase['日期'] = pd.to_datetime(df_price_increase['日期'], format='%Y%m%d')

# 子頁：軟體價格漲幅
def price_increase_page():
    st.title("📉 軟體價格漲幅")
    st.markdown('***')
    st.write("以下是軟體價格漲幅資訊：")

    # 使用 Altair 繪製折線圖
    line_chart = alt.Chart(df_price_increase).mark_line(point=True).encode(
        x='日期:T',
        y='累積漲幅%:Q',
        tooltip=['項目', '累積漲幅%', '日期']
    ).properties(
        title='Autodesk 軟體價格漲幅，以1年期的商品來看，從2022年至2025年整體約漲了44.6%；以3年期的商品來看，從2022年至2025年整體約漲了54.6%！',
        width=700,
        height=400
    )

    st.altair_chart(line_chart, use_container_width=True)
    st.markdown('***')
    st.dataframe(df_price_increase)

# 主程式與多頁面應用
st.sidebar.title("軟體管理目錄")
page = st.sidebar.selectbox("選擇頁面", ["主頁", "軟體價格統計", "軟體價格漲幅"])

if page == "主頁":
    main_page()
elif page == "軟體價格統計":
    stats_page()
elif page == "軟體價格漲幅":
    price_increase_page()
