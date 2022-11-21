#!/usr/bin/env python3

# Standard
import json
from time import sleep
from datetime import datetime
from pytz import timezone
import time

# Third party
import stomp

# RPi
# from bells_gpio import bell_tapper, up_bell, down_bell

# windows
from bells_windows import bell_tapper, up_bell, down_bell, peg

pause_period = 0.4
pause2_period = 1.0
long_period = 2.5

TIMEZONE_LONDON: timezone = timezone("Europe/London")

# TD message types

C_BERTH_STEP = "CA"       # Berth step      - description moves from "from" berth into "to", "from" berth is erased
C_BERTH_CANCEL = "CB"     # Berth cancel    - description is erased from "from" berth
C_BERTH_INTERPOSE = "CC"  # Berth interpose - description is inserted into the "to" berth, previous contents erased
C_HEARTBEAT = "CT"        # Heartbeat       - sent periodically by a train describer

S_SIGNALLING_UDPATE = "SF"            # Signalling update
S_SIGNALLING_REFRESH = "SG"           # Signalling refresh
S_SIGNALLING_REFRESH_FINISHED = "SH"  # Signalling refresh finished


def print_td_frame(parsed_body):
    # Each message in the queue is a JSON array
    for outer_message in parsed_body:
        # Each list element consists of a dict with a single entry - our real target - e.g. {"CA_MSG": {...}}
        message = list(outer_message.values())[0]

        message_type = message["msg_type"]
        area_id = message["area_id"]

        if area_id == "NM":
            # The feed time is in milliseconds, but python takes timestamps in seconds
            timestamp = int(message["time"]) / 1000
            utc_datetime = datetime.utcfromtimestamp(timestamp)
            uk_datetime = TIMEZONE_LONDON.fromutc(utc_datetime).strftime("%Y-%m-%d %H:%M:%S")

            # For the sake of demonstration, we're only displaying C-trainClass messages
            if message_type in [C_BERTH_STEP, C_BERTH_CANCEL, C_BERTH_INTERPOSE]:
                description = message.get("descr", "")
                from_berth = message.get("from", "")
                to_berth = message.get("to", "")

                if from_berth.startswith('40'):
                    print(f"{uk_datetime} {message_type} {area_id} {description} {from_berth}->{to_berth}")
                    match from_berth:
                        case '4072':
                            print (f"{uk_datetime} Up train {description} near Fiskerton")
                            IsLineClear("rear", "UP", description)
                        case '4062':
                            print (f"{uk_datetime} Up train {description} near Bleasby")
                            TrainEnteringSection("rear", "UP", description)
                            pause2()
                            IsLineClear("advance", "UP", description)
                        case '4050':
                            print (f"{uk_datetime} Up train {description} near Lowdham")
                            TrainEnteringSection("advance", "UP", description)
                            long_pause()
                            TrainOutOfSection("rear", "UP", description)
                        case '4042':
                            print (f"{uk_datetime} Up train {description} near Burton Joyce")
                            TrainOutOfSection("advance", "UP", description)
                        case '4036':
                            print (f"{uk_datetime} Up train {description} near Carlton")

                        case '4037':
                            print (f"{uk_datetime} Down train {description} near Carlton")
                            IsLineClear("rear", "DOWN", description)
                        case '4043':
                            print (f"{uk_datetime} Down train {description} near Burton Joyce")
                            TrainEnteringSection("rear", "DOWN", description)
                            pause2()
                            IsLineClear("advance", "DOWN", description)
                        case '4051':
                            print (f"{uk_datetime} Down train {description} near Lowdham")
                            TrainEnteringSection("advance", "UP", description)
                            long_pause()
                            TrainOutOfSection("rear", "DOWN", description)
                        case '4065':
                            print (f"{uk_datetime} Down train {description} near Bleasby")
                            TrainOutOfSection("advance", "DOWN", description)

            # For the sake of demonstration, we're only displaying C-trainClass messages
            if message_type in [S_SIGNALLING_UDPATE, S_SIGNALLING_REFRESH, S_SIGNALLING_REFRESH_FINISHED]:
                address = message.get("address", "")
                data = message.get("data", "")

                # print(f"{uk_datetime} {message_type} {area_id} {address} {data}")


def IsLineClear(section, line, description):
    trainClass = description[0]
    # trainClass 1: 4
    # trainClass 2: 3-1
    # trainClass 5: 2-2-1
    # trainClass 6: 1-4

    # section 'rear': Train is belled to us, we tap reply and peg up
    # section 'advance: We tap the code, and the reply is belled

    # Line is UP or DOWN

    CallAttention(section, line)
    print(f"Is Line Clear for {description} on {line} (in {section})", end='')

    match trainClass:
        case '1':
            print(" (4)")
            ding(section, line)
            ding(section, line)
            ding(section, line)
            ding(section, line)
            pause2()
            tap(section, line)
            tap(section, line)
            tap(section, line)
            tap(section, line)

        case '2':
            print(" (3-1)")
            ding(section, line)
            ding(section, line)
            ding(section, line)
            pause()
            ding(section, line)
            pause2()
            tap(section, line)
            tap(section, line)
            tap(section, line)
            pause()
            tap(section, line)

        case '5':
            print(" (2-2-1)")
            ding(section, line)
            ding(section, line)
            pause()
            ding(section, line)
            ding(section, line)
            pause()
            ding(section, line)
            pause2()
            tap(section, line)
            tap(section, line)
            pause()
            tap(section, line)
            tap(section, line)
            pause()
            tap(section, line)

        case '6':
            print(" (1-4)")
            ding(section, line)
            pause()
            ding(section, line)
            ding(section, line)
            ding(section, line)
            ding(section, line)
            pause2()
            tap(section, line)
            pause()
            tap(section, line)
            tap(section, line)
            tap(section, line)
            tap(section, line)

        case _:
            print(" (unknown class {trainClass})")

    pause2()
    peg(section, line, 'LC')

def TrainEnteringSection(section, line, description):
    # section 'rear': Train is belled to us, we tap reply and peg up
    # section 'advance: We tap the code, and the reply is belled

    # Line is UP or DOWN

    print(f"Train {description} Entering Section (2) on {line} (in {section})")
    ding(section, line)
    ding(section, line)
    long_pause()
    tap(section, line)
    tap(section, line)
    pause2()
    peg(section, line, 'TOL')

def TrainOutOfSection(section, line, description):
    # section 'rear': Train is belled to us, we tap reply and peg up
    # section 'advance: We tap the code, and the reply is belled

    # Line is UP or DOWN

    CallAttention(section, line)

    print(f"Train {description} Out Of Section (2-1) on {line} (in {section})")
    ding(section, line)
    ding(section, line)
    pause()
    ding(section, line)
    pause2()
    tap(section, line)
    tap(section, line)
    pause()
    tap(section, line)
    pause2()
    peg(section, line, 'NORMAL')

def CallAttention(section, line):
    print(f"Call Attention on {line} (in {section})")
    ding(section, line)
    long_pause()
    tap(section, line)
    pause2()

def ding(section, line):
    # section 'rear': Ring the bell
    # section 'advance: Tap the tapper

    # Line is UP or DOWN
    if section == "rear":
        if line == "UP":
            down_bell()
        else:
            up_bell()
    else:
        bell_tapper()

def tap(section, line):
    # section 'rear': Tap the tapper
    # section 'advance: Ring the bell

    # Line is UP or DOWN
    if section == "advance":
        if line == "UP":
            up_bell()
        else:
            down_bell()
    else:
        bell_tapper()

def pause():
    # short pause between taps, 300ms
    time.sleep(pause_period)

def pause2():
    # Longer pause, say 1 second
    time.sleep(pause2_period)

def long_pause():
    # Time for signalman to get to the bell, say 3 seconds
    time.sleep(long_period)

class Listener(stomp.ConnectionListener):
    _mq: stomp.Connection

    def __init__(self, mq: stomp.Connection):
        self._mq = mq

    def on_message(self, frame):
        headers, message_raw = frame.headers, frame.body
        parsed_body = json.loads(message_raw)

        if headers["destination"].startswith("/topic/TRAIN_MVT_"):
            trust.print_trust_frame(parsed_body)
        elif headers["destination"].startswith("/topic/TD_"):
            print_td_frame(parsed_body)

    def on_error(self, frame):
        print('received an error {}'.format(frame.body))

    def on_disconnected(self):
        print('disconnected')


if __name__ == "__main__":
    with open("secrets.json") as f:
        feed_username, feed_password = json.load(f)

    # https://stomp.github.io/stomp-specification-1.2.html#Heart-beating
    # We're committing to sending and accepting heartbeats every 5000ms
    connection = stomp.Connection([('datafeeds.networkrail.co.uk', 61618)], keepalive=True, heartbeats=(15000, 15000))
    connection.set_listener('', Listener(connection))

    # Connect to feed
    connect_headers = {
        "username": feed_username,
        "passcode": feed_password,
        "wait": True,
        }

    # Subscription
    subscribe_headers = {
        "destination": "/topic/TD_MC_EM_SIG_AREA",
        "id": 1,
        "ack": "auto",
    }

    while 1:
        try:
            # print("Attempting connection")
            connection.connect(**connect_headers)
            connection.subscribe(**subscribe_headers)

            while connection.is_connected():
                sleep(1)
        except KeyboardInterrupt:
            print("Keyboard interrupt")
            break
        except:
            print("Connection failed")
