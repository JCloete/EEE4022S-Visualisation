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
        self.insert_dish()

    def create_UI(self):
        # Create a Top frame where the activity takes place
        self.top_frame = tk.Frame(root, width=1280, height=840)
        self.top_frame.pack(fill=tk.BOTH, expand=True)

        # Create a bottom frame for UI
        self.bottom_frame = tk.Frame(root, relief=tk.RAISED, borderwidth=1)
        self.bottom_frame.pack(side = tk.BOTTOM, fill=tk.BOTH, expand=True)

        # button to exit program - TODO: PUT THIS IN A CONTROL GENERATION METHOD
        self.quit_button = tk.Button(self.bottom_frame, text="Quit", fg="red", command=root.destroy)
        self.quit_button.pack( side = tk.RIGHT, padx=5, pady=5)

    def insert_map(self):
        self.map_original = Image.open(self.map_path)
        self.map_original = self.map_original.resize((1280, 840), Image.ANTIALIAS)
        self.map = ImageTk.PhotoImage(self.map_original)
        self.map_display = tk.Label(self.top_frame, image=self.map, borderwidth=0)
        self.map_display.grid(column=0, row=0)
        self.map_display.pack(fill=tk.BOTH, expand=True)

    def insert_dish(self):
        self.dish_original = Image.open(self.dish_path)
        self.dish_original = self.dish_original.resize((20, 20), Image.ANTIALIAS)
        self.dish = ImageTk.PhotoImage(self.dish_original)
        self.dish_canvas = tk.Label(self.top_frame, image=self.dish, borderwidth=0).place(x = 800, y = 400)



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