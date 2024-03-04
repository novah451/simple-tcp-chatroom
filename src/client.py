import socket
import threading
import sys

# HOST = "192.168.1.115"
HOST = "127.0.0.1"
# PORT = 59000
PORT = int(sys.argv[2])
FORMAT = "utf-8"

stop_thread = False

nickname = sys.argv[1]
if nickname == "admin":
    password = input("Enter password for admin: ")


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


def client_receive():
    while True:
        global stop_thread
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode(FORMAT)
            if message == "NICK":
                client.send(nickname.encode(FORMAT))
                next_message = client.recv(1024).decode(FORMAT)
                if next_message == "PASS":
                    client.send(password.encode(FORMAT))
                    if client.recv(1024).decode(FORMAT) == "REFUSE":
                        print("Connection was refused! Wrong password!")
                        stop_thread = True
                elif next_message == "BAN":
                    print("\nConnection refused because of ban!")
                    print("Press ENTER to return to cmdline")
                    # client.close()
                    stop_thread = True
                    break
            elif message == "YHBK":
                print("\nYou were kicked by an admin!")
                print("Press ENTER to return to cmdline")
                client.close()
                # stop_thread = True
                break
            else:
                print(message)
        except:
            print("\nError! Something went wrong: Closing Connection")
            print("Press ENTER to return to cmdline")
            client.close()
            # stop_thread = True
            break


def client_send():
    while True:
        global stop_thread
        if stop_thread:
            break
        message = f'{nickname}: {input("")}'
        # LIST OF COMMANDS
        if message[len(nickname) + 2 :].startswith("/"):
            # Show all possible commands
            if message[len(nickname) + 2 :].startswith("/help"):
                print("Here's a list of available commands:")
            # Exit chatroom
            if message[len(nickname) + 2 :].startswith("/exit"):
                client.send(f"EXIT {nickname}".encode(FORMAT))
                stop_thread = True
            # List all connected users
            if message[len(nickname) + 2 :].startswith("/users"):
                client.send(f"LISTUS".encode(FORMAT))
            #
            ######################
            ### ADMIN COMMANDS ###
            ######################
            #
            # KICK COMMAND
            if message[len(nickname) + 2 :].startswith("/kick"):
                if nickname == "admin":
                    client.send(f"KICK {message[len(nickname)+2+6:]}".encode(FORMAT))
                else:
                    print("The kick command can only be executed by the admin!")
            # BAN COMMAND
            if message[len(nickname) + 2 :].startswith("/ban"):
                if nickname == "admin":
                    client.send(f"BAN {message[len(nickname)+2+5:]}".encode(FORMAT))
                else:
                    print("The ban command can only be executed by the admin!")
            # SERVER-ALL USERS COMMAND
            # if message[len(nickname) + 2 :].startswith("/server"):
            #    if nickname == "admin":
            #        client.send(f"SERVALL".encode(FORMAT))
            #    else:
            #        print("The ban command can only be executed by the admin!")
        else:
            client.send(message.encode(FORMAT))


receive_thread = threading.Thread(target=client_receive)
receive_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()
