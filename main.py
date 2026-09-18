# this python script allows you to play minecraft with a thrustmaster t80 steering wheel btw

import pygame
import pyautogui
import time
import ctypes

pygame.init()
pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("No controller found.")
    input("Press Enter to exit...")
    raise SystemExit

wheel = pygame.joystick.Joystick(0)
wheel.init()

STEERING_AXIS = 0

D_BUTTON = 1
A_BUTTON = 2
W_BUTTON = 3
S_BUTTON = 0

LEFT_CLICK_BUTTON = 9
RIGHT_CLICK_BUTTON = 10

UP_BUTTON = 8
DOWN_BUTTON = 7

SCROLL_UP_BUTTON = 6
SCROLL_DOWN_BUTTON = 5

STEERING_SENSITIVITY = 25
VERTICAL_SENSITIVITY = 20
SCROLL_AMOUNT = 1
DEADZONE = 0.05

pyautogui.PAUSE = 0

left_pressed = False
right_pressed = False

MOUSEEVENTF_MOVE = 0x0001

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("mi", MOUSEINPUT)
    ]

def move_mouse(dx, dy):
    extra = ctypes.c_ulong(0)

    mouse_input = MOUSEINPUT(
        int(dx),
        int(dy),
        0,
        MOUSEEVENTF_MOVE,
        0,
        ctypes.pointer(extra)
    )

    input_data = INPUT(
        0,
        mouse_input
    )

    ctypes.windll.user32.SendInput(
        1,
        ctypes.byref(input_data),
        ctypes.sizeof(input_data)
    )

print("T80 Minecraft controller active.")
print("Steering = look left/right")
print("Button 8 = look up")
print("Button 7 = look down")
print("Button 1 = W")
print("Button 2 = A")
print("Button 3 = S")
print("Button 4 = D")
print("Left paddle = left click")
print("Right paddle = right click")
print("Button 6 = scroll up")
print("Button 5 = scroll down")
print("Press Ctrl+C to stop.")

try:
    while True:
        pygame.event.pump()

        steering = wheel.get_axis(STEERING_AXIS)

        if abs(steering) < DEADZONE:
            steering = 0

        mouse_x = steering * STEERING_SENSITIVITY
        mouse_y = 0

        if wheel.get_button(UP_BUTTON):
            mouse_y -= VERTICAL_SENSITIVITY

        if wheel.get_button(DOWN_BUTTON):
            mouse_y += VERTICAL_SENSITIVITY

        if mouse_x != 0 or mouse_y != 0:
            move_mouse(mouse_x, mouse_y)

        left = wheel.get_button(LEFT_CLICK_BUTTON)
        right = wheel.get_button(RIGHT_CLICK_BUTTON)

        if left and not left_pressed:
            pyautogui.click(button="left")

        if right and not right_pressed:
            pyautogui.click(button="right")

        if wheel.get_button(SCROLL_UP_BUTTON):
            pyautogui.scroll(SCROLL_AMOUNT)

        if wheel.get_button(SCROLL_DOWN_BUTTON):
            pyautogui.scroll(-SCROLL_AMOUNT)

        keys = {
            W_BUTTON: "w",
            A_BUTTON: "a",
            S_BUTTON: "s",
            D_BUTTON: "d"
        }

        for button, key in keys.items():
            if wheel.get_button(button):
                pyautogui.keyDown(key)
            else:
                pyautogui.keyUp(key)

        left_pressed = left
        right_pressed = right

        time.sleep(0.01)

except KeyboardInterrupt:
    pass

finally:
    for key in ("w", "a", "s", "d"):
        pyautogui.keyUp(key)

    pygame.quit()
