"""
코드 실행 전 할일 :
1. capture_all.py 를 통해 화면 전체를 캡쳐한다.
2. image_cropper.py 를 통해 원하는 강수의 템플릿 이미지를 크롭한다. e.g.,[+17] 
3. 이 코드에 TPL_PATH (템플릿 패스) 에 해당 이미지 경로를 넣는다. 
4. POINTS 에 1) 특수기호 2) / 3) /강화 4) 보내기 버튼의 위치를 차례로 넣는다. (개발자 모드 진입 후 포인트 위치 확인 켜기)
5. 템플릿을 찾을 위치를 ROI 에 지정해놓고, 해당 위치가 맞는지 capture.py 에 넣고 확인해본다.
"""

import subprocess, time
import cv2
import numpy as np

# ================= 설정 =================
TPL_PATH = "target_number.png"
THRESH = 0.93

# [+16] 표시 ROI (x1, y1, x2, y2)
X1, Y1, X2, Y2 = 172, 760, 320, 1030

# 순차 탭할 포인트들
POINTS = [
    (100, 2100),
    (500, 1650),
    (500, 888),
    (990, 1378),
]

DELAY_BETWEEN_TAPS = 0.12   # 포인트 사이
CYCLE_SLEEP = 1             # 한 사이클 끝나고 대기
# ======================================

def screencap():
    return subprocess.check_output(["adb", "exec-out", "screencap", "-p"])

def decode(png):
    return cv2.imdecode(np.frombuffer(png, np.uint8), cv2.IMREAD_COLOR)

def tap(x, y):
    subprocess.run(["adb", "shell", "input", "tap", str(x), str(y)], check=False)

tpl = cv2.imread(TPL_PATH, cv2.IMREAD_GRAYSCALE)
if tpl is None:
    raise FileNotFoundError(TPL_PATH)

print("[START] auto enhance")

while True:
    # 1) 강화 수치 체크
    img = decode(screencap())
    if img is None:
        continue

    roi = img[Y1:Y2, X1:X2]
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray, tpl, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)

    if max_val >= THRESH:
        cv2.imwrite("debug_roi.png", roi)
        print(f"[STOP] [+16] detected (score={max_val:.3f})")
        break

    # 2) 아직 아니면 → 포인트 순차 탭
    for x, y in POINTS:
        tap(x, y)
        time.sleep(DELAY_BETWEEN_TAPS)

    time.sleep(CYCLE_SLEEP)
