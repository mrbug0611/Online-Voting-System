from socket import *
import threading as thr
import pickle as pic

PORT = 5073
SERVER = gethostbyname(gethostname())

ADDR = (SERVER, PORT)
server = socket(AF_INET, SOCK_STREAM)
HEADER = 64
FORMAT = 'utf-8'

server.bind(ADDR)

cate_date = {"Javascript": 0,
             "C#": 0,
             "PHP": 0,
             "Python": 0,
             "Go": 0}
cate_names = list(cate_date.keys())
cate_colors = list(cate_date.values())


def handle_client(conn, addr):
    print(f"New Connection: {addr}")

    connected = True
    while connected:
        msg_len = conn.recv(HEADER).decode(FORMAT)
        if msg_len:
            msg_len = int(msg_len)
            msg = pic.loads(conn.recv(HEADER * 8))
            msg = list(msg)
            msg[1] += 1

            for i in range(5):
                if msg[0] == cate_names[i]:
                    print("message", msg[0], cate_names[i])
                    cate_colors[i] += 1
                    break

            print("cate colors", cate_colors)
            conn.send(pic.dumps(msg))
            conn.send(pic.dumps(cate_colors))

    conn.close()


def start():
    server.listen()
    print(f"Server is listening on {SERVER}")

    while True:
        conn, addr = server.accept()
        thread = thr.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"\nActive Connections: {thr.active_count() - 1}")


print("Server is Starting")
start()
