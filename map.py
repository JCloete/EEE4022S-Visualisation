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
        self.boat_path = 'boat.jpg'

        self.create_UI()
        self.insert_map()
        self.insert_dish()
        self.insert_boat()

        self.create_line()

    def create_UI(self):
        # Create a Top frame where the activity takes place
        #self.top_frame = tk.Frame(root, width=1280, height=840)
        #self.top_frame.pack(fill=tk.BOTH, expand=True)

        # Create a canvas to draw on
        self.map_canvas = tk.Canvas(root, width=1280, height=760)
        self.map_canvas.pack(fill=tk.BOTH, expand=True)

        # Create a bottom frame for UI
        self.bottom_frame = tk.Frame(root, relief=tk.RAISED, borderwidth=1)
        self.bottom_frame.pack(side = tk.BOTTOM, fill=tk.BOTH, expand=False)

        # button to exit program - TODO: PUT THIS IN A CONTROL GENERATION METHOD
        self.quit_button = tk.Button(self.bottom_frame, text="Quit", fg="red", command=root.destroy, width=5, height=2)
        self.quit_button.pack( side = tk.RIGHT, padx=5, pady=5)

        self.control_frame = tk.Frame(self.bottom_frame, relief=tk.RAISED, borderwidth=1)

        # Configure Grid for the buttons
        self.control_frame.columnconfigure(0, pad=3)
        self.control_frame.columnconfigure(1, pad=3)
        self.control_frame.columnconfigure(2, pad=3)

        self.control_frame.rowconfigure(0, pad=3)
        self.control_frame.rowconfigure(1, pad=3)
        self.control_frame.rowconfigure(2, pad=3)

        self.up_button = tk.Button(self.control_frame, text="Up", width=5, height=2)
        self.up_button.grid(row=0, column=1)
        #self.up_button.pack(side = tk.TOP, padx=5, pady=5)

        self.left_button = tk.Button(self.control_frame, text="CCW", width=5, height=2)
        self.left_button.grid(row=1, column=0)
        #self.left_button.pack(side = tk.LEFT, padx=5, pady=5)

        self.right_button = tk.Button(self.control_frame, text="CW", width=5, height=2)
        self.right_button.grid(row=1, column=2)
        #self.right_button.pack(side = tk.RIGHT, padx=5, pady=5)

        self.down_button = tk.Button(self.control_frame, text="Down", width=5, height=2)
        self.down_button.grid(row=2, column=1)
        #self.down_button.pack(side = tk.BOTTOM, padx=5, pady=5)

        self.control_frame.pack(side = tk.LEFT, fill=tk.BOTH, expand=False)

    def insert_map(self):
        self.map_original = Image.open(self.map_path)
        self.map_original = self.map_original.resize((1280, 840), Image.ANTIALIAS)
        self.map = ImageTk.PhotoImage(self.map_original)

        self.map_display = self.map_canvas.create_image(0, 0, anchor=tk.NW, image=self.map)

        #self.map_display = tk.Label(self.top_frame, image=self.map, borderwidth=0)
        #self.map_display.grid(column=0, row=0)
        #self.map_display.pack(fill=tk.BOTH, expand=True)

    def insert_dish(self):
        self.dish_original = Image.open(self.dish_path)
        self.dish_original = self.dish_original.resize((20, 20), Image.ANTIALIAS)
        self.dish = ImageTk.PhotoImage(self.dish_original)
        self.dish_canvas = tk.Label(self.map_canvas, image=self.dish, borderwidth=0).place(x = 1000, y = 200)

    def insert_boat(self):
        self.boat_original = Image.open(self.boat_path)
        self.boat_original = self.boat_original.resize((20, 20), Image.ANTIALIAS)
        self.boat = ImageTk.PhotoImage(self.boat_original)
        self.boat_canvas = tk.Label(self.map_canvas, image=self.boat, borderwidth=0).place(x = 1100, y = 100)

    def create_line(self):
        self.map_canvas.create_line(1010, 210, 1110, 110, width=2, fill='red')

root = tk.Tk()
root.geometry("1280x960")
root.title("NeXtRAD NTPCS Visualisation")

app = Application(master=root)
app.mainloop()