import cv2
import numpy as np

# Kích thước cửa sổ
window_width = 1600
window_height = 1000
window_name = "app sửa hình"

# Tạo cửa sổ
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, window_width, window_height)

# Tạo hình nền (màu trắng)
background = np.ones((window_height, window_width, 3), dtype=np.uint8) * 255

# Thông số các nút
button_width = 300
button_height = 100
button_margin = 50
button_color = (0, 150, 255)  # Màu cam
button_text_color = (255, 255, 255)  # Màu trắng

# Vị trí các nút
buttons = [
    {"text": "Nút 1", "pos": (button_margin, button_margin)},
    {"text": "Nút 2", "pos": (button_margin, button_margin*2 + button_height)},
    {"text": "Nút 3", "pos": (window_width - button_width - button_margin, button_margin)},
    {"text": "Nút 4", "pos": (window_width - button_width - button_margin, button_margin*2 + button_height)}
]

# Vẽ các nút lên hình nền
for button in buttons:
    x, y = button["pos"]
    # Vẽ hình chữ nhật làm nút
    cv2.rectangle(background, 
                 (x, y), 
                 (x + button_width, y + button_height), 
                 button_color, -1)
    # Vẽ viền nút
    cv2.rectangle(background, 
                 (x, y), 
                 (x + button_width, y + button_height), 
                 (0, 0, 0), 2)
    # Thêm text vào nút
    text_size = cv2.getTextSize(button["text"], cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
    text_x = x + (button_width - text_size[0]) // 2
    text_y = y + (button_height + text_size[1]) // 2
    cv2.putText(background, button["text"], 
               (text_x, text_y), 
               cv2.FONT_HERSHEY_SIMPLEX, 1, 
               button_text_color, 2)

# Hàm xử lý sự kiện chuột
def mouse_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        for idx, button in enumerate(buttons):
            bx, by = button["pos"]
            # Kiểm tra click có nằm trong nút không
            if bx <= x <= bx + button_width and by <= y <= by + button_height:
                print(f"Bạn đã nhấn {button['text']}")
                # Thay đổi màu nút khi nhấn
                cv2.rectangle(background, 
                              (bx, by), 
                              (bx + button_width, by + button_height), 
                              (0, 255, 0), -1)  # Màu xanh khi nhấn
                cv2.putText(background, button["text"], 
                          (text_x, text_y), 
                          cv2.FONT_HERSHEY_SIMPLEX, 1, 
                          button_text_color, 2)
                cv2.imshow(window_name, background)
                cv2.waitKey(200)  # Hiệu ứng nhấp nháy
                # Trả lại màu ban đầu
                cv2.rectangle(background, 
                              (bx, by), 
                              (bx + button_width, by + button_height), 
                              button_color, -1)
                cv2.imshow(window_name, background)

# Gán hàm xử lý sự kiện chuột
cv2.setMouseCallback(window_name, mouse_event)

# Hiển thị cửa sổ
cv2.imshow(window_name, background)
cv2.waitKey(0)
cv2.destroyAllWindows()