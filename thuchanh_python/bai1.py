import requests
import pandas as pd
from datetime import datetime

# Bước 1: Gửi yêu cầu GET đến API
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 52.52,
    "longitude": 13.41,
    "past_days": 10,
    "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
    "timezone": "auto"  # Tự động điều chỉnh múi giờ
}

response = requests.get(url, params=params)
data = response.json()

# Bước 2: Tạo DataFrame từ dữ liệu nhận được
hourly = data["hourly"]
df = pd.DataFrame({
    "time": hourly["time"],
    "temperature_2m": hourly["temperature_2m"],
    "relative_humidity_2m": hourly["relative_humidity_2m"],
    "wind_speed_10m": hourly["wind_speed_10m"]
})

# Thêm thông tin latitude và longitude
df["latitude"] = data["latitude"]
df["longitude"] = data["longitude"]

# Chuyển cột 'time' sang định dạng datetime
df["time"] = pd.to_datetime(df["time"])

# Bước 3: Lưu dữ liệu vào tệp CSV
df.to_csv("weather_data.csv", index=False)
print("Đã lưu dữ liệu vào 'weather_data.csv'.")

# Bước 4: Tính tổng các giá trị đến ngày 29-04
# Lọc dữ liệu đến hết ngày 29-04
end_date = pd.to_datetime("2025-04-29")
df_filtered = df[df["time"].dt.date <= end_date.date()]

# Tính tổng
total_temp = df_filtered["temperature_2m"].sum()
total_humidity = df_filtered["relative_humidity_2m"].sum()
total_wind = df_filtered["wind_speed_10m"].sum()

print(f"Tổng temperature_2m đến 29-04: {total_temp:.2f}°C")
print(f"Tổng relative_humidity_2m đến 29-04: {total_humidity:.2f}%")
print(f"Tổng wind_speed_10m đến 29-04: {total_wind:.2f} km/h")