# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pyperclip


class Symbol:
    def __init__(self, symbol, frequency):
        self.symbol = symbol
        self.frequency = frequency


class Board:
    def __init__(self, low_board, high_board):
        self.low_board = low_board
        self.high_board = high_board


def get_frequency(element):
    return element.frequency


def encode_mute(event):
    event.widget._nametowidget(event.widget.winfo_parent()).focus()
    try:
        if event.widget.get(0.0, END) == "Encoding information\n":
            return
    except AttributeError:
        if event.widget["text"] == "Result":
            return
    try:
        pyperclip.copy(event.widget.get(0.0, END).replace("", ""))
    except AttributeError:
        pyperclip.copy(event.widget["text"])
    messagebox.showinfo("System information", "Widget's value copied to clipboard")


def decode_mute(event):
    event.widget._nametowidget(event.widget.winfo_parent()).focus()


def encode_message(event):
    pass


def encode_message_lambda(text_input, result_label, text_info, errors_label):
    glass = text_input.get(0.0, END)
    glass = glass.replace("\n", "")
    text_input.delete(0.0, END)
    text_input.insert(0.0, glass)
    user_string = text_input.get(0.0, END)
    copy_string = ""
    user_string = str(user_string.lower().strip().replace(" ", "_"))
    if user_string == "":
        errors_label.config(text="User's string not found")
        return
    errors_label.config(text="")
    text_info.delete(0.0, END)
    text_info.insert(0.0, "User's string: " + user_string + "\n")
    array_of_letters = []
    for ch in list(user_string):
        if not ord(ch) == 10:
            array_of_letters.append(ch)
    array_of_letters.sort()
    frequency_of_letters = []
    text_info.insert(END, "Frequency of symbols:\n")
    count = 0
    vector_length = 0
    for ch_i in list(array_of_letters):
        for ch_g in list(array_of_letters):
            if ch_i == ch_g:
                count += 1
        is_exist = False
        for sym in frequency_of_letters:
            if sym.symbol == ch_i:
                is_exist = True
        if not is_exist:
            frequency_of_letters.append(Symbol(ch_i, count))
            vector_length += count
        count = 0
    frequency_of_letters.sort(key=get_frequency, reverse=True)
    dict_of_letters = dict()
    length = 0
    for element in frequency_of_letters:
        dict_of_letters[element.symbol] = Board(length, 0)
        length += element.frequency/vector_length
        copy_string += element.symbol + "-" + str(element.frequency) + "\n"
        dict_of_letters[element.symbol] = Board(dict_of_letters[element.symbol].low_board, length)
        text_info.insert(END, "\'" + element.symbol + "\'" + "-" + str(element.frequency)+"\n")
        text_info.insert(END, "from " + str(dict_of_letters[element.symbol].low_board) + "\n")
        text_info.insert(END, "to " + str(dict_of_letters[element.symbol].high_board) + "\n\n")
    low_old = 0
    low_board = 0
    high_old = 1
    high_board = 1
    for ch in list(user_string):
        high_board = low_old + (high_old - low_old)*dict_of_letters[ch].high_board
        low_board = low_old + (high_old - low_old)*dict_of_letters[ch].low_board
        high_old = high_board
        low_old = low_board
    if low_board == high_board:
        result_label.config(text=str(high_board))
    else:
        result_label.config(text=str(low_board) + "\n" + str(high_board))
    pyperclip.copy(copy_string)


def decode_message(event):
    pass


def decode_message_lambda(user_code, text_info, text_result, errors_label):
    user_code = float(user_code)
    text_info = text_info.lower().strip()
    lines = text_info.split("\n")
    precision = int(lines[0].split("-")[1])
    frequency_of_letters = []
    for line in lines:
        if line.split("-")[0] == "precision":
            continue
        frequency_of_letters.append(Symbol(line.split("-")[0], int(line.split("-")[1])))
    frequency_of_letters.sort(key=get_frequency, reverse=True)
    vector_length = 0
    for sym in frequency_of_letters:
        vector_length += sym.frequency
    dict_of_letters = dict()
    length = 0
    for element in frequency_of_letters:
        dict_of_letters[element.symbol] = Board(length, 0)
        length += element.frequency / vector_length
        dict_of_letters[element.symbol] = Board(dict_of_letters[element.symbol].low_board, length)
    first_char = ""
    for sym in frequency_of_letters:
        if dict_of_letters[sym.symbol].low_board <= user_code <= dict_of_letters[sym.symbol].high_board:
            first_char = sym.symbol
    user_string = [first_char]
    for i in range(0, precision):
        user_code = (user_code - dict_of_letters[user_string[i]].low_board) /\
                    (dict_of_letters[user_string[i]].high_board - dict_of_letters[user_string[i]].low_board)
        print(user_code)
        for sym in frequency_of_letters:
            if dict_of_letters[sym.symbol].low_board <= user_code <= dict_of_letters[sym.symbol].high_board:
                print(sym.symbol)
                user_string.append(sym.symbol)
    print(user_string)


def main():
    root = Tk()
    root.title("Arithmetic Encryption")
    root.minsize(350, 370)
    root.maxsize(350, 370)
    # frame_width = 350
    # frame_height = 370
    # config_size = "{0}x{1}".format(frame_width, frame_height)
    # root.geometry(config_size)

    tabs = ttk.Notebook(root)
    tabs.pack(fill="both", expand=True)

    encode_tab = Frame(root)
    decode_tab = Frame(root)
    tabs.add(encode_tab, text="Encode message")
    tabs.add(decode_tab, text="Decode message")
    encode_text_input = Text(encode_tab,
                             font="Arial 14")
    encode_text_input.place(x=5,
                            y=5,
                            width=335,
                            height=53)
    encode_text_input.bind("<Return>", lambda _: encode_message_lambda(encode_text_input,
                                                                       encode_result_label,
                                                                       encode_text_info,
                                                                       encode_errors))

    label_size = [5, 64, 252, 40]

    encode_errors = Label(encode_tab,
                          fg="red")
    encode_errors.place(x=label_size[0],
                        y=94,
                        width=label_size[2],
                        height=label_size[3])

    encode_result_frame = LabelFrame(encode_tab)
    encode_result_frame.place(x=label_size[0],
                              y=label_size[1],
                              width=label_size[2],
                              height=label_size[3])
    encode_result_label = Label(encode_tab,
                                text="Result")
    encode_result_label.place(x=label_size[0]+2,
                              y=label_size[1]+1,
                              width=label_size[2]-4,
                              height=label_size[3]-3)
    encode_result_label.bind("<Button-1>", encode_mute)

    encode_submit = Button(encode_tab,
                           text="Submit \nEncoding",
                           command=lambda: encode_message_lambda(encode_text_input,
                                                                 encode_result_label,
                                                                 encode_text_info,
                                                                 encode_errors))
    # encode_submit.bind("<Button-1>", encode_message)
    encode_submit.place(x=260,
                        y=63,
                        width=80,
                        height=40)

    info_size = [5, 125, 335, 215]
    encode_text_info = Text(encode_tab)
    encode_text_info.place(x=info_size[0] + 2,
                           y=info_size[1] + 1,
                           width=info_size[2] - 4,
                           height=info_size[3] - 3)
    encode_text_info.bind("<FocusIn>", encode_mute)
    encode_text_info.insert(0.0, "Encoding information")

    encode_text_scrollbar = Scrollbar(encode_text_info)
    encode_text_scrollbar["command"] = encode_text_info.yview
    encode_text_input["yscrollcommand"] = encode_text_scrollbar.set
    encode_text_scrollbar.pack(side='right',
                               fill='y')

    decode_float_input = Text(decode_tab)
    decode_float_input.place(x=label_size[0]+3,
                             y=label_size[1]-58,
                             width=label_size[2]-5,
                             height=label_size[3])

    decode_submit = Button(decode_tab,
                           text="Submit \nDecoding",
                           command=lambda: decode_message_lambda(decode_float_input.get(0.0, END),
                                                                 decode_text_input.get(0.0, END),
                                                                 decode_text_result,
                                                                 decode_errors))
    decode_submit.place(x=260,
                        y=5,
                        width=80,
                        height=40)
    # decode_submit.bind("<Button-1>", decode_message)

    decode_errors = Label(decode_tab, fg="red")
    decode_errors.place(x=9, y=50, width=250, height=12)

    decode_result_frame = LabelFrame(decode_tab)
    decode_result_frame.place(x=7,
                              y=66,
                              width=330,
                              height=label_size[3]+4)
    decode_result_label = Label(decode_tab,
                                text="Input precision, symbols and their frequency \n"
                                     "as in example: precision-5\\nA-2\\nB-3\\nC-3")
    decode_result_label.place(x=8,
                              y=68,
                              width=320,
                              height=label_size[3] - 3)

    decode_text_input = Text(decode_tab)
    decode_text_input.place(x=7,
                            y=115,
                            width=330,
                            height=170)
    decode_text_input.insert(0.0, "precision-5\nA-2\nB-3\nC-3")

    decode_text_result = Text(decode_tab,
                              font="Arial 14")
    decode_text_result.place(x=7,
                             y=290,
                             width=330,
                             height=50)
    decode_text_result.insert(0.0, "Result")
    decode_text_result.bind("<FocusIn>", decode_mute)

    decode_text_scrollbar = Scrollbar(decode_text_input)
    decode_text_scrollbar["command"] = decode_text_input.yview
    decode_text_input["yscrollcommand"] = decode_text_scrollbar.set
    decode_text_scrollbar.pack(side='right',
                               fill='y')

    root.mainloop()


if __name__ == "__main__":
    main()
