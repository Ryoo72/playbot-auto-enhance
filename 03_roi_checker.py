"""
내가 찾은 ROI 가 맞는지 확인하는 코드.
(개발자 옵션 > 입력 > 포인터 위치 를 켜놓고 찾으면 편리합니다.)
"""
import subprocess
import cv2
import numpy as np

# ROI
X1, Y1, X2, Y2 = 172, 760, 320, 1030

# 1. adb screencap (PNG 바이너리 받기)
raw = subprocess.check_output(
    ["adb", "exec-out", "screencap", "-p"]
)

# 2. PNG → OpenCV 이미지
img = cv2.imdecode(
    np.frombuffer(raw, np.uint8),
    cv2.IMREAD_COLOR
)

# 3. ROI crop
roi = img[Y1:Y2, X1:X2]

# 4. 저장 + 확인
cv2.imwrite("roi_check.png", roi)
cv2.imshow("ROI CHECK", roi)
cv2.waitKey(0)
cv2.destroyAllWindows()
