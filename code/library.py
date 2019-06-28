import cv2
import pyautogui
from PIL import ImageGrab
import time
from logging import getLogger, Formatter, StreamHandler, INFO
import os

WORKSPACE_PATH = os.path.dirname(os.path.abspath(__file__))
IMG_PATH = WORKSPACE_PATH + "\\horiishu\\src\\"

class ImageOperation(object):
    def open_img(self, filename):
        img = cv2.imread(IMG_PATH + filename, 0)
        return img

    def match_img(self, src_name, timeout=10, pass_rate=0.9, get_val=False):
        src_img = self.open_img(src_name)
        img_shape = self.get_shape(src_img)
        for i in range(timeout):
            capture = self.get_capture()
            result = cv2.matchTemplate(capture, src_img, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if get_val:
                print("max: ", end="")
                print(max_val, max_loc)
            if max_val > pass_rate:
                c_loc = (max_loc[0] + img_shape[1] / 2,
                         max_loc[1] + img_shape[0] / 2)
                if get_val:
                    print("center: ", end="")
                    print(c_loc)
                return c_loc
            time.sleep(0.7)
        return False

    def get_shape(self, img):
        return img.shape

    def get_capture(self, filename="capture.png"):
        ImageGrab.grab().save(IMG_PATH + filename)
        return self.open_img(filename)

class WindowsGUI(object):
    def click(self, location, time_c=1):
        if not location:
            raise ValueError("'NoneType' object has Detected !!")
        for i in range(time_c):
            pyautogui.click(location[0], location[1])
        self.cursor_out()
        time.sleep(1)

    def cursor_out(self):
        pyautogui.moveTo(1, 1)

    def refresh(self):
        pyautogui.click(85, 50)

class CommonLogger(object):
    logger = getLogger(__name__)
    handler = StreamHandler()
    formatter = Formatter('%(asctime)s - [%(levelname)s][%(module)s][%(funcName)s] %(message)s', "%H:%M")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(INFO)
    logger.addHandler(handler)

    def common_logger(self):
        return self.logger
