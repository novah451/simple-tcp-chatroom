import socket
import threading

# HOST = "192.168.1.115"
HOST = "127.0.0.1"
PORT = 59000
FORMAT = "utf-8"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


# Function to handle clients' connections
def handle_client(client):
    while True:
        try:
            msg = message = client.recv(1024)
            # Handles /kick [name] command
            if msg.decode(FORMAT).startswith("KICK"):
                if nicknames[clients.index(client)] == "admin":
                    name_to_kick = msg.decode(FORMAT)[5:]
                    if name_to_kick in nicknames:
                        kick_user(name_to_kick)
                    else:
                        client.send("This user is not in the chatroom!".encode(FORMAT))
                else:
                    client.send("Command was refused!".encode(FORMAT))
            # Handles /ban [name] command
            elif msg.decode(FORMAT).startswith("BAN"):
                if nicknames[clients.index(client)] == "admin":
                    name_to_ban = msg.decode(FORMAT)[4:]
                    if name_to_ban in nicknames:
                        kick_user(name_to_ban)
                        with open("bans.txt", "a") as f:
                            f.write(f"{name_to_ban}\n")
                        print(f"{name_to_ban} was banned!")
                    else:
                        client.send(
                            "This user is not currently in the chatroom".encode(FORMAT)
                        )
                else:
                    client.send("Command was refused!".encode(FORMAT))
            # Handles /server command
            # elif msg.decode(FORMAT).startswith("SERV"):
            #    if nicknames[clients.index(client)] == "admin":
            #        print("\nAll currently connected users: \n")
            #        for name in nicknames:
            #            print(f"{name} ")
            #    else:
            #        client.send("Command was refused!".encode(FORMAT))
            # Handles /exit command
            elif msg.decode(FORMAT).startswith("EXIT"):
                name = msg.decode(FORMAT)[5:]
                name_index = nicknames.index(name)
                client_to_kick = clients[name_index]
                # clients.remove(client_to_kick)
                client_to_kick.send("You left the chatroom".encode(FORMAT))
                # client_to_kick.close()
                # nicknames.remove(name)
                broadcast(f"{name} has left the chatroom!".encode(FORMAT))
            # Handles /users command
            elif msg.decode(FORMAT).startswith("LISTUS"):
                client.send("\nAll connected users: ".encode(FORMAT))
                for name in nicknames:
                    client.send(f"{name} ".encode(FORMAT))
                client.send("\n".encode(FORMAT))
            else:
                broadcast(message)
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                # broadcast(f"{nickname} has left the chat room!".encode(FORMAT))
                nicknames.remove(nickname)
                break


# Main function to receive the clients connection
def receive():
    while True:
        client, address = server.accept()
        print(f"A connection has been established with {str(address)}")

        client.send("NICK".encode(FORMAT))
        nickname = client.recv(1024).decode(FORMAT)

        with open("bans.txt", "r") as f:
            bans = f.readlines()

        if nickname + "\n" in bans:
            client.send("BAN".encode(FORMAT))
            client.close()
            continue

        if nickname == "admin":
            client.send("PASS".encode(FORMAT))
            password = client.recv(1024).decode(FORMAT)

            # TODO: Make this more secure when checking password of admin
            if password != "adminpass":
                client.send("REFUSE".encode(FORMAT))
                client.close()
                # uses continue INSTEAD of break because server uses one thread
                continue

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}!")
        broadcast(f"{nickname} has joined the chatroom!".encode(FORMAT))
        client.send("You are now connected!\n".encode(FORMAT))
        client.send("All connected users: ".encode(FORMAT))
        for name in nicknames:
            client.send(f"{name} ".encode(FORMAT))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


def kick_user(name):
    if name in nicknames:
        name_index = nicknames.index(name)
        client_to_kick = clients[name_index]
        clients.remove(client_to_kick)
        # client_to_kick.send("You were kicked by an admin!".encode(FORMAT))
        client_to_kick.send("YHBK".encode(FORMAT))
        # client_to_kick.close()
        nicknames.remove(name)
        broadcast(f"{name} was kicked by an admin!".encode(FORMAT))


if __name__ == "__main__":
    print("[STARTING] Server is running and listening ...")
    receive()
