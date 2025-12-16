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
TPL_PATH = "template_16_real.png"
THRESH = 0.95

POINTS = [
    (100, 2100),
    (500, 1650),
    (500, 888),
    (990, 1378),
]

DELAY_BETWEEN_TAPS = 0.12
CYCLE_SLEEP = 1
# ======================================

def beep():
    # macOS 기본 시스템 사운드
    subprocess.run(
        ["afplay", "/System/Library/Sounds/Glass.aiff"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

def screencap():
    return subprocess.check_output(["adb", "exec-out", "screencap", "-p"])

def decode(png):
    return cv2.imdecode(np.frombuffer(png, np.uint8), cv2.IMREAD_COLOR)

def tap(x, y):
    subprocess.run(["adb", "shell", "input", "tap", str(x), str(y)], check=False)

tpl = cv2.imread(TPL_PATH, cv2.IMREAD_GRAYSCALE)
if tpl is None:
    raise FileNotFoundError(TPL_PATH)
th, tw = tpl.shape[:2]

print("[START] auto enhance")
while True:
    img = decode(screencap())
    if img is None:
        continue

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    res = cv2.matchTemplate(gray, tpl, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(res)

    if max_val >= THRESH:
        # 디버그: 매칭 위치 박스 표시
        debug = img.copy()
        x, y = max_loc
        cv2.rectangle(debug, (x, y), (x + tw, y + th), (0, 0, 255), 2)
        cv2.imwrite("debug_full.png", debug)

        for _ in range(3):
            beep()
            time.sleep(0.15)
        print(f"[STOP] [+16] detected (score={max_val:.3f})")
        break

    # 아직 아니면 → 포인트 순차 탭
    for x, y in POINTS:
        tap(x, y)
        time.sleep(DELAY_BETWEEN_TAPS)

    time.sleep(CYCLE_SLEEP)
