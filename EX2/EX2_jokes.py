import tkinter as tk
import random
from PIL import Image, ImageTk, ImageSequence
import winsound

#load randomJokes.txt
try:
    with open("EX2/randomJokes.txt", "r", encoding="utf-8") as f:
        jokes = []
        for l in f:
            if "?" in l:
                s = l.strip().split("?",1)
                jokes.append((s[0] + "?", s[1]))
except:
    jokes = [("No jokes found?", "Check the file lol")]

current = None

root = tk.Tk()
root.title("Jokes App")
root.geometry("800x500")
root.resizable(False, False)

#gif
gif = Image.open("EX2/ex2teehee.gif")
gif_frames = []
for frame in ImageSequence.Iterator(gif):
    fr = frame.copy().resize((343, 333))
    gif_frames.append(ImageTk.PhotoImage(fr))

bg_label = tk.Label(root, image=gif_frames[0])
bg_label.place(x=400, y=200)

animating = False

def animate_bg(i=0):
    global animating
    if not animating:
        return

    bg_label.config(image=gif_frames[i])

    if i + 1 < len(gif_frames):
        root.after(70, animate_bg, i + 1)
    else:
        animating = False
        bg_label.config(image=gif_frames[0])

#ui
setup = tk.Label(root, text="Press the button ig", wraplength=350, bg="white")
setup.place(x=20, y=50)

punch = tk.Label(root, text="", wraplength=350, bg="white")
punch.place(x=20, y=150)

#functions
def get_joke():
    global current
    current = random.choice(jokes)
    setup.config(text=current[0])
    punch.config(text="")
    alexa_btn.config(state="disabled")

def show_p():
    global animating
    if current:
        punch.config(text=current[1])

        animating = True
        animate_bg(0)

        #sound effect
        try:
            winsound.PlaySound("EX2/laugh.wav",
                winsound.SND_FILENAME | winsound.SND_ASYNC)
        except:
            pass

def next_j():
    alexa_btn.config(state="normal")
    get_joke()

#buttons
alexa_btn = tk.Button(root, text="Alexa tell me a joke", command=get_joke)
alexa_btn.place(x=20, y=10)

punch_btn = tk.Button(root, text="Show Punchline", command=show_p)
punch_btn.place(x=600, y=100)

next_btn = tk.Button(root, text="Next Joke", command=next_j)
next_btn.place(x=20, y=250)

quit_btn = tk.Button(root, text="Quit", command=root.quit)
quit_btn.place(x=20, y=300)

root.mainloop()
