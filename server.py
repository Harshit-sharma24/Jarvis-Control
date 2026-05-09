from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import urllib.parse
import pyautogui
import time
import io
import subprocess
import mss
from PIL import Image


pyautogui.FAILSAFE = False

SECRET_KEY = "1234"

class MyHandler(BaseHTTPRequestHandler):

    def _send(self, msg="OK"):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(msg.encode())

    def do_GET(self):

        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        key = query.get("key", [""])[0]

        if path != "/" and key != SECRET_KEY:
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b"Unauthorized")
            return

        try:

            # ================= HOME =================
            if path == "/":
                self._send("Jarvis Running")
                return

            # ================= BASIC =================
            elif path == "/chrome":
                os.system("start chrome")
                self._send("Chrome Opened")

            elif path == "/music":
                os.system("start wmplayer")
                self._send("Music Playing")

            elif path == "/shutdown":
                os.system("shutdown /s /t 1")
                self._send("Shutdown")

            elif path == "/lock":
                os.system("rundll32.exe user32.dll,LockWorkStation")
                self._send("Locked")

            # ================= FILE =================
            elif path == "/downloads":
                os.system("start %USERPROFILE%\\Downloads")
                self._send("Downloads")

            elif path == "/documents":
                os.system("start %USERPROFILE%\\Documents")
                self._send("Documents")

            # ================= SOUND =================
            elif path == "/volume_up":
                os.system("nircmd.exe changesysvolume 2000")
                self._send("Volume Up")

            elif path == "/volume_down":
                os.system("nircmd.exe changesysvolume -2000")
                self._send("Volume Down")

            elif path == "/mute":
                os.system("nircmd.exe mutesysvolume 2")
                self._send("Muted")

            # ================= BRIGHTNESS (FIXED 💡) =================
            elif path == "/brightness_low":
                subprocess.run([
                    "powershell",
                    "-Command",
                    "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,30)"
                ])
                self._send("Brightness Low")

            elif path == "/brightness_high":
                subprocess.run([
                    "powershell",
                    "-Command",
                    "(Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,100)"
                ])
                self._send("Brightness High")
                
            elif path == "/screenshot":
                filename = f"screenshot_{int(time.time())}.png"
                filepath = os.path.join(os.getcwd(), filename)

                img = pyautogui.screenshot()
                img.save(filepath)

                print("📸 Saved:", filepath)
                self._send(f"Saved: {filename}")


            # ================= TOUCHPAD =================
            elif path == "/move":
                x = int(query.get("x", [0])[0])
                y = int(query.get("y", [0])[0])

                # smooth + fast
                pyautogui.moveRel(x * 3, y * 3, duration=0)
                self._send(f"Moved {x},{y}")

            # ================= DRAG =================
            elif path == "/drag_start":
                pyautogui.mouseDown()
                self._send("Drag Start")

            elif path == "/drag_end":
                pyautogui.mouseUp()
                self._send("Drag End")

            # ================= SCROLL =================
            elif path == "/scroll":
                amt = int(query.get("amt", [0])[0])
                pyautogui.scroll(amt)
                self._send(f"Scrolled {amt}")

            # ================= MOUSE =================
            elif path == "/mouse_left":
                pyautogui.click()
                self._send("Left Click")

            elif path == "/mouse_right":
                pyautogui.rightClick()
                self._send("Right Click")

            elif path == "/double_click":
                pyautogui.doubleClick()
                self._send("Double Click")

            # ================= KEYBOARD =================
            elif path == "/enter":
                pyautogui.press("enter")
                self._send("Enter Pressed")

            elif path == "/space":
                pyautogui.press("space")
                self._send("Space Pressed")

            # ================= REAL-TIME TYPING 🔥 =================
            elif path == "/type":
                text = query.get("text", [""])[0]
                text = urllib.parse.unquote(text)

                # instant typing (no delay)
                pyautogui.write(text, interval=0)
                self._send("Typed")

           
           # ===== 🔥 SAFE HOTKEYS =====

            elif path == "/copy":
                time.sleep(0.2)
                pyautogui.hotkey("ctrl", "c")
                self._send("Copied")
            
            elif path == "/paste":
                time.sleep(0.2)
                pyautogui.hotkey("ctrl", "v")
                self._send("Pasted")
            
            elif path == "/cut":
                time.sleep(0.2)
                pyautogui.hotkey("ctrl", "x")
                self._send("Cut")
            
            elif path == "/select_all":
                time.sleep(0.2)
                pyautogui.hotkey("ctrl", "a")
                self._send("Selected All")
            
            elif path == "/alt_tab":
                pyautogui.keyDown("alt")
                pyautogui.press("tab")
                time.sleep(0.2)
                pyautogui.keyUp("alt")
                self._send("Switched App")
            
            # ================= APPS =================
            elif path == "/notepad":
                os.system("start notepad")
                self._send("Notepad Opened")

            elif path == "/calc":
                os.system("start calc")
                self._send("Calculator Opened")

            # ================= CLEAN =================
            elif path == "/clean":
                os.system("del /q/f/s %TEMP%\\*")
                self._send("Cleaned")

                 # ===== 🔥 LIVE SCREEN =====
            # ================= LIVE SCREEN HD =================
            elif path == "/screen":

                with mss.mss() as sct:

                    monitor = sct.monitors[1]

                    shot = sct.grab(monitor)

                    img = Image.frombytes(
                        "RGB",
                        shot.size,
                        shot.rgb
                    )

                    # HD resize
                    img = img.resize((1366, 768))

                    buffer = io.BytesIO()

                    img.save(
                        buffer,
                        format="JPEG",
                        quality=85,
                        optimize=True
                    )

                    buffer.seek(0)

                    self.send_response(200)
                    self.send_header("Content-type", "image/jpeg")
                    self.end_headers()

                    self.wfile.write(buffer.read())

            # ================= UNKNOWN =================
            else:
                self._send("Unknown Command")

        except Exception as e:

            print("❌ ERROR:", str(e))

            self._send("Error: " + str(e))


# ================= START =================
server = HTTPServer(("0.0.0.0", 8000), MyHandler)
print("🚀 Jarvis Running on http://0.0.0.0:8000")
server.serve_forever()