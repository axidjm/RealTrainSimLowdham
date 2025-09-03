#!/usr/bin/env python3

# Standard
import json
import time
from datetime import datetime
from time import sleep

# Third party
import stomp

# Project
from bells import (
    IsLineClear,
    TrainEnteringSection,
    TrainOutOfSection,
    bells_test,
    long_pause,
    tc4601,
)
from pytz import timezone

__version__ = "1.0.0"
debug = False

TIMEZONE_LONDON: timezone = timezone("Europe/London")

# TD message types

C_BERTH_STEP = "CA"  # Berth step      - description moves from "from" berth into "to", "from" berth is erased
C_BERTH_CANCEL = "CB"  # Berth cancel    - description is erased from "from" berth
C_BERTH_INTERPOSE = "CC"  # Berth interpose - description is inserted into the "to" berth, previous contents erased
C_HEARTBEAT = "CT"  # Heartbeat       - sent periodically by a train describer

S_SIGNALLING_UDPATE = "SF"  # Signalling update
S_SIGNALLING_REFRESH = "SG"  # Signalling refresh
S_SIGNALLING_REFRESH_FINISHED = "SH"  # Signalling refresh finished

message_received = False


def print_td_frame(parsed_body):
    global message_received

    # print("Received a message\n")
    # Each message in the queue is a JSON array
    for outer_message in parsed_body:
        # Each list element consists of a dict with a single entry - our real target - e.g. {"CA_MSG": {...}}
        message = list(outer_message.values())[0]

        message_type = message["msg_type"]
        area_id = message["area_id"]

        # print("Received message type: ", message_type, " area_id: ", area_id)
        if not message_received:
            print(f"Message Received {message}")

        if area_id == "NM":
            # The feed time is in milliseconds, but python takes timestamps in seconds
            timestamp = int(int(message["time"]) / 1000)
            utc_datetime = datetime.fromtimestamp(timestamp, tz=timezone("utc"))
            # uk_datetime = TIMEZONE_LONDON.fromutc(dt=utc_datetime).strftime("%Y-%m-%d %H:%M:%S")
            uk_datetime = utc_datetime.strftime("%Y-%m-%d %H:%M:%S")

            # For the sake of demonstration, we're only displaying C-trainClass messages
            if message_type in [C_BERTH_STEP, C_BERTH_CANCEL, C_BERTH_INTERPOSE]:
                description = message.get("descr", "")
                from_berth = message.get("from", "")
                to_berth = message.get("to", "")

                if from_berth.startswith("40"):
                    print(
                        f"{uk_datetime} {message_type} {area_id} {description} {from_berth}->{to_berth}"
                    )
                    match from_berth:
                        case "4072":
                            print(f"{uk_datetime} Up train {description} near Fiskerton")
                            IsLineClear("rear", "UP", description)
                        case "4062":
                            print(f"{uk_datetime} Up train {description} near Bleasby")
                            TrainEnteringSection("rear", "UP", description)
                            long_pause()
                            IsLineClear("advance", "UP", description)
                        case "4050":
                            print(f"{uk_datetime} Up train {description} near Lowdham")
                            tc4601("OCCUPIED")
                            TrainEnteringSection("advance", "UP", description)
                            long_pause()
                            TrainOutOfSection("rear", "UP", description)
                            if description[0] == "6":
                                print("20 sec delay extra before clearing TC")
                                time.sleep(20)  # Freight trains take a while to clear the TC!
                            tc4601("CLEAR")
                        case "4042":
                            print(f"{uk_datetime} Up train {description} near Burton Joyce")
                            TrainOutOfSection("advance", "UP", description)
                        case "4036":
                            print(f"{uk_datetime} Up train {description} near Carlton")

                        case "4037":
                            print(f"{uk_datetime} Down train {description} near Carlton")
                            IsLineClear("rear", "DOWN", description)
                        case "4043":
                            print(f"{uk_datetime} Down train {description} near Burton Joyce")
                            TrainEnteringSection("rear", "DOWN", description)
                            long_pause()
                            IsLineClear("advance", "DOWN", description)
                        case "4051":
                            print(f"{uk_datetime} Down train {description} near Lowdham")
                            TrainEnteringSection("advance", "UP", description)
                            print("20 sec delay before TrainOutOfSection")
                            time.sleep(20)
                            TrainOutOfSection("rear", "DOWN", description)
                        case "4065":
                            print(f"{uk_datetime} Down train {description} near Bleasby")
                            TrainOutOfSection("advance", "DOWN", description)
                        case _:
                            if from_berth[0:3] == "400":
                                print(
                                    f"{uk_datetime} Down train {description} "
                                    f"leaving Nottingham platform {from_berth[3]}"
                                )

            # For the sake of demonstration, we're only displaying C-trainClass messages
            # Docs on S-messages is thin to non-existent
            # https://wiki.openraildata.com/index.php/S_Class_Messages
            if debug and message_type in [
                S_SIGNALLING_UDPATE,
                S_SIGNALLING_REFRESH,
                S_SIGNALLING_REFRESH_FINISHED,
            ]:
                address = message.get("address", "")
                data = message.get("data", "")

                print(f"{uk_datetime} {message_type} {area_id} {address} {data}")

    message_received = True


def connect_and_subscribe():
    # Connect to feed
    connect_headers = {
        "username": "signalbox@lowdhamstation.me.uk",
        "passcode": "SigBox1!",
        "wait": True,
    }

    # Subscription
    subscribe_headers = {
        "destination": "/topic/TD_MC_EM_SIG_AREA",
        "id": 1,
        "ack": "auto",
    }

    # print("Attempting connection")
    connection.connect(**connect_headers)
    connection.subscribe(**subscribe_headers)


class Listener(stomp.ConnectionListener):
    _mq: stomp.Connection

    def __init__(self, mq: stomp.Connection):
        self._mq = mq

    def on_message(self, frame):
        headers, message_raw = frame.headers, frame.body
        # print(headers, '\n', message_raw, '\n')
        parsed_body = json.loads(message_raw)

        if headers["destination"].startswith("TRAIN_MVT_"):
            pass
        elif headers["destination"].startswith("TD_"):
            print_td_frame(parsed_body)

    def on_error(self, frame):
        print("received an error {}".format(frame.body))

    def on_disconnected(self):
        print("disconnected")


if __name__ == "__main__":
    print("Signalling real trains as they pass Lowdham ", __version__)
    # Sample code is here: https://github.com/openraildata/td-trust-example-python3/blob/master/main.py

    # https://stomp.github.io/stomp-specification-1.2.html#Heart-beating
    # We're committing to sending and accepting heartbeats every 5000ms
    connection = stomp.Connection(
        [("publicdatafeeds.networkrail.co.uk", 61618)], keepalive=True, heartbeats=(20000, 20000)
    )
    connection.set_listener("", Listener(connection))

    try:
        # bells_test()
        print("End of test")
    except KeyboardInterrupt:
            print("Keyboard interrupt")

    while 1:
        try:
            sleep(1)
            connect_and_subscribe()

            while connection.is_connected():
                sleep(1)
        except KeyboardInterrupt:
            print("Keyboard interrupt")
            break
        except:
            print("Connection failed")
