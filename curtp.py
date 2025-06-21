import ctypes
import random
import time

import keyboard
import pyautogui

# Constants for mouse events
MOUSEEVENTF_MOVE         = 0x0001
MOUSEEVENTF_LEFTDOWN     = 0x0002
MOUSEEVENTF_LEFTUP       = 0x0004
MOUSEEVENTF_RIGHTDOWN    = 0x0008
MOUSEEVENTF_RIGHTUP      = 0x0010
MOUSEEVENTF_MIDDLEDOWN   = 0x0020
MOUSEEVENTF_MIDDLEUP     = 0x0040
MOUSEEVENTF_WHEEL        = 0x0800  # Vertical scroll
MOUSEEVENTF_HWHEEL       = 0x01000 # Horizontal scroll
VK_PRIOR = 0x21  # Page Up
VK_NEXT  = 0x22  # Page Down
KEYEVENTF_KEYUP = 0x0002

class Keyboard:
    def __init__(self):
        print(self)

    def sskp(self, key="a"):
        pyautogui.press('a')  # Presses the 'a' key

    def skc(self, key="ctrl+c"):
        a = key.split("+")
        pyautogui.hotkey(*a)

    def s(self, sen="Hello, how are you today?", interval=0.05):
        pyautogui.write(sen, interval=interval)

class Mouse:
    def __init__(self):
        self.x = 0
        self.y = 0

    def move(self, x=None, y=None):
        """Move the mouse to (x, y), or random if not provided."""
        if x is None:
            x = random.randint(0, 1920)
        if y is None:
            y = random.randint(0, 1080)

        self.x = int(x)
        self.y = int(y)
        ctypes.windll.user32.SetCursorPos(self.x, self.y)

    def smooth_move(self, x, y, duration=0.5, steps=50):
        """Smoothly move the mouse from current position to (x, y)."""

        # Define POINT structure for cursor position
        class POINT(ctypes.Structure):
            _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]

        pt = POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
        start_x, start_y = pt.x, pt.y
        end_x, end_y = int(x), int(y)

        for i in range(1, steps + 1):
            t = i / steps
            intermediate_x = int(start_x + (end_x - start_x) * t)
            intermediate_y = int(start_y + (end_y - start_y) * t)
            ctypes.windll.user32.SetCursorPos(intermediate_x, intermediate_y)
            time.sleep(duration / steps)

        self.x, self.y = end_x, end_y

    def click(self, button="left"):
        """Perform a mouse click. Supports left, right, and middle."""
        if button == "left":
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, self.x, self.y, 0, 0)
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, self.x, self.y, 0, 0)
        elif button == "right":
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTDOWN, self.x, self.y, 0, 0)
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_RIGHTUP, self.x, self.y, 0, 0)
        elif button == "middle":
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_MIDDLEDOWN, self.x, self.y, 0, 0)
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_MIDDLEUP, self.x, self.y, 0, 0)
        else:
            raise ValueError("button must be 'left', 'right', or 'middle'")

    def drag_and_drop(self, to_x, to_y, duration=0.5, steps=50):
        """Drag from current position to (to_x, to_y) using smooth motion."""
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, self.x, self.y, 0, 0)
        self.smooth_move(to_x, to_y, duration=duration, steps=steps)
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, self.x, self.y, 0, 0)

    def scroll(self, amount=1, upordown="up", speed=0):
        """
        Scroll the mouse wheel vertically.

        :param amount: Number of notches to scroll. 1 = standard single scroll.
        :param upordown: 'up' or 'down'
        :param speed: Delay (ms) between scroll steps, if multiple notches
        """
        delta = 120 if upordown.lower() == "up" else -120
        for _ in range(abs(amount)):
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_WHEEL, 0, 0, delta, 0)
            if speed > 0:
                time.sleep(speed / 1000.0)

    def scroll_horizontal(self, amount=1, direction="right", speed=0):
        """
        Scroll the mouse wheel horizontally.

        :param amount: Number of notches to scroll. 1 = standard single scroll.
        :param direction: 'left' or 'right'
        :param speed: Delay (ms) between scroll steps, if multiple notches
        """
        delta = 120 if direction.lower() == "right" else -120
        for _ in range(abs(amount)):
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_HWHEEL, 0, 0, delta, 0)
            if speed > 0:
                time.sleep(speed / 1000.0)

    def smooth_scroll(self, amount=1, upordown="up", duration=0.5):
        """
        Smoothly scrolls the mouse vertically over time.

        :param amount: Number of scroll notches (positive integer).
        :param upordown: 'up' or 'down'
        :param duration: Total time (in seconds) for the scroll
        """
        delta = 120 if upordown.lower() == "up" else -120
        delay = duration / amount if amount > 0 else 0

        for _ in range(abs(amount)):
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_WHEEL, 0, 0, delta, 0)
            time.sleep(delay)

    def smooth_scroll_horizontal(self, amount=1, direction="right", duration=0.5):
        """
        Smoothly scrolls the mouse horizontally over time.

        :param amount: Number of scroll notches (positive integer).
        :param direction: 'left' or 'right'
        :param duration: Total time (in seconds) for the scroll
        """
        delta = 120 if direction.lower() == "right" else -120
        delay = duration / amount if amount > 0 else 0

        for _ in range(abs(amount)):
            ctypes.windll.user32.mouse_event(MOUSEEVENTF_HWHEEL, 0, 0, delta, 0)
            time.sleep(delay)

    def press_key(self, vk_code):
        """Simulates a key press and release of a virtual key code."""
        ctypes.windll.user32.keybd_event(vk_code, 0, 0, 0)
        time.sleep(0.05)  # Brief delay to simulate real press
        ctypes.windll.user32.keybd_event(vk_code, 0, KEYEVENTF_KEYUP, 0)

    def page_up(self):
        """Simulate Page Up key press."""
        self.press_key(VK_PRIOR)

    def page_down(self):
        """Simulate Page Down key press."""
        self.press_key(VK_NEXT)

    def smooth_page_up(self, steps=3, delay=0.3):
        """
        Simulates smooth Page Up scrolling.
        :param steps: Number of Page Up presses.
        :param delay: Time in seconds between each press.
        """
        for _ in range(steps):
            self.press_key(VK_PRIOR)
            time.sleep(delay)

    def smooth_page_down(self, steps=3, delay=0.3):
        """
        Simulates smooth Page Down scrolling.
        :param steps: Number of Page Down presses.
        :param delay: Time in seconds between each press.
        """
        for _ in range(steps):
            self.press_key(VK_NEXT)
            time.sleep(delay)



# Optional usage
if __name__ == "__main__":
    m = Mouse()
    key = Keyboard()

    time.sleep(3)
    key.s()
    key.skc(key="enter")
    time.sleep(0.5)
