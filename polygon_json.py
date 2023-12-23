import json
import numpy as np
import cv2

# Đọc dữ liệu từ tệp JSON
with open('polygon.json', 'r') as json_file:
    data = json.load(json_file)

# Lấy dữ liệu từ khóa "polygon_data"
polygon_left = np.array(data.get("left", []))
polygon_right = np.array(data.get("right", []))
print(type(polygon_left))
print(polygon_right)