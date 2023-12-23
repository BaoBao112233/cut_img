# Import packages
import os
import argparse
import cv2
import numpy as np
import sys
import importlib.util
import json

def cut_frame_polygon(frame):
    # Tạo một mask đen với kích thước bằng với frame
    mask = np.zeros_like(frame)

    # Vẽ đa giác trắng lên mask
    cv2.fillPoly(mask, [polygon_area], (255, 255, 255))
    # cv2.fillPoly(mask, [polygon_right], (255, 255, 255))

    # Áp dụng mask để cắt frame
    result = cv2.bitwise_and(frame, mask)

    return frame, result


# Tọa độ của đa giác (polygon)
# Đọc dữ liệu từ tệp JSON
with open('polygon.json', 'r') as json_file:
    data = json.load(json_file)

height = data['size_height']
width = data['size_width']

# Define and parse input arguments
parser = argparse.ArgumentParser()

parser.add_argument('--Width_video',help='Width_frame video' , default= width) 
parser.add_argument('--Height_video',help='Height_frame video' , default= height) 
parser.add_argument('--video', help='Name of the video file',default='4K_road_traffic.mp4')
parser.add_argument('--path_save_json', help='Path save polygon jon',default="polygon.json")

args = parser.parse_args()

VIDEO_NAME = args.video
WIDTH_VIDEO = int(args.Width_video)
HEIGHT_VIDEO = int(args.Height_video)

# Get path to current working directory
CWD_PATH = os.getcwd()

# Path to video file
VIDEO_PATH = os.path.join(CWD_PATH,VIDEO_NAME)


# Open video file
video = cv2.VideoCapture(VIDEO_PATH)

# Kiểm tra xem video có được mở thành công không
if not video.isOpened():
    print('Failed to open the video.')
    exit()



# Lấy dữ liệu từ khóa "polygon_data"
polygon_area = np.array(data.get("area", []))
# polygon_right = np.array(data.get("right", []))

print("Polygon area:",polygon_area)
# print("Polygon right:",polygon_right)

while True:
    # Đọc frame từ video
    ret, frame = video.read()

    # Kiểm tra xem video còn frame để đọc không
    if not ret:
        print('End of video.')
        break
    
    frame_resized = cv2.resize(frame, (WIDTH_VIDEO, HEIGHT_VIDEO))
    
    frame, result = cut_frame_polygon(frame_resized)

    # Hiển thị frame gốc và frame đã cắt
    cv2.imshow('Original frame',frame)
    cv2.imshow('Cropped Frame', result)
    
    # Chờ 30ms và kiểm tra xem người dùng có nhấn phím 'q' không
    key = cv2.waitKey(30)
    if key == ord('q'):
        break

# Giải phóng các tài nguyên và đóng cửa sổ
video.release()
cv2.destroyAllWindows()
