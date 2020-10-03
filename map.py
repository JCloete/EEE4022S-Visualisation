import time
import tkinter as tk
from PIL import ImageTk, Image

import math



class Dish():
    def __init__(self, x_pos=0, y_pos=0, altitude=1, azimuth=0, elevation=0):
        self.x_position = x_pos
        self.y_position = y_pos
        self.altitude = altitude
        self.azimuth = azimuth
        self.elevation = elevation

        self.image_path = 'dish.png'

        self.create_image()

    def create_image(self):
        # Create Image
        dish_original = Image.open(self.image_path)
        dish_original = dish_original.resize((20, 20), Image.ANTIALIAS)

        # Work out angle rotation
        angle = self.rotation()
        

        self.dish_img = ImageTk.PhotoImage(dish_original.rotate(angle))


    # TODO: Add in Limits to azimuth and elevation
    def adjust_azimuth(self, adjustment):
        if (self.azimuth <= 0) and (adjustment == -1):
            self.azimuth = 359
        elif (self.azimuth >= 359) and (adjustment == 1):
            self.azimuth = 0
        else:
            self.azimuth += adjustment

        # Create Image
        dish_original = Image.open(self.image_path)
        dish_original = dish_original.resize((20, 20), Image.ANTIALIAS)

        # Work out angle rotation
        angle = self.rotation()

        self.dish_img = ImageTk.PhotoImage(dish_original.rotate(angle))

    def adjust_elevation(self, adjustment):
        self.elevation += adjustment

    def rotation(self):
        adjusted_angle = 0

        if (self.azimuth >= 45):
            adjusted_angle = 360 - (self.azimuth - 45)
        else:
            adjusted_angle = 45 - self.azimuth

        return adjusted_angle

class Boat():
    def __init__(self, x_pos=0, y_pos=0, altitude=1):
        self.x_position = x_pos
        self.y_position = y_pos
        self.altitude = altitude

        self.image_path = 'boat.jpg'

        self.create_image()

    def create_image(self):
        # Create Image
        boat_original = Image.open(self.image_path)
        boat_original = boat_original.resize((20, 20), Image.ANTIALIAS)
        self.boat_img = ImageTk.PhotoImage(boat_original)

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)

        # Path for images
        self.map_path = 'Test.jpg'
        self.dish_path = 'dish.png'
        self.boat_path = 'boat.jpg'

        self.create_base_layout()
        self.insert_map()
        self.insert_dish()
        self.insert_boat()
        self.create_controls()
        self.create_info_panel()

        self.create_line()
        self.draw()

    def create_base_layout(self):
        # Create a Top canvas to draw on
        self.map_canvas = tk.Canvas(self.master, width=1280, height=760)
        self.map_canvas.pack(fill=tk.BOTH, expand=True)

        # Create a bottom frame for UI
        self.bottom_frame = tk.Frame(self.master, relief=tk.RAISED, borderwidth=1)
        self.bottom_frame.pack(side = tk.BOTTOM, fill=tk.BOTH, expand=False)

        # button to exit program - TODO: PUT THIS IN A CONTROL GENERATION METHOD
        self.quit_button = tk.Button(self.bottom_frame, text="Quit", fg="red", command=self.master.destroy, width=5, height=2)
        self.quit_button.pack( side = tk.RIGHT, padx=5, pady=5)

    def create_controls(self):
        # ===============================================================================================
        # Controls Frame
        self.control_frame = tk.Frame(self.bottom_frame, relief=tk.RAISED, borderwidth=1)

        # Configure Grid for the buttons
        self.control_frame.columnconfigure(0, pad=3)
        self.control_frame.columnconfigure(1, pad=3)
        self.control_frame.columnconfigure(2, pad=3)

        self.control_frame.rowconfigure(0, pad=3)
        self.control_frame.rowconfigure(1, pad=3)
        self.control_frame.rowconfigure(2, pad=3)

        # Create the relevant Buttons
        self.up_button = tk.Button(self.control_frame, text="Up", command=self.turn_up, width=5, height=2)
        self.up_button.grid(row=0, column=1)

        self.left_button = tk.Button(self.control_frame, text="CCW", command=self.turn_CCW, width=5, height=2)
        self.left_button.grid(row=1, column=0)

        self.right_button = tk.Button(self.control_frame, text="CW", command=self.turn_CW, width=5, height=2)
        self.right_button.grid(row=1, column=2)

        self.down_button = tk.Button(self.control_frame, text="Down", command=self.turn_down, width=5, height=2)
        self.down_button.grid(row=2, column=1)

        self.control_frame.pack(side = tk.LEFT, fill=tk.BOTH, expand=False)

    def create_info_panel(self):
        # =============================================================================================================
        # Info Frame
        self.info_frame = tk.Frame(self.bottom_frame, borderwidth=1)

        # Configure Grid for the Buttons
        self.info_frame.columnconfigure(0, pad=3)
        self.info_frame.columnconfigure(1, pad=3)
        self.info_frame.columnconfigure(2, pad=3)
        self.info_frame.columnconfigure(3, pad=3)

        self.info_frame.rowconfigure(0, pad=3)
        self.info_frame.rowconfigure(1, pad=3)

        # Create the relevant labels
        # Generate Azimuth changing variable
        self.azimuth_var = tk.IntVar()
        self.azimuth_var.set(self.dish.azimuth)

        # Generate Azimuth Display
        self.azimuth_display = tk.Label(self.info_frame, text="Azimuth:", relief=tk.GROOVE, width=8, height=1)
        self.azimuth_display.grid(row=0, column=0)
        self.azimuth_display_box = tk.Label(self.info_frame, textvariable=self.azimuth_var, relief=tk.SUNKEN, width=4, height=1)
        self.azimuth_display_box.grid(row=0, column=1)

        # Generate Azimuth changing variable
        self.elevation_var = tk.IntVar()
        self.elevation_var.set(self.dish.elevation)

        # Generate Elevation Display
        self.elevation_display = tk.Label(self.info_frame, text="Elevation:", relief=tk.GROOVE, width=8, height=1)
        self.elevation_display.grid(row=1, column=0)
        self.elevation_display_box = tk.Label(self.info_frame, textvariable=self.elevation_var, relief=tk.SUNKEN, width=4, height=1)
        self.elevation_display_box.grid(row=1, column=1)

        # Generate Units
        self.elevation_units = tk.Label(self.info_frame, text=u"\N{DEGREE SIGN} (deg)")
        self.elevation_units.grid(row=1, column=3)
        self.azimuth_units = tk.Label(self.info_frame, text=u"\N{DEGREE SIGN} (deg)")
        self.azimuth_units.grid(row=0, column=3)

        self.info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        # =============================================================================================================

    def insert_map(self):
        self.map_original = Image.open(self.map_path)
        self.map_original = self.map_original.resize((1280, 840), Image.ANTIALIAS)
        self.map = ImageTk.PhotoImage(self.map_original)

        self.map_display = self.map_canvas.create_image(0, 0, anchor=tk.NW, image=self.map)

    def insert_dish(self):
        # Variables for Dish data
        self.dish = Dish(1000, 200, 1, 0, 0)

        self.dish_canvas = tk.Label(self.map_canvas, image=self.dish.dish_img, borderwidth=0).place(x = self.dish.x_position, y = self.dish.y_position)

    # Depreciated
    def insert_boat(self):
        self.boat = Boat(1100, 100, 0)

        self.boat_canvas = tk.Label(self.map_canvas, image=self.boat.boat_img, borderwidth=0).place(x = self.boat.x_position, y = self.boat.y_position)

    def create_line(self):
        # Line variables
        self.line_start_position_x = self.dish.x_position + 10
        self.line_start_position_y = self.dish.y_position + 10

        self.line_end_position_x = self.line_start_position_x
        self.line_end_position_y = self.line_start_position_y

        #self.line_end_position_x = self.line_start_position_x + 100 * math.sin(self.dish.azimuth * ((2*math.pi)/360))
        #self.line_end_position_y = self.line_start_position_y - 100 * math.cos(self.dish.azimuth * ((2*math.pi)/360))

        self.map_canvas.create_line(self.line_start_position_x, self.line_start_position_y, self.line_end_position_x, self.line_end_position_y, width=2, fill='red', tags="direction")

    def turn_CCW(self):
        # Turn the line CCW
        self.dish.adjust_azimuth(-1)

    def turn_CW(self):
        # Turn the line CW
        self.dish.adjust_azimuth(1)

    def turn_up(self):
        # Adjust elevation upwards
        self.dish.adjust_elevation(1)

    def turn_down(self):
        # Adjust elevation upwards
        self.dish.adjust_elevation(-1)

    def draw(self):
        # Draw Radar
        self.map_canvas.delete(self.dish_canvas)
        self.dish_canvas = tk.Label(self.map_canvas, image=self.dish.dish_img, borderwidth=0).place(x = self.dish.x_position, y = self.dish.y_position)

        # Draw Boat
        self.map_canvas.delete(self.boat_canvas)
        self.boat_canvas = tk.Label(self.map_canvas, image=self.boat.boat_img, borderwidth=0).place(x = self.boat.x_position, y = self.boat.y_position)

        # Draw Line
        self.line_end_position_x = self.line_start_position_x + 300 * math.sin(self.dish.azimuth * ((2*math.pi)/360))
        self.line_end_position_y = self.line_start_position_y - 300 * math.cos(self.dish.azimuth * ((2*math.pi)/360))

        self.map_canvas.coords("direction", (self.line_start_position_x, self.line_start_position_y, self.line_end_position_x, self.line_end_position_y))
        self.after(50, self.draw)

        # Update Labels
        self.azimuth_var.set(self.dish.azimuth)
        self.elevation_var.set(self.dish.elevation)

def main():
    root = tk.Tk()
    root.geometry("1280x960")
    root.title("NeXtRAD NTPCS Visualisation")

    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()