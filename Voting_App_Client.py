from socket import *
import tkinter as tk
from tkinter import Canvas
import Pmw
import pickle as pic

PORT = 5073
SERVER = gethostbyname(gethostname())
FORMAT = "utf-8"
HEADER = 64

ADDR = (SERVER, PORT)
client = socket(AF_INET, SOCK_STREAM)
client.connect(ADDR)

root = tk.Tk()
root.title("Voting App")
photo = tk.PhotoImage(file='Voting_App.png')
root.iconphoto(False, photo)
Pmw.initialise(root)

question = tk.Label(root, text="What is the best programming language out of these 5?")
question.config(font=('Courier', 20))
x_label = tk.Label(root, text='Candidates')
x_label.config(font=('Courier', 15))

canvas = Canvas()
canvas.config(width=800, height=701, bg='white')
adjust_value = 14

keys = []
bars = []
btns = []
tips = []

key_data = {"Javascript": "green",
            "C#": "pink",
            "PHP": "turquoise",
            "Python": "green yellow",
            "Go": "purple"}
key_language = list(key_data.keys())
key_color = list(key_data.values())

balloon = Pmw.Balloon()
label = balloon.component("label")
label.config(background="black", foreground="white")


class GraphKey:
    def __init__(self, x, y, color, text):
        self.x = x
        self.y = y
        self.color = color
        self.text = text

    def draw(self):
        global canvas
        canvas.create_rectangle(self.x + 69, self.y + 25, self.x + 34, self.y + 45, fill=self.color)
        canvas.create_text((self.x + 115), self.y + 35, text=self.text, font=('Courier', 10))


class BarGraph:
    def __init__(self, x, y, color, text, value):
        self.value = value
        self.x = x
        self.y = y
        self.y2 = self.y
        self.color = color
        self.pos = 0
        self.votes = 0
        self.text = text
        self.sent = False

    def draw(self):
        global canvas
        the_bar = canvas.create_rectangle(self.x, self.y, self.x + 50, self.y2, fill=self.color, tag="bar")
        balloon.tagbind(canvas, the_bar, f"Candidate\n {self.text} {self.votes}")


class VoteButton:
    number_change = 16
    x_change = 0
    self_change = 0
    z = 0
    indexes = [0, 1, 2, 3, 4]

    def __init__(self, row, column, text):
        self.sent = True
        self.row = row
        self.column = column
        self.text = text
        self.vbtn = tk.Button(root, text=self.text, command=self.voting)

    def draw(self):
        self.vbtn.grid(row=self.row, column=self.column, )

    def voting(self):
        adjust_bar = False
        global x
        global adjust_value
        down_bar = False
        y = 0
        online_adjust = False

        client_votes = [0, 0, 0, 0, 0]


        for bar in bars:

            bar_values = (self.text, bar.votes)

            bar_txt_msg = bar.text.encode(FORMAT)
            msg_len = len(bar_txt_msg)
            send_length = str(msg_len).encode(FORMAT)
            send_length += b"" * (HEADER - len(send_length))
            client.send(send_length)
            client.send(pic.dumps(bar_values))

            msg1 = (pic.loads(client.recv(2048 * 8)))
            msg2 = (pic.loads(client.recv(2048 * 8)))

            for bar in bars:
                if self.text == bar.text:
                    bar.votes = msg2[bar.value]
                    break


            for i in range(5):


                if msg2[i] > adjust_value:
                    x = max(msg2) - VoteButton.number_change
                    canvas.delete("some_tag")
                    draw_lines(45, 695, x, True)

                    canvas.delete("some_tag")
                    draw_lines(45, 695, max(msg2) + 2 - 14 + VoteButton.x_change, True)

                    if self.text == bar.text:

                        VoteButton.self_change += 1
                    else:
                        VoteButton.self_change += 1

                    online_adjust = True

                    VoteButton.number_change += 1
                    break

            break

        for bar in bars:

            if self.text == bar.text:
                if bar.votes > x:
                    bar.y2 -= 45
                client_votes[y] += 1

                bar.draw()

                if max(msg2) >= adjust_value:
                    if client_votes[y] < bar.votes:
                        if (bar.votes - client_votes[y]) % 2 == 0:
                            bar.y2 -= 90
                            online_adjust = True
                        else:
                            bar.y2 -= 45

                    if online_adjust:

                        bar.y2 += 45
                        adjust_value = bar.votes + 1

                    else:
                        if bar.votes % 2 != 0:
                            adjust_value = bar.votes + 1
                        else:
                            adjust_value = bar.votes + 2
                    canvas.delete("some_tag")



                    x += 2
                    bars_index = msg2.index(max(msg2))



                    draw_lines(45, 695, max(msg2) + 2 - 14 + VoteButton.x_change, True)
                    bars[bars_index].y2 = 70






                    down_bar = True

                    adjust_bar = True
            y += 1

        for bar in bars:



            if down_bar and adjust_bar and not online_adjust:
                for ind in VoteButton.indexes:

                    bars[ind].y2 += 90

                    continue
                canvas.delete("bar")
                bar.draw()
                break






def draw_keys(x, y):
    z = 0
    for i in key_language:
        keys.append(GraphKey(x, y, key_color[z], i))
        keys.append(GraphKey(x, y, key_color[z], i))

        x += 139
        z += 1

    for key in keys:
        key.draw()


def draw_bar(x, y):
    z = 0
    for i in key_color:
        bars.append(BarGraph(x, y, i, key_language[z], z))

        z += 1
        x += 139

    for bar in bars:
        bar.draw()


def draw_button(x, y):
    for i in key_language:
        btns.append(VoteButton(x, y, i))
        y += 1

    for btn in btns:
        btn.draw()


def draw_lines(x, y, num, can):
    z = num

    for i in range(8):
        canvas.create_line(x, y + 5, x + 750, y + 5)
        if can:
            if num % 2 != 0:
                num += 1
            canvas.create_text(x - 30, y, text=num, font=('Courier', 10), tag="some_tag")

        num += 2
        y -= 90

    for i in range(2):
        canvas.create_line(x, y + 725, x, y + 94)
        x += 750

    if z % 2 != 0:
        z += 1
    return z


draw_keys(35, 0)
draw_bar(85, 700)
filler = tk.Label(root, text='')
x_label.grid(row=2, column=3)

canvas.grid(row=1, column=0, columnspan=7)
question.grid(row=0, column=0, columnspan=7)
draw_button(3, 1)
x = 0
draw_lines(45, 695, x, False)
draw_lines(45, 695, x, True)

root.mainloop()
