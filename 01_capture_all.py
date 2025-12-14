"""
1. 화면 전체 캡쳐하기. (원하는 강화수가 표시된 화면을 띄워놓고 캡쳐하세요.)
"""
import subprocess
from datetime import datetime

def adb_full_screencap(path):
    png = subprocess.check_output(["adb", "exec-out", "screencap", "-p"])
    with open(path, "wb") as f:
        f.write(png)

if __name__ == "__main__":
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out = f"screen_{ts}.png"
    adb_full_screencap(out)
    print("saved:", out)
