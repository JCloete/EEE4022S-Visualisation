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
        self.elevation = round(self.elevation, 2)

    def rotation(self):
        adjusted_angle = 0

        if (self.azimuth >= 45):
            adjusted_angle = 360 - (self.azimuth - 45)
        else:
            adjusted_angle = 45 - self.azimuth

        return adjusted_angle

class Target():
    def __init__(self, x_pos=0, y_pos=0, altitude=1, image_path=''):
        self.x_position = x_pos
        self.y_position = y_pos
        self.altitude = altitude

        self.image_path = image_path

        self.create_image()

    def create_image(self):
        # Create Image
        image_original = Image.open(self.image_path)
        image_original = image_original.resize((20, 20), Image.ANTIALIAS)
        self.image_tk = ImageTk.PhotoImage(image_original)

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)

        # Path for images
        self.map_path = 'map.png'
        self.dish_path = 'dish.png'

        # Create the base Layer
        self.create_base_layout()

        # Insert all relevant objects
        self.insert_map()
        self.insert_dish()
        self.insert_line()
        self.insert_boat()

        # Insert all the controls
        self.create_controls()
        self.create_info_panel()

        # Draw the Scene
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

        # Icon for settings
        self.settings_icon = ImageTk.PhotoImage(file='settings_icon.png')

        self.settings_button = tk.Button(self.control_frame, image=self.settings_icon, command=self.settings_menu, width=40, height=40)
        self.settings_button.grid(row=1, column=1)

        self.right_button = tk.Button(self.control_frame, text="CW", command=self.turn_CW, width=5, height=2)
        self.right_button.grid(row=1, column=2)

        self.down_button = tk.Button(self.control_frame, text="Down", command=self.turn_down, width=5, height=2)
        self.down_button.grid(row=2, column=1)

        self.control_frame.pack(side = tk.LEFT, fill=tk.BOTH, expand=False)

    def create_info_panel(self):
        # =============================================================================================================
        # Info Frame
        self.info_frame = tk.Frame(self.bottom_frame, borderwidth=2)
        self.info_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create the dish frame
        self.dish_frame = tk.Frame(self.info_frame, relief=tk.RIDGE, borderwidth=3, padx=5)

        # Create the Pedestal labels
        # Generate Title Label
        self.dish_title = tk.Label(self.dish_frame, text="Dish Information", width=16, anchor=tk.CENTER)
        self.dish_title.grid(row=0, column=1, columnspan=3, padx=2, pady=3)

        # Generate Azimuth changing variable
        self.azimuth_var = tk.IntVar()
        self.azimuth_var.set(float(self.dish.azimuth))

        # Generate Azimuth Display
        self.azimuth_display = tk.Label(self.dish_frame, text="Azimuth:", relief=tk.GROOVE, width=8, height=1)
        self.azimuth_display.grid(row=1, column=1, padx=2, pady=3)
        self.azimuth_display_box = tk.Label(self.dish_frame, textvariable=self.azimuth_var, relief=tk.SUNKEN, width=4, height=1)
        self.azimuth_display_box.grid(row=1, column=2)

        # Generate Azimuth changing variable
        self.elevation_var = tk.DoubleVar()
        self.elevation_var.set(self.dish.elevation)

        # Generate Elevation Display
        self.elevation_display = tk.Label(self.dish_frame, text="Elevation:", relief=tk.GROOVE, width=8, height=1)
        self.elevation_display.grid(row=2, column=1)
        self.elevation_display_box = tk.Label(self.dish_frame, textvariable=self.elevation_var, relief=tk.SUNKEN, width=4, height=1)
        self.elevation_display_box.grid(row=2, column=2)

        # Generate Units
        self.azimuth_units = tk.Label(self.dish_frame, text=u"\N{DEGREE SIGN} (deg)")
        self.azimuth_units.grid(row=1, column=3)
        self.elevation_units = tk.Label(self.dish_frame, text=u"\N{DEGREE SIGN} (deg)")
        self.elevation_units.grid(row=2, column=3)
        
        self.dish_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        # ====================================================================================================================================
        # Create the Target frame
        self.target_frame = tk.Frame(self.info_frame, relief=tk.RIDGE, borderwidth=3, padx=5)

        # Create the Target labels
        # Generate title Label
        self.target_title = tk.Label(self.target_frame, text="Target Information", width=16, anchor=tk.CENTER)
        self.target_title.grid(row=0, column=1, columnspan=3, padx=2, pady=3)

        # Generate desired Azimuth changing variable
        self.desired_azimuth_var = tk.IntVar()
        self.desired_azimuth_var.set(self.calculate_azimuth())

        # Generate Azimuth Display
        self.desired_azimuth_display = tk.Label(self.target_frame, text="Desired Azimuth:", relief=tk.GROOVE, width=14, height=1)
        self.desired_azimuth_display.grid(row=1, column=1, padx=2, pady=3)
        self.desired_azimuth_display_box = tk.Label(self.target_frame, textvariable=self.desired_azimuth_var, relief=tk.SUNKEN, width=4, height=1)
        self.desired_azimuth_display_box.grid(row=1, column=2)

        # Generate Azimuth changing variable
        self.desired_elevation_var = tk.DoubleVar()
        self.desired_elevation_var.set(self.dish.elevation)

        # Generate Elevation Display
        self.desired_elevation_display = tk.Label(self.target_frame, text="Desired Elevation:", relief=tk.GROOVE, width=14, height=1)
        self.desired_elevation_display.grid(row=2, column=1)
        self.desired_elevation_display_box = tk.Label(self.target_frame, textvariable=self.desired_elevation_var, relief=tk.SUNKEN, width=4, height=1)
        self.desired_elevation_display_box.grid(row=2, column=2)

        # Generate Units
        self.desired_azimuth_units = tk.Label(self.target_frame, text=u"\N{DEGREE SIGN} (deg)")
        self.desired_azimuth_units.grid(row=1, column=3)
        self.desired_elevation_units = tk.Label(self.target_frame, text=u"\N{DEGREE SIGN} (deg)")
        self.desired_elevation_units.grid(row=2, column=3)

        self.target_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        

    def insert_map(self):
        self.map_original = Image.open(self.map_path)
        self.map_original = self.map_original.resize((1280, 840), Image.ANTIALIAS)
        self.map = ImageTk.PhotoImage(self.map_original)

        self.map_display = self.map_canvas.create_image(0, 0, anchor=tk.NW, image=self.map)

    def insert_dish(self):
        # Variables for Dish data
        self.dish = Dish(350, 470, 1, 0, 0)

        self.dish_canvas = tk.Label(self.map_canvas, image=self.dish.dish_img, borderwidth=0).place(x = self.dish.x_position, y = self.dish.y_position)

    # Depreciated
    def insert_boat(self):
        self.boat = Target(450, 230, 0, 'boat.jpg')

        self.boat_canvas = tk.Label(self.map_canvas, image=self.boat.image_tk, borderwidth=0).place(x = self.boat.x_position, y = self.boat.y_position)

    def insert_line(self):
        # Line variables
        self.line_start_position_x = self.dish.x_position + 10
        self.line_start_position_y = self.dish.y_position + 10

        self.line_end_position_x = self.line_start_position_x
        self.line_end_position_y = self.line_start_position_y

        self.map_canvas.create_line(self.line_start_position_x, self.line_start_position_y, self.line_end_position_x, self.line_end_position_y, width=2, fill='red', tags="direction")

    def turn_CCW(self):
        # Turn the line CCW
        self.dish.adjust_azimuth(-1)

    def turn_CW(self):
        # Turn the line CW
        self.dish.adjust_azimuth(1)

    def turn_up(self):
        # Adjust elevation upwards
        self.dish.adjust_elevation(0.01)

    def turn_down(self):
        # Adjust elevation upwards
        self.dish.adjust_elevation(-0.01)

    def calculate_line_length(self):
        max_length = 300.0

        if self.dish.elevation == 0:
            return max_length

        line_length = (self.dish.altitude - self.boat.altitude) / math.tan(abs(self.dish.elevation) * ((2*math.pi)/360))

        if line_length > max_length:
            return max_length

        return line_length

    def calculate_azimuth(self):
        azimuth = math.atan2(self.boat.x_position - self.dish.x_position, self.boat.y_position - self.dish.y_position)
        azimuth = (180 - azimuth * (180/math.pi)) % 360

        return round(azimuth, 1)

    def calculate_elevation(self):
        length = (math.sqrt((self.boat.x_position - self.dish.x_position)**2 + (self.boat.y_position - self.dish.y_position)**2))
        elevation = math.atan2(float(self.boat.altitude - self.dish.altitude), length) * (180/math.pi)

        return round(elevation, 2)

    def draw(self):
        # Draw Radar
        self.map_canvas.delete(self.dish_canvas)
        self.dish_canvas = tk.Label(self.map_canvas, image=self.dish.dish_img, borderwidth=0).place(x = self.dish.x_position, y = self.dish.y_position)

        # Draw Boat
        self.map_canvas.delete(self.boat_canvas)
        self.boat_canvas = tk.Label(self.map_canvas, image=self.boat.image_tk, borderwidth=0).place(x = self.boat.x_position, y = self.boat.y_position)

        # Draw Line
        line_length = self.calculate_line_length()
        self.line_end_position_x = self.line_start_position_x + line_length * math.sin(self.dish.azimuth * ((2*math.pi)/360))
        self.line_end_position_y = self.line_start_position_y - line_length * math.cos(self.dish.azimuth * ((2*math.pi)/360))

        self.map_canvas.coords("direction", (self.line_start_position_x, self.line_start_position_y, self.line_end_position_x, self.line_end_position_y))
        self.after(50, self.draw)

        # Update Labels
        self.azimuth_var.set(float(self.dish.azimuth))
        self.elevation_var.set(self.dish.elevation)

        self.desired_azimuth_var.set(self.calculate_azimuth())
        self.desired_elevation_var.set(self.calculate_elevation())

    #Settings Menu related functions
    def settings_menu(self):
        # Create the settings menu to adjust Coordinates and set Azimuth/Elevation
        # Create new window
        self.settings_window = tk.Toplevel(self.master)
        self.settings_window.maxsize(250, 250)
        self.settings_window.minsize(250, 250)
        self.settings_frame = tk.Frame(self.settings_window)
        self.settings_frame.pack(fill=tk.BOTH, expand=False)

        # Grids
        # Configure Grid for the buttons
        self.settings_frame.columnconfigure(0, pad=6)
        self.settings_frame.columnconfigure(1, pad=6)

        self.settings_frame.rowconfigure(0, pad=6)
        self.settings_frame.rowconfigure(1, pad=6)
        self.settings_frame.rowconfigure(2, pad=6)
        self.settings_frame.rowconfigure(3, pad=6)
        self.settings_frame.rowconfigure(4, pad=6)
        self.settings_frame.rowconfigure(5, pad=6)
        self.settings_frame.rowconfigure(6, pad=6)
        self.settings_frame.rowconfigure(7, pad=6)
        self.settings_frame.rowconfigure(8, pad=6)
        
        # Create boxes to enter relevant information
        set_desired_azimuth_L = tk.Label(self.settings_frame, text="Desired Azimuth")
        set_desired_azimuth_B = tk.Entry(self.settings_frame)
        set_desired_azimuth_L.grid(row=0, column=0)
        set_desired_azimuth_B.grid(row=0, column=1)

        set_desired_elevation_L = tk.Label(self.settings_frame, text="Desired Elevation")
        set_desired_elevation_B = tk.Entry(self.settings_frame)
        set_desired_elevation_L.grid(row=1, column=0)
        set_desired_elevation_B.grid(row=1, column=1)

        # Target Section
        target_info = tk.Label(self.settings_frame, text="Target Coordinates", relief=tk.GROOVE)
        target_info.grid(row=2, column=0, columnspan=2)

        target_latitude_L = tk.Label(self.settings_frame, text="Latitude")
        target_latitude_L.grid(row=3, column=0)
        target_latitude_B = tk.Entry(self.settings_frame)
        target_latitude_B.grid(row=3, column=1)

        target_longitude_L = tk.Label(self.settings_frame, text="Longitude")
        target_longitude_L.grid(row=4, column=0)
        target_longitude_B = tk.Entry(self.settings_frame)
        target_longitude_B.grid(row=4, column=1)

        # Pedestal Section
        pedestal_info = tk.Label(self.settings_frame, text="Pedestal Coordinates", relief=tk.GROOVE)
        pedestal_info.grid(row=5, column=0, columnspan=2)

        pedestal_latitude_L = tk.Label(self.settings_frame, text="Latitude")
        pedestal_latitude_L.grid(row=6, column=0)
        pedestal_latitude_B = tk.Entry(self.settings_frame)
        pedestal_latitude_B.grid(row=6, column=1)

        pedestal_longitude_L = tk.Label(self.settings_frame, text="Longitude")
        pedestal_longitude_L.grid(row=7, column=0)
        pedestal_longitude_B = tk.Entry(self.settings_frame)
        pedestal_longitude_B.grid(row=7, column=1)

        apply_settings_button = tk.Button(self.settings_frame, text="Apply", command=self.apply_settings)
        apply_settings_button.grid(row=8, column=0)
        destroy_settings = tk.Button(self.settings_frame, text="Cancel", command=self.settings_window.destroy)
        destroy_settings.grid(row=8, column=1)

    def apply_settings(self):
        self.settings_window.destroy()

def main():
    root = tk.Tk()
    root.geometry("1280x960")
    root.title("NeXtRAD NTPCS Visualisation")

    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()