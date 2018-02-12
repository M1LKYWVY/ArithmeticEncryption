# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import ttk


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


def decode_mute(event):
    event.widget._nametowidget(event.widget.winfo_parent()).focus()


def encode_message(event):
    pass


def encode_message_lambda(user_string, result_label, text_info, errors_label):
    user_string = str(user_string.lower().strip())
    if user_string == "":
        errors_label.config(text="Check input string")
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
    # count = 1
    # vector_length = 0
    # for i in range(1, array_of_letters.__len__()):
    #     if i == array_of_letters.__len__()-1:
    #         count += 1
    #         frequency_of_letters.append(Symbol(array_of_letters[i], count))
    #         vector_length += count
    #     if array_of_letters[i] != array_of_letters[i-1]:
    #         vector_length += count
    #         frequency_of_letters.append(Symbol(array_of_letters[i-1], count))
    #         count = 0
    #     count += 1
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
        dict_of_letters[element.symbol] = Board(dict_of_letters[element.symbol].low_board, length)
        text_info.insert(END, element.symbol + "-" + str(element.frequency)+"\n")
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


def decode_message(event):
    pass


def decode_message_lambda(user_string):
    pass


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

    encode_submit = Button(encode_tab,
                           text="Submit \nEncoding",
                           command=lambda: encode_message_lambda(encode_text_input.get(0.0, END),
                                                                 encode_result_label,
                                                                 encode_text_info,
                                                                 encode_errors))
    # encode_submit.bind("<Button-1>", encode_message)
    encode_submit.place(x=260,
                        y=63,
                        width=80,
                        height=40)
    # Field to print errors in encode situation

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

    decode_result_frame = LabelFrame(decode_tab)
    decode_result_frame.place(x=label_size[0],
                              y=label_size[1]-59,
                              width=label_size[2],
                              height=label_size[3])
    decode_result_label = Label(decode_tab,
                                text="Input symbols and their frequency \n"
                                     "as in example: A-2\\n B-3\\n C-3")
    decode_result_label.place(x=label_size[0]+2,
                              y=label_size[1]-58,
                              width=label_size[2]-4,
                              height=label_size[3]-3)

    decode_submit = Button(decode_tab,
                           text="Submit \nDecoding")
    decode_submit.place(x=260,
                        y=5,
                        width=80,
                        height=40)
    decode_submit.bind("<Button-1>", decode_message)
    # Field to print errors in decode situations
    decode_errors = Label(decode_tab, fg="red")
    decode_errors.place(x=7, y=45, width=330, height=20)

    decode_text_input = Text(decode_tab)
    decode_text_input.place(x=7,
                            y=67,
                            width=330,
                            height=220)
    decode_text_input.insert(0.0, "A-2\nB-3\nC-3")

    decode_text_result = Text(decode_tab,
                              font="Arial 14")
    decode_text_result.place(x=7,
                             y=290,
                             width=330,
                             height=53)
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
