import tkinter as tk
import os
import fnmatch
from typing import Pattern
from pygame import mixer
import shutil
from tkinter import filedialog
import random
from tkinter import ttk


canvas=tk.Tk()
canvas.title("Music Player")
canvas.geometry("500x500")
canvas.config(bg='white')
rootpath ="Music"
pattern ="*.mp3"


mixer.init()

#image pour les boutton
prec_img=tk.PhotoImage(file="prev.png")
stop_img=tk.PhotoImage(file="stop.png")
play_img=tk.PhotoImage(file="play.png")
pause_img=tk.PhotoImage(file="pause.png")
next_img=tk.PhotoImage(file="next.png")
plus_img = tk.PhotoImage(file="plus.png")
minus_img = tk.PhotoImage(file="minus.png")
random_img = tk.PhotoImage(file="random.png")


def select():
    global loop
    label.config(text=listBox.get("anchor"))
    mixer.music.load(rootpath + "\\" + listBox.get("anchor"))
    mixer.music.play()
    if loop:
        mixer.music.play(-1)
def stop():
    mixer.music.stop()
    listBox.select_clear('active')
def next():
    next_song=listBox.curselection()
    next_song=next_song[0] + 1
    next_song_name=listBox.get(next_song)
    label.config(text=next_song_name)

    mixer.music.load(rootpath + "\\" + next_song_name)
    mixer.music.play()

    listBox.select_clear(0, "end")
    listBox.activate(next_song)
    listBox.select_set(next_song)
def prec():

    prec_song = listBox.curselection()
    prec_song= prec_song[0]-1
    prec_song_name=listBox.get(prec_song)

    label.config(text= prec_song_name)

    mixer.music.load(rootpath +"\\"+ prec_song_name)
    mixer.music.play()

    listBox.select_clear(0,'end')
    listBox.activate(prec_song)
    listBox.select_set(prec_song)
def pause():
    if pauseButton["text"]== "pause":
        mixer.music.pause()
        pauseButton["text"]= "pay"

    else:
          mixer.music.unpause()
          pauseButton["text"]= "pause"
def toggle_loop():
    global loop
    loop = not loop
    if loop:
        loopButton["text"] = "Loop: On"
    else:
        loopButton["text"] = "Loop: Off"
def add_track():
    filename = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
    if filename:
        destination = os.path.join("Music", os.path.basename(filename))
        shutil.copy2(filename, destination)
        listBox.insert("end", os.path.basename(filename))
def remove_track():
        song_name = listBox.get("active")
        file_path = os.path.join(rootpath, song_name)
        listBox.delete("active")
        if label["text"] == song_name:
                stop()
        os.remove(file_path)
def set_pos(val):
        position = float(val)
        mixer.music.set_pos(position)
def play_random():
        random_song = random.choice(listBox.get(0, "end"))
        label.config(text=random_song)
        mixer.music.load(rootpath + "\\" + random_song)
        mixer.music.play()
        listBox.select_clear(0, "end")
        listBox.activate(random_song)
        listBox.select_set(random_song)

#parametre couleur de la fenetre
listBox=tk.Listbox(canvas, fg="cyan", bg="black", width=100, font=('poppin"', 14))
listBox.pack(padx=15, pady=15)

label=tk.Label(canvas , text="", bg='white', fg='black', font=('poppin', 18))
label.pack(pady=15)

top=tk.Frame(canvas, bg="white")
top.pack (padx= 10, pady=5, anchor='center')


#different boutton
precButton = tk.Button(canvas, text="prec", image=prec_img, bg='white', borderwidth=0, command=prec)
precButton.pack(pady=15, in_=top, side="left")

stopButton = tk.Button(canvas, text="stop", image=stop_img, bg='white', borderwidth=0, command=stop)
stopButton.pack(pady=15,in_=top, side="left")

playButton = tk.Button(canvas, text="play", image=play_img, bg='white', borderwidth=0, command=select)
playButton.pack(pady=15, in_=top, side="left")

pauseButton = tk.Button(canvas, text="pause", image=pause_img, bg='white', borderwidth=0, command=pause)
pauseButton.pack(pady=15,in_=top, side="left")

nextButton = tk.Button(canvas, text="next", image=next_img, bg='white', borderwidth=0, command=next)
nextButton.pack(pady=15,in_=top, side="left")

randomButton = tk.Button(canvas, text="Random", image=random_img, bg="white", borderwidth=0, command=play_random)
randomButton.pack(pady=15, in_=top, side="left")

addButton = tk.Button(top, image=plus_img, bg="white", borderwidth=0, command=add_track)
addButton.pack(side="left")

removeButton = tk.Button(top, image=minus_img, bg="white", borderwidth=0, command=remove_track)
removeButton.pack(side="left")

loop = False
loopButton = tk.Button(canvas, text="Loop: Off", bg="white", borderwidth=0, command=toggle_loop)
loopButton.pack(pady=15, in_=top, side="left")

pos_bar = ttk.Scale(canvas, from_=0, to=100, orient="horizontal", command=set_pos)
pos_bar.pack(padx=10, pady=5)


for root, dirs,files in os.walk(rootpath):
    for filename in fnmatch.filter(files,pattern):
        listBox.insert('end', filename)
canvas.mainloop()