# from tkinter import *
# from tkinter import ttk
#
#
# def left_click(event):
#     global text
#     text.delete("1.0", END)
#     text.insert(END, "leftclick")
#
#
# def right_click(event):
#     global text
#     text.delete(END)
#     text.insert(END, "rightclick")
#
#
# def get_text(event):
#     global text
#     print(text.get("1.0", END))
#
#
# # def main():
#
# root = Tk()
# root.minsize(600, 600)
# root.maxsize(600, 600)
# button1 = Button(root, text="button1")
# button1.bind("<Button-1>", get_text)
# button2 = Button(root, text="button2")
# button3 = Button(root, text="button3")
# text = Text(root)
# text.bind("<Button-1>", left_click)
# text.bind("<Button-3>", right_click)
# label = Label(root, text="Type your string here")
# button1.pack()
# button2.pack()
# button3.pack()
# text.pack()
# label.pack()
# root.mainloop()
#
#
# # if __name__ == "__main__":
# #     main()
#
#
from tkinter import *
from tkinter import ttk


def encode_mute(event):
    encode_tab.focus()


def decode_mute(event):
    decode_tab.focus()


root = Tk()
# root.minsize(500, 500)
# root.maxsize(500, 500)
frame_width = 350
frame_height = 370
config_size = "{0}x{1}".format(frame_width, frame_height)
root.geometry(config_size)

tabs = ttk.Notebook(root)
tabs.pack(fill='both', expand=True)

encode_tab = Frame(root)
decode_tab = Frame(root)
tabs.add(encode_tab, text="Encode message")
tabs.add(decode_tab, text="Decode message")

encode_text_input = Text(encode_tab, font="Arial 14")
encode_text_input.place(x=5, y=5, width=335, height=53)

label_size = [5, 64, 252, 40]
encode_result_frame = LabelFrame(encode_tab)
encode_result_frame.place(x=label_size[0], y=label_size[1], width=label_size[2], height=label_size[3])
encode_result_label = Label(encode_tab, text="Result")
encode_result_label.place(x=label_size[0]+2, y=label_size[1]+1, width=label_size[2]-4, height=label_size[3]-3)

encode_submit = Button(encode_tab, text="Submit \nEncoding")
encode_submit.place(x=260, y=63, width=80, height=40)

encode_errors = Label(encode_tab, fg="red")
encode_errors.place(x=7, y=104, width=330, height=20)

info_size = [5, 125, 335, 215]
encode_text_info = Text(encode_tab)
encode_text_info.place(x=info_size[0] + 2, y=info_size[1] + 1, width=info_size[2] - 4, height=info_size[3] - 3)
encode_text_info.bind("<FocusIn>", encode_mute)
encode_text_info.insert(0.0, "Encoding information")

encode_text_scrollbar = Scrollbar(encode_text_info)
encode_text_scrollbar["command"] = encode_text_info.yview
encode_text_input["yscrollcommand"] = encode_text_scrollbar.set
encode_text_scrollbar.pack(side='right', fill='y')

decode_result_frame = LabelFrame(decode_tab)
decode_result_frame.place(x=label_size[0], y=label_size[1]-59, width=label_size[2], height=label_size[3])
decode_result_label = Label(decode_tab, text="Input symbols and their frequency \n"
                                             "as in example: A-2\\n B-3\\n C-3")
decode_result_label.place(x=label_size[0]+2, y=label_size[1]-58, width=label_size[2]-4, height=label_size[3]-3)

decode_submit = Button(decode_tab, text="Submit \nDecoding")
decode_submit.place(x=260, y=5, width=80, height=40)

decode_errors = Label(decode_tab, fg="red")
decode_errors.place(x=7, y=45, width=330, height=20)

decode_text_input = Text(decode_tab)
decode_text_input.place(x=7, y=67, width=330, height=220)
decode_text_input.insert(0.0, "A-2\nB-3\nC-3")

decode_text_result = Text(decode_tab, font="Arial 14")
decode_text_result.place(x=7, y=290, width=330, height=53)
decode_text_result.insert(0.0, "Result")
decode_text_result.bind("<FocusIn>", decode_mute)

decode_text_scrollbar = Scrollbar(decode_text_input)
decode_text_scrollbar["command"] = decode_text_input.yview
decode_text_input["yscrollcommand"] = decode_text_scrollbar.set
decode_text_scrollbar.pack(side='right', fill='y')

root.mainloop()
