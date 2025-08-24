import cv2
import numpy as np
import mediapipe as mp

# Chế độ xử lý nền
BACKGROUND_MODES = {
    "BLUR": 0,
    "REPLACE": 1,
    "GRAYSCALE": 2,
    "VIRTUAL_BG": 3
}

class ImprovedBackgroundEffect:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.background_mode = BACKGROUND_MODES["BLUR"]
        self.background_image = None
        
        # Khởi tạo MediaPipe Selfie Segmentation
        self.mp_selfie_segmentation = mp.solutions.selfie_segmentation
        self.selfie_segmentation = self.mp_selfie_segmentation.SelfieSegmentation(model_selection=1)
        
        # Load ảnh nền thay thế (nếu có)
        try:
            self.background_image = cv2.imread('img_phongcanh (1).jpg')
            if self.background_image is not None:
                print("Đã tải ảnh nền thành công")
            else:
                print("Không tìm thấy ảnh nền, sử dụng màu đơn sắc")
                # Tạo ảnh nền mặc định màu xanh
                self.background_image = np.zeros((480, 640, 3), dtype=np.uint8)
                self.background_image[:] = (255, 0, 0)  # Màu xanh lam
        except Exception as e:
            print(f"Không thể tải ảnh nền: {e}")
            # Tạo ảnh nền mặc định màu xanh
            self.background_image = np.zeros((480, 640, 3), dtype=np.uint8)
            self.background_image[:] = (255, 0, 0)  # Màu xanh lam
    
    def apply_background_effect(self, frame):
        # Chuyển đổi màu từ BGR sang RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Áp dụng selfie segmentation
        results = self.selfie_segmentation.process(frame_rgb)
        
        # Lấy mask
        segmentation_mask = results.segmentation_mask
        
        # Áp dụng ngưỡng để có mask nhị phân
        condition = np.stack((segmentation_mask,) * 3, axis=-1) > 0.5
        
        # Tạo background dựa trên chế độ đã chọn
        if self.background_mode == BACKGROUND_MODES["BLUR"]:
            # Làm mờ nền
            background = cv2.GaussianBlur(frame, (55, 55), 0)
        elif self.background_mode == BACKGROUND_MODES["REPLACE"]:
            # Thay thế nền
            background = cv2.resize(self.background_image, (frame.shape[1], frame.shape[0]))
        elif self.background_mode == BACKGROUND_MODES["GRAYSCALE"]:
            # Chuyển nền thành grayscale
            background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            background = cv2.cvtColor(background, cv2.COLOR_GRAY2BGR)
        elif self.background_mode == BACKGROUND_MODES["VIRTUAL_BG"]:
            # Ảo ảnh nền (màu xanh lá)
            background = np.zeros_like(frame)
            background[:] = (0, 255, 0)  # Màu xanh lá
        
        # Kết hợp foreground và background
        output_image = np.where(condition, frame, background)
        
        return output_image
    
    def run(self):
        print("""
        Hướng dẫn sử dụng:
        - Nhấn 'b' để chuyển chế độ làm mờ nền
        - Nhấn 'r' để chuyển chế độ thay thế nền
        - Nhấn 'g' để chuyển chế độ grayscale nền
        - Nhấn 'v' để chuyển chế độ nền ảo (xanh lá)
        - Nhấn 'q' để thoát
        """)
        
        while True:
            ret, frame = self.cap.read()
            if not ret:
                break
            
            # Lật frame để có hiệu ứng gương
            frame = cv2.flip(frame, 1)
            
            # Áp dụng hiệu ứng nền
            result = self.apply_background_effect(frame)
            
            # Hiển thị kết quả
            cv2.imshow('Background Effect - Improved', result)
            
            # Xử lý phím nhấn
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('b'):
                self.background_mode = BACKGROUND_MODES["BLUR"]
                print("Chế độ: Làm mờ nền")
            elif key == ord('r'):
                self.background_mode = BACKGROUND_MODES["REPLACE"]
                print("Chế độ: Thay thế nền")
            elif key == ord('g'):
                self.background_mode = BACKGROUND_MODES["GRAYSCALE"]
                print("Chế độ: Grayscale nền")
            elif key == ord('v'):
                self.background_mode = BACKGROUND_MODES["VIRTUAL_BG"]
                print("Chế độ: Nền ảo (xanh lá)")
        
        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    effect = ImprovedBackgroundEffect()
    effect.run()