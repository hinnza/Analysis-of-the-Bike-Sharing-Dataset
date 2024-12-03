import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='darkgrid')

# Helper functions to prepare datasets
def create_hourly_usage_df(df):
    hourly_df = df.groupby(['hr', 'weekday']).agg({'cnt': 'sum'}).reset_index()
    return hourly_df

def create_user_type_df(df):
    user_type_df = df.groupby('workingday').agg({'casual': 'sum', 'registered': 'sum'}).reset_index()
    user_type_df.rename(columns={0: "Holiday", 1: "Workday"}, inplace=True)
    return user_type_df

def create_weather_effect_df(df):
    weather_df = df.groupby('weathersit').agg({'cnt': 'mean'}).reset_index()
    weather_df['weathersit'] = weather_df['weathersit'].replace({
        1: "Clear",
        2: "Cloudy",
        3: "Light Rain/Snow",
        4: "Heavy Rain/Snow"
    })
    return weather_df

# Load dataset
data = pd.read_csv("hour.csv")

# Sidebar for filters
st.sidebar.title("Filters")
year = st.sidebar.selectbox("Select Year", options=[2011, 2012], index=0)
month = st.sidebar.slider("Select Month", min_value=1, max_value=12, value=(1, 12))
hour_range = st.sidebar.slider("Select Hour Range", min_value=0, max_value=23, value=(0, 23))

# Filter dataset
filtered_data = data[
    (data['yr'] == (year - 2011)) &
    (data['mnth'].between(month[0], month[1])) &
    (data['hr'].between(hour_range[0], hour_range[1]))
]

# Prepare datasets
hourly_usage_df = create_hourly_usage_df(filtered_data)
user_type_df = create_user_type_df(filtered_data)
weather_effect_df = create_weather_effect_df(filtered_data)

# Dashboard title
st.title("🚴 Bike Sharing Usage Dashboard")
st.header(f"Year {year} Usage Insights")

# Metrics Section
st.subheader("Summary Metrics")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Rides", filtered_data['cnt'].sum())
with col2:
    st.metric("Average Temperature", f"{filtered_data['temp'].mean():.2f}")
with col3:
    st.metric("Average Humidity", f"{filtered_data['hum'].mean():.2f}")

# Hourly Usage Trends
st.subheader("Hourly Usage Trends")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=hourly_usage_df, x='hr', y='cnt', hue='weekday', palette="pastel", ax=ax)
ax.set_title("Hourly Usage by Day of Week")
ax.set_xlabel("Hour")
ax.set_ylabel("Total Users")
st.pyplot(fig)

# User Type Distribution
st.subheader("User Type Distribution")
fig, ax = plt.subplots(figsize=(10, 5))
user_type_df = user_type_df.melt(id_vars='workingday', value_vars=['casual', 'registered'], 
                                 var_name='User Type', value_name='Count')
sns.barplot(data=user_type_df, x='workingday', y='Count', hue='User Type', palette="muted", ax=ax)
ax.set_title("User Type Distribution (Workday vs Holiday)")
ax.set_xlabel("Working Day (0: Holiday, 1: Workday)")
ax.set_ylabel("Total Users")
st.pyplot(fig)

# Weather Effect
st.subheader("Weather Effect on Bike Usage")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=weather_effect_df, x='weathersit', y='cnt', palette="coolwarm", ax=ax)
ax.set_title("Average Usage by Weather Condition")
ax.set_xlabel("Weather Condition")
ax.set_ylabel("Average Users")
st.pyplot(fig)
