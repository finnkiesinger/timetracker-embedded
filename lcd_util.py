#!/usr/bin/python
import time
import RPi.GPIO as GPIO

LCD_RS = 7
LCD_E = 11
LCD_DATA4 = 12
LCD_DATA5 = 15
LCD_DATA6 = 16
LCD_DATA7 = 18

LCD_WIDTH = 16
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0
LCD_CHR = GPIO.HIGH
LCD_CMD = GPIO.LOW
E_PULSE = 0.0005
E_DELAY = 0.0005


class LcdUtil():
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(LCD_E, GPIO.OUT)
        GPIO.setup(LCD_RS, GPIO.OUT)
        GPIO.setup(LCD_DATA4, GPIO.OUT)
        GPIO.setup(LCD_DATA5, GPIO.OUT)
        GPIO.setup(LCD_DATA6, GPIO.OUT)
        GPIO.setup(LCD_DATA7, GPIO.OUT)

        self.display_init()

    def write_first_line(self, message):
        self.lcd_send_byte(LCD_LINE_1, LCD_CMD)
        self.lcd_message(message)

    def write_second_line(self, message):
        self.lcd_send_byte(LCD_LINE_2, LCD_CMD)
        self.lcd_message(message)

    def clear(self):
        self.lcd_send_byte(LCD_LINE_1, LCD_CMD)
        self.lcd_message("")
        self.lcd_send_byte(LCD_LINE_2, LCD_CMD)
        self.lcd_message("")

    def lcd_send_byte(self, bits, mode):
        GPIO.output(LCD_RS, mode)
        GPIO.output(LCD_DATA4, GPIO.LOW)
        GPIO.output(LCD_DATA5, GPIO.LOW)
        GPIO.output(LCD_DATA6, GPIO.LOW)
        GPIO.output(LCD_DATA7, GPIO.LOW)
        if bits & 0x10 == 0x10:
            GPIO.output(LCD_DATA4, GPIO.HIGH)
        if bits & 0x20 == 0x20:
            GPIO.output(LCD_DATA5, GPIO.HIGH)
        if bits & 0x40 == 0x40:
            GPIO.output(LCD_DATA6, GPIO.HIGH)
        if bits & 0x80 == 0x80:
            GPIO.output(LCD_DATA7, GPIO.HIGH)
        time.sleep(E_DELAY)
        GPIO.output(LCD_E, GPIO.HIGH)
        time.sleep(E_PULSE)
        GPIO.output(LCD_E, GPIO.LOW)
        time.sleep(E_DELAY)
        GPIO.output(LCD_DATA4, GPIO.LOW)
        GPIO.output(LCD_DATA5, GPIO.LOW)
        GPIO.output(LCD_DATA6, GPIO.LOW)
        GPIO.output(LCD_DATA7, GPIO.LOW)
        if bits & 0x01 == 0x01:
            GPIO.output(LCD_DATA4, GPIO.HIGH)
        if bits & 0x02 == 0x02:
            GPIO.output(LCD_DATA5, GPIO.HIGH)
        if bits & 0x04 == 0x04:
            GPIO.output(LCD_DATA6, GPIO.HIGH)
        if bits & 0x08 == 0x08:
            GPIO.output(LCD_DATA7, GPIO.HIGH)
        time.sleep(E_DELAY)
        GPIO.output(LCD_E, GPIO.HIGH)
        time.sleep(E_PULSE)
        GPIO.output(LCD_E, GPIO.LOW)
        time.sleep(E_DELAY)

    def lcd_message(self, message):
        message = message.ljust(LCD_WIDTH, " ")
        for i in range(LCD_WIDTH):
            self.lcd_send_byte(ord(message[i]), LCD_CHR)

    def display_init(self):
        self.lcd_send_byte(0x33, LCD_CMD)
        self.lcd_send_byte(0x32, LCD_CMD)
        self.lcd_send_byte(0x28, LCD_CMD)
        self.lcd_send_byte(0x0C, LCD_CMD)
        self.lcd_send_byte(0x06, LCD_CMD)
        self.lcd_send_byte(0x01, LCD_CMD)
