import cv2
import pyautogui
from PIL import ImageGrab
import time
from logging import getLogger, Formatter, StreamHandler, INFO
import os

WORKSPACE_PATH = os.path.dirname(os.path.abspath(__file__)).strip("code")
IMG_PATH = WORKSPACE_PATH + "src\\"

class ImageOperation(object):
    def __init__(self, base_dir=''):
        self.base_dir = base_dir
        self.logger = CommonLogger().common_logger()

    def open_img(self, filename):
        img = cv2.imread(IMG_PATH + self.base_dir + filename, 0)
        return img

    def match_img(self, src_imgname, timeout=10, pass_rate=0.9, get_val=True):
        if isinstance(src_imgname, str):
            src_list = [src_imgname]
        else:
            src_list = src_imgname
        src_img_list = []
        for src_name in src_list:
            self.logger.info(src_name)
            src_img = self.open_img(src_name)
            img_shape = self.get_shape(src_img)
            src_img_list.append([src_img, img_shape])
        #if get_val:
        for i in range(timeout):
            capture = self.get_capture()
            img_num = 0
            for src_img, img_shape in src_img_list:
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
                    #self.logger.info(type(src_imgname))
                    if isinstance(src_imgname, list):
                        res = [img_num, c_loc]
                        self.logger.info(res)
                        return res
                    return c_loc
                img_num += 1
            time.sleep(0.7)
        if isinstance(src_imgname, list):
            return [-1, False]
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
            pyautogui.moveTo(location[0], location[1])
            time.sleep(0.1)
            pyautogui.click()
            time.sleep(0.7)
            # pyautogui.click(location[0], location[1])
            #time.sleep(1)
        self.cursor_out()

    def cursor_out(self):
        pyautogui.moveTo(1, 1)

    def drag(self, f_loc, t_loc):
        pyautogui.mouseDown(f_loc[0], f_loc[1])
        pyautogui.moveTo(t_loc[0], t_loc[1])
        pyautogui.mouseUp()
        time.sleep(1)
        self.cursor_out()

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
