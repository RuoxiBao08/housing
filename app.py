# 导入依赖库
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 加载加州住房数据集（确保housing.csv在同一文件夹）
df = pd.read_csv("housing.csv")

# 设置页面标题（必须包含你的姓名，示例：by [你的名字]）
st.title("California Housing Data (1990) by Minyang Jiang")


st.sidebar.header("Filter Controls")  # 侧边栏标题


# 注：先查看数据集的位置类型字段名（如df.columns），替换下方"ocean_proximity"为实际字段
location_options = df["ocean_proximity"].unique()  # 自动获取所有位置类型选项
location_filter = st.sidebar.multiselect(
    label="Select Location Type",  # 控件标题
    options=location_options,      # 可选值（从数据中提取）
    default=location_options       # 默认选中所有类型
)

income_filter = st.sidebar.radio(
    label="Filter by Income Level",  # 控件标题
    options=["Low (≤2.5)", "Medium (>2.5 & <4.5)", "High (>4.5)"],  # 选项
    index=0  # 默认选中第一个选项（Low）
)


price_filter = st.slider(
    label="Minimal Median House Price",  # 滑块标题
    min_value=0,                         # 最小值（文档要求）
    max_value=500001,                    # 最大值（文档要求）
    value=200000                         # 默认值（文档要求）
)

# ---------------------- 4. 数据筛选逻辑（核心） ----------------------
# 筛选条件1：房价 ≥ 滑块值
df_filtered = df[df["median_house_value"] >= price_filter]

# 筛选条件2：位置类型匹配多选框选择
df_filtered = df_filtered[df_filtered["ocean_proximity"].isin(location_filter)]

# 筛选条件3：收入水平（用if语句实现，按要求划分）
if income_filter == "Low (≤2.5)":
    df_filtered = df_filtered[df_filtered["median_income"] <= 2.5]
elif income_filter == "Medium (>2.5 & <4.5)":
    df_filtered = df_filtered[(df_filtered["median_income"] > 2.5) & (df_filtered["median_income"] < 4.5)]
else:  # High (>4.5)
    df_filtered = df_filtered[df_filtered["median_income"] > 4.5]

# 5.1 地图展示（Streamlit地图需数据包含latitude/longitude字段，加州数据集默认有这两个字段）
st.subheader("Housing Location Distribution")
st.map(df_filtered, zoom=6)  # zoom=6聚焦加州区域，更清晰

# 5.2 中位数房价直方图（bins=30，文档明确要求）
st.subheader("Distribution of Median House Value")
fig, ax = plt.subplots(figsize=(10, 4))
df_filtered["median_house_value"].hist(bins=30, color="#1f77b4", alpha=0.7, ax=ax)
ax.set_xlabel("Median House Value (USD)")
ax.set_ylabel("Number of Housing Units")
ax.set_title("Histogram of Median House Price")
st.pyplot(fig) 