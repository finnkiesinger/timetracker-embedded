from lcd_util import LcdUtil
from nfc_util import NfcUtil
from rgb_util import RgbUtil
from socket_client import WebsocketClient
from time import sleep
import socketio

client = WebsocketClient("ws://localhost:3002")
lcd_util = LcdUtil()
lcd_util.clear()
lcd_util.write_first_line("Bereit")
nfc_util = NfcUtil()
rgb_util = RgbUtil()

response = None


def handle_scan_result(message):
    global response
    response = message


client.add_callback("scan", handle_scan_result)
client.add_callback("change", handle_scan_result)
while True:
    try:
        client.connect()
        break
    except socketio.exceptions.ConnectionError as err:
        print("ConnectionError: %s", err)
        sleep(1)
lcd_util.write_first_line("Bereit")
print("ready")

while True:
    lines = nfc_util.read_nfc()
    unfiltered = str(lines).split("\\n")
    uid = None
    for line in unfiltered:
        if line.strip().startswith("UID"):
            rgb_util.set_brightness(2, 100)
            uid = line.strip().split(": ")[1].replace(" ", "")

    if uid is None:
        continue

    lcd_util.write_first_line("Bitte warten...")
    client.emit("card_read", uid)
    while response is None:
        sleep(0.05)
    sleep(1)

    if type(response) is str:
        if response == 'not_found':
            rgb_util.set_brightness(2, 0)
            rgb_util.set_brightness(1, 0)
            rgb_util.set_brightness(0, 100)
            lcd_util.write_first_line("Nicht gefunden")
    elif type(response) is dict:
        rgb_util.set_brightness(2, 0)
        rgb_util.set_brightness(0, 0)
        rgb_util.set_brightness(1, 100)
        if response["action"] == "started":
            lcd_util.write_first_line("Angemeldet:")
        if response["action"] == "ended":
            lcd_util.write_first_line("Abgemeldet:")
        lcd_util.write_second_line(response["username"])
    sleep(3)
    rgb_util.turn_off()
    lcd_util.write_first_line("Bereit")
    lcd_util.write_second_line("")
