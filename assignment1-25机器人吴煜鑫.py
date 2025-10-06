import cv2
import numpy as np
import matplotlib.pyplot as plt

# 从output.avi中逐帧读取并将当前帧存为frame
cam = cv2.VideoCapture(r"res\output.avi")
cnt = 0

while True:
    ret, frame = cam.read()
    if not ret:
        break
        
    frame = cv2.rotate(frame, cv2.ROTATE_180)
    
    # 展示当前帧
    cv2.imshow('frame', frame)
    
    # 等待按键，如果按下q键则退出
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break
        
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # 在while循环中进行你对frame的处理
    current = frame[130:200, 300:340]
  
    # 红色（考虑色相环两端）
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])
    
    # 修复：将 hsv 改为 current
    mask_red = cv2.inRange(current, lower_red1, upper_red1) | cv2.inRange(current, lower_red2, upper_red2)

    # 紫色（色相范围130-160）
    lower_purple = np.array([130, 100, 100])
    upper_purple = np.array([160, 255, 255])
    mask_purple = cv2.inRange(current, lower_purple, upper_purple)

    # 蓝色（色相范围100-130）
    lower_blue = np.array([100, 100, 100])
    upper_blue = np.array([130, 255, 255])
    mask_blue = cv2.inRange(current, lower_blue, upper_blue)

    # 计算各颜色像素数量
    red_count = cv2.countNonZero(mask_red)
    purple_count = cv2.countNonZero(mask_purple)
    blue_count = cv2.countNonZero(mask_blue)

    color_counts = {'红色': red_count, '蓝色': blue_count, '紫色': purple_count}
    
    # 只有当有颜色被检测到时才输出
    if red_count > 0 or blue_count > 0 or purple_count > 0:
        dominant_color = max(color_counts, key=color_counts.get)
        print(f"帧 {cnt}: 主要颜色 - {dominant_color}")
    else:
        print(f"帧 {cnt}: 无球")
    
    cnt += 1

cam.release()
cv2.destroyAllWindows()  # 关闭窗口