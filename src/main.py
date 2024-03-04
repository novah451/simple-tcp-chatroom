# In the future, this program will be the first program the user runs
# It will: spawn a server/room, connect user to their created room/allow user
# to join whichever room is available w/ access code

# Some features mentioned may be put into seperate files
# (e.g., the creation of a room may be done with spawn.py)

import os
import json
import time
import hashlib

with open("servers.json", "r") as file:
    chatrooms = json.load(file)


def clear():
    if os.name == "nt":
        cc = "cls"
    else:
        cc = "clear"
    os.system(cc)


def join_room():
    clear()
    empt = False
    resp = ""

    if not chatrooms["rooms"]:
        empt = True

    if empt:
        print("No rooms have been created yet. Would you like to make one?\n")
        print("[Y]: Yes")
        print("[N]: No")
        resp = input("\n>>> ")
        if resp == "Y":
            create_room()
    else:
        print("Which room would you like to join: \n")
        roomID = 1
        for room in chatrooms["rooms"]:
            roomName = room["name"]
            print(f"[{roomID}]: {roomName}")
            roomID += 1
        print("\n[R]: Return")
        resp = input("\n>>> ")

    roomToEnter = int(resp)
    return roomToEnter


def create_room():
    clear()

    # check if user can make a room
    if len(chatrooms["rooms"]) == 5:
        print("You cannot make anymore rooms, sorry!\n")
        return

    owner = input("Username: \t\t>>> ")
    name = input("Room Name: \t\t>>> ")
    access_code = input("Room's Access Code: \t>>> ")

    ac_256 = hashlib.sha256(access_code.encode("utf-8")).hexdigest()

    port_numbers = [59000, 59001, 59002, 59003, 59004]
    available_ports = []
    taken_ports = []
    for entity in chatrooms["rooms"]:
        if entity["port"] in port_numbers:
            taken_ports.append(entity["port"])
    # print(taken_ports)
    for total_num in port_numbers:
        if total_num not in taken_ports:
            available_ports.append(total_num)
    # print(available_ports)

    entry = {
        "owner": owner,
        "name": name,
        "port": available_ports[0],
        "access_code": ac_256,
    }

    chatrooms["rooms"].append(entry)

    # fcc = json.dumps(chatrooms, indent=4)
    # print(fcc)

    with open("servers.json", "w") as file:
        json.dump(chatrooms, file, indent=4)


if __name__ == "__main__":
    roomToEnter = 0
    while True:
        clear()
        print("Hello, and welcome to Novah's Simple TCP Chatroom!")
        print("Running on " + os.name + "\n")
        print("[1] JOIN A ROOM")
        print("[2] CREATE A ROOM\n")

        resp = input(">>> ")

        if resp == "1":
            roomToEnter = join_room()
            break
        elif resp == "2":
            create_room()
            break

    time.sleep(5)
    clear()
    roomInfo = chatrooms["rooms"][roomToEnter]
    command = f"client.py {roomInfo["owner"]} {roomInfo["port"]}"
    # os.system("client.py admin")

# I am too tired to keep working right now
# plus i got other things to take care of
# TODO: Fix the way the program connects the user
# TODO: Fix the goddamn logic of the program. makes no sense right now