import pandas as pd

# Đọc dữ liệu từ file Excel qua URL
url = "https://docs.google.com/spreadsheets/d/1e9rRiwAmRYq60Lx2PBMZcSOA8jC-rmoL/export?format=xlsx"
try:
    # Đọc dữ liệu vào DataFrame
    data = pd.read_excel(url)
except Exception as e:
    print(f"Lỗi khi đọc file: {e}")
    exit()

# Kiểm tra xem file có dữ liệu không
if data.empty:
    print("File Excel không chứa dữ liệu!")
    exit()

# Xử lý dữ liệu: Kiểm tra và loại bỏ giá trị NaN trong các cột liên quan
data = data.dropna(subset=['vpv1', 'pCharge', 'SOC', 'ppv1', 'ppv2', 'ppv3'])

# Xử lý cột SOC ở dạng số+%
# Loại bỏ ký tự '%' và chuyển đổi SOC thành kiểu số để so sánh
data['SOC'] = data['SOC'].str.rstrip('%').astype(float)

# Lọc dữ liệu theo điều kiện
filtered_data = data[(data['vpv1'] != 0) & (data['pCharge'] != 0) & (data['SOC'] > 8)].copy()

# Tính tổng dữ liệu các cột ppv1, ppv2, ppv3 và lưu vào cột mới 'Sum_PPV'
filtered_data['Sum_PPV'] = filtered_data[['ppv1', 'ppv2', 'ppv3']].sum(axis=1)

# Lưu dữ liệu đã lọc vào file CSV mới
filtered_data.to_csv('Data_new.csv', index=False)

# Xác nhận hoàn thành
print("Dữ liệu đã được lọc, tính toán và lưu vào file 'Data_new.csv'.")