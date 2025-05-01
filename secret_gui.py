import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import threading
import time
import os

class MovingGIF:
    def __init__(self, root, gif_path):
        self.root = root
        self.root.title("Singe qui danse")
        self.canvas = tk.Canvas(root, width=500, height=400, bg="white")
        self.canvas.pack()

        # Charger le GIF
        self.gif = Image.open(gif_path)
        self.frames = [ImageTk.PhotoImage(frame.copy().convert("RGBA")) for frame in ImageSequence.Iterator(self.gif)]

        self.index = 0
        self.x = 50
        self.y = 50
        self.dx = 4
        self.dy = 3

        self.image_id = self.canvas.create_image(self.x, self.y, image=self.frames[0], anchor="nw")
        self.canvas.tag_bind(self.image_id, "<Button-1>", self.close_window)

        self.running = True
        threading.Thread(target=self.animate, daemon=True).start()
        threading.Thread(target=self.move, daemon=True).start()

    def animate(self):
        while self.running:
            self.index = (self.index + 1) % len(self.frames)
            self.canvas.itemconfig(self.image_id, image=self.frames[self.index])
            time.sleep(0.1)

    def move(self):
        while self.running:
            self.x += self.dx
            self.y += self.dy

            if self.x <= 0 or self.x + self.gif.width >= 500:
                self.dx *= -1
            if self.y <= 0 or self.y + self.gif.height >= 400:
                self.dy *= -1

            self.canvas.coords(self.image_id, self.x, self.y)
            time.sleep(0.03)

    def close_window(self, event):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    if not os.path.exists("monkey.gif"):
        print("Le fichier monkey.gif est manquant. Place-le dans le même dossier que ce script.")
    else:
        root = tk.Tk()
        app = MovingGIF(root, "monkey.gif")
        root.mainloop()
