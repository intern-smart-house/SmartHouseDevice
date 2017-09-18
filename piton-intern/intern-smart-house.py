import websocket
import json
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)  # set board mode to Broadcom

GPIO.setup(17, GPIO.OUT)  # set up pin 17 TV
GPIO.setup(18, GPIO.OUT)  # set up pin 18 Lights
GPIO.setup(22, GPIO.OUT)  # set up pin 12 A/C
GPIO.setup(27, GPIO.OUT)  # set up pin 27 Alarm


GPIO.output(17, 0)  # turn off pin 17
GPIO.output(18, 0)  # turn off pin 18
GPIO.output(22, 0)  # turn off pin 22
GPIO.output(27, 0)  # turn off pin 27


class Payload(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)

def ws_uri():
    return "wss://smarthouseintern.azurewebsites.net/ws"

def ws_on_message(ws, msg):
    message = str(Payload(msg).data).lower()

    if message != "":
        if "tv" in message or "television" in message:
            if "open" in message or "on" in message or "opened" in message:
                print("TV Opened!!")
                GPIO.output(17, 1)  # turn on pin 17

            if "close" in message or "off" in message or "closed" in message:
                print("TV Closed!!")
                GPIO.output(17, 0)  # turn off pin 17

        if "light" in message or "lights" in message:
            if "open" in message or "on" in message or "opened" in message:
                print("Lights Opened!!")
                GPIO.output(18, 1)  # turn on pin 18
            if "close" in message or "off" in message or "closed" in message:
                print("Lights Closed!!")
                GPIO.output(18, 0)  # turn off pin 18

        if "ac" in message or "air" in message or "condition" in message or "conditioner" in message:
            if "open" in message or "on" in message or "opened" in message:
                print("ac Opened!!")
                GPIO.output(22, 1)  # turn on pin 22
            if "close" in message or "off" in message or "closed" in message:
                print("ac Closed!!")
                GPIO.output(22, 0)  # turn off pin 22
                
        if "alarm" in message or "alarms" in message:
            if "open" in message or "on" in message or "opened" in message:
                print("alarm Opened!!")
                GPIO.output(27, 1)  # turn on pin 27
            if "close" in message or "off" in message or "closed" in message:
                print("alarm Closed!!")
                GPIO.output(27, 0)  # turn off pin 27
        
        if "all" in message or "whole" in message:
            if "open" in message or "on" in message or "opened" in message:
                print("All Opened!!")
                GPIO.output(17, 1)  # turn on pin 17
                GPIO.output(18, 1)  # turn on pin 18
                GPIO.output(22, 1)  # turn on pin 22
                GPIO.output(27, 1)  # turn on pin 27
            if "close" in message or "off" in message or "closed" in message:
                print("All Closed!!")
                GPIO.output(17, 0)  # turn off pin 17
                GPIO.output(18, 0)  # turn off pin 18
                GPIO.output(22, 0)  # turn off pin 22
                GPIO.output(27, 0)  # turn off pin 27


def ws_on_error(ws, err):
    print(err)

def ws_on_open(ws):
    print("### WebSocket Opened ###")


def ws_on_close(ws):
    print("### WebSocket Closed ###")


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(ws_uri(), 
                                on_message = ws_on_message,
                                on_close = ws_on_close,
                                on_error = ws_on_error)
    ws.on_open = ws_on_open
    ws.run_forever()