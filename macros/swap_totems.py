import time

import pyautogui


GEM1_POS = (1375, 275)
GEM2_POS = (1560, 275)


pyautogui.write("ix")
time.sleep(0.1)
pyautogui.moveTo(*GEM1_POS, duration=0.2)
pyautogui.click(button="right")
pyautogui.moveTo(*GEM2_POS, duration=0.2)
pyautogui.click(button="left")
pyautogui.moveTo(*GEM1_POS, duration=0.2)
pyautogui.click(button="left")
time.sleep(0.1)
pyautogui.write("xi")
