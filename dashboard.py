import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import os
from dotenv import load_dotenv
from streamlit_autorefresh import st_autorefresh


load_dotenv()


CHANNEL_ID = os.getenv("CHANNEL_ID")
READ_API_KEY = os.getenv("READ_API_KEY")


st_autorefresh(
    interval=5000,
    key="farm_refresh"
  )
st.set_page_config(
    page_title="Smart Agriculture Dashboard",
    layout="wide"
)

st.title("🌱 Smart Agriculture Monitoring System")

url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results=2"

response = requests.get(url)

data = response.json()

feeds = data["feeds"]

df = pd.DataFrame(feeds)

if len(df)>0:

    df["created_at"] = pd.to_datetime(df["created_at"])
    last_update = df["created_at"].iloc[-1]

    st.info(f"Last Updated: {last_update}")

    df["field1"] = pd.to_numeric(df["field1"])
    df["field2"] = pd.to_numeric(df["field2"])
    df["field3"] = pd.to_numeric(df["field3"])
    df["field4"] = pd.to_numeric(df["field4"])
    df["field5"] = pd.to_numeric(df["field5"])

    soil = df["field1"].iloc[-1]
    ###########################

    ###########################
    temp = df["field2"].iloc[-1]
    hum = df["field3"].iloc[-1]
    light = df["field4"].iloc[-1]

    weather_forecast = "CLEAR"

    auto_pump = "ON" if soil < 1800 and weather_forecast != "RAIN" else "OFF"
    
    pump = "ON" if df["field5"].iloc[-1]==1 else "OFF"

    c1,c2,c3,c4,c5,c6 = st.columns(6)

    c1.metric("Soil", soil)
    c2.metric("Temp", temp)
    c3.metric("Humidity", hum)
    c4.metric("Light", light)
    c5.metric("ThingSpeak Pump", pump)
    c6.metric("AI Pump Decision", auto_pump)
    
    
    water_saved = max(0, (soil - 1800) * 0.01)

    st.metric(
    "Estimated Water Saved (L)",
    round(water_saved,2)
  )
  
    st.divider()

    fig1 = px.line(
        df,
        x="created_at",
        y="field1",
        title="Soil Moisture Trend"
    )

    st.plotly_chart(fig1,use_container_width=True)

    fig2 = px.line(
        df,
        x="created_at",
        y="field2",
        title="Temperature Trend"
    )

    st.plotly_chart(fig2,use_container_width=True)

    fig3 = px.line(
        df,
        x="created_at",
        y="field3",
        title="Humidity Trend"
    )

    st.plotly_chart(fig3,use_container_width=True)

    fig4 = px.line(
        df,
        x="created_at",
        y="field4",
        title="Light Intensity Trend"
    )

    st.plotly_chart(fig4,use_container_width=True)
    print(response.json())
    
else:
    st.warning("No Data Available")
    
   # weather_forecast = "CLEAR"
if soil < 1500:
    soil_status = "🔴 Dry"
elif soil < 2500:
    soil_status = "🟡 Moderate"
else:
    soil_status = "🟢 Healthy"
st.success(f"Soil Condition: {soil_status}")
#if soil < 1800 and weather_forecast != "RAIN":
  #  pump = "ON"
#else:
 #   pump = "OFF"