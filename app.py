import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load data
df = pd.read_csv("StudentPerformanceFactors.csv")

# Title and theme
st.set_page_config(page_title="Student Performance Dashboard", layout="wide")

st.title("📊 Student Performance EDA Dashboard")

# Sidebar Filters
st.sidebar.header("🔍 Filter Options")
cat_col = st.sidebar.selectbox("Select Categorical Variable for Box Plot", df.select_dtypes(include='object').columns)
x_scatter = st.sidebar.selectbox("X-axis for Scatter Plot", df.select_dtypes(include='number').columns)
y_scatter = st.sidebar.selectbox("Y-axis for Scatter Plot", df.select_dtypes(include='number').columns)
color_scatter = st.sidebar.selectbox("Color by Categorical Feature", df.select_dtypes(include='object').columns)

# Tabs for different analysis sections
tab1, tab2, tab3, tab4 = st.tabs(["📈 Distribution", "📦 Box Plot", "📊 Correlation", "⚡ Scatter Plot"])

# Tab 1: Distribution
with tab1:
    st.subheader("Distribution of Exam Scores")
    fig = px.histogram(df, x="Exam_Score", nbins=30, title="Distribution of Exam Scores",
                       color_discrete_sequence=["#636EFA"], template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# Tab 2: Box Plot by Categorical Variable
with tab2:
    st.subheader(f"Exam Scores by {cat_col}")
    fig = px.box(df, x=cat_col, y="Exam_Score", color=cat_col,
                 title=f"Exam Scores by {cat_col}",
                 template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)

# Tab 3: Correlation Matrix
with tab3:
    st.subheader("Correlation Matrix (Numerical Variables)")
    corr = df.select_dtypes(include='number').corr()
    fig = go.Figure(data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.index,
        colorscale="Viridis"
    ))
    fig.update_layout(template="plotly_dark", title="Correlation Matrix")
    st.plotly_chart(fig, use_container_width=True)

# Tab 4: Scatter Plot
with tab4:
    st.subheader(f"{x_scatter} vs {y_scatter} by {color_scatter}")
    fig = px.scatter(df, x=x_scatter, y=y_scatter, color=df[color_scatter],
                     title=f"{x_scatter} vs {y_scatter} colored by {color_scatter}",
                     template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
