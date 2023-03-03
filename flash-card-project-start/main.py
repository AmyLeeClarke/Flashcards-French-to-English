BACKGROUND_COLOR = "#B1DDC6"
from tkinter import Canvas, PhotoImage, Button, Tk, Label
from turtle import Screen
import pandas
import csv
import random
import time
current_card = {}
to_learn = {}
# read csv and turn data into separate dicts
try:
    france_data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = france_data.to_dict(orient="records")


# changes word when button clicked
def new_word():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="White")
    canvas.itemconfig(card_background, image=card_back_img)



def pass_answer():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    new_word()

# window
window = Tk()
window.title("Flashcard game")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

# canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
canvas.grid(row=0, column=0, columnspan=2)

# canvas text
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))

# cross button
cross_image = PhotoImage(file="images/right.png")
cross_button = Button(image=cross_image, highlightthickness=0, command=pass_answer)
cross_button.grid(row=1, column=0)

# check button
check_image = PhotoImage(file="images/wrong.png")
check_button = Button(image=check_image, highlightthickness=0, command=new_word)
check_button.grid(row=1, column=1)

# 3s time


new_word()

window.mainloop()