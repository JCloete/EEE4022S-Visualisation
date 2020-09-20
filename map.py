import time
import tkinter as tk
from PIL import ImageTk, Image

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)

        self.map_path = 'Test.jpg'
        self.dish_path = 'dish.png'

        self.create_UI()
        self.insert_map()
        #self.insert_dish()
        #self.draw_dish()

    def create_UI(self):
        self.top_frame = tk.Frame(root, width=1280, height=840)
        self.top_frame.pack(fill=tk.BOTH, expand=True)

        self.bottom_frame = tk.Frame(root, relief=tk.RAISED, borderwidth=1)
        self.bottom_frame.pack(side = tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.quit_button = tk.Button(self.bottom_frame, text="Quit", fg="red", command=root.destroy)
        self.quit_button.pack( side = tk.RIGHT, padx=5, pady=5)

    def insert_map(self):
        self.map_original = Image.open(self.map_path)
        self.map_original = self.map_original.resize((1280, 840), Image.ANTIALIAS)
        self.map = ImageTk.PhotoImage(self.map_original)
        self.map_display = tk.Label(self.top_frame, image=self.map, borderwidth=0)
        self.map_display.grid(column=0, row=0)
        self.map_display.pack(fill=tk.BOTH, expand=True)



root = tk.Tk()
root.geometry("1280x960")
root.title("NeXtRAD NTPCS Visualisation")

app = Application(master=root)
app.mainloop()

######

#root = tk.Tk()
#root.geometry("1280x960")
#root.title("NeXtRAD NTPCS Visualisation")

#top_frame = tk.Frame(root, width=1280, height=960-120)
#top_frame.pack(fill=tk.BOTH, expand=True)

#bottom_frame = tk.Frame(root, relief=tk.RAISED, borderwidth=1)
#bottom_frame.pack(side = tk.BOTTOM, fill=tk.BOTH, expand=True)

#quit_button = tk.Button(bottom_frame, text="Quit", fg="red", command=root.destroy)
#quit_button.pack( side = tk.RIGHT, padx=5, pady=5)

#root.mainloop()