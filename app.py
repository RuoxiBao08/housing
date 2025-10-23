import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="California Housing App", layout="wide")

st.title("🏠 California Housing Data Explorer")

# 1️⃣ 从网络读取数据（不需要 housing.xlsx）
url = "https://raw.githubusercontent.com/ageron/handson-ml/master/datasets/housing/housing.csv"
df = pd.read_csv(url)

# 2️⃣ 侧边栏筛选
st.sidebar.header("筛选条件")

# 房价滑块
min_price = float(df["median_house_value"].min())
max_price = float(df["median_house_value"].max())
price_filter = st.sidebar.slider("选择房价范围", min_price, max_price, (min_price, max_price))
df = df[(df["median_house_value"] >= price_filter[0]) & (df["median_house_value"] <= price_filter[1])]

# 地理位置多选
location_types = df["ocean_proximity"].unique()
selected_locations = st.sidebar.multiselect("选择位置类型", location_types, default=location_types)
df = df[df["ocean_proximity"].isin(selected_locations)]

# 收入水平筛选
st.sidebar.subheader("收入水平筛选")
income_option = st.sidebar.radio(
    "选择收入等级",
    ("全部", "Low (< 2.5)", "Medium (2.5-4.5)", "High (> 4.5)")
)
if income_option == "Low (< 2.5)":
    df = df[df["median_income"] < 2.5]
elif income_option == "Medium (2.5-4.5)":
    df = df[(df["median_income"] >= 2.5) & (df["median_income"] < 4.5)]
elif income_option == "High (> 4.5)":
    df = df[df["median_income"] >= 4.5]

# 3️⃣ 地图显示
st.subheader("📍 地图分布")
st.map(df[["latitude", "longitude"]])

# 4️⃣ 直方图
st.subheader("🏡 房价分布直方图（30 bins）")
fig, ax = plt.subplots()
ax.hist(df["median_house_value"], bins=30, color="skyblue", edgecolor="black")
ax.set_xlabel("Median House Value")
ax.set_ylabel("Count")
st.pyplot(fig)

# 5️⃣ 数据预览
st.subheader("📊 数据预览")
st.dataframe(df.head(10))