"""
2. 원하는 곳 크롭하기. (흰 배경에 "[+17]" 이 표시된 영역을 크롭하세요.)
"""
import cv2

IMG_PATH = "roi_check.png"   # 자를 원본 이미지
OUT_PATH = "template_16_real.png" # 저장될 템플릿

img = cv2.imread(IMG_PATH)
if img is None:
    raise FileNotFoundError(IMG_PATH)

# 마우스로 드래그 → Enter 누르면 확정
r = cv2.selectROI("select template", img, showCrosshair=True, fromCenter=False)
cv2.destroyAllWindows()

x, y, w, h = map(int, r)
crop = img[y:y+h, x:x+w]

cv2.imwrite(OUT_PATH, crop)
print("saved:", OUT_PATH)
