import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import json
import os
import math

IMAGE_PATH = "pathplanner/fll_map_2025.jpg"
OUTPUT_PATH = "pathplanner/points.json"
RUN_PATH = "pathplanner/PathData.json"

class DrawingAppClick:
    def __init__(self, root):
        self.root = root
        self.root.title("FLL Map Point Connector")

        self.bg_image = Image.open(IMAGE_PATH)
        self.tk_image = ImageTk.PhotoImage(self.bg_image)
        self.canvas = tk.Canvas(root, width=self.tk_image.width(), height=self.tk_image.height())
        self.canvas.pack()
        self.canvas.create_image(0, 0, image=self.tk_image, anchor="nw")

        self.canvas.bind("<Button-1>", self.add_point)

        self.spacing_label = tk.Label(root, text="Spacing:")
        self.spacing_label.pack()
        self.spacing_entry = tk.Entry(root)
        self.spacing_entry.insert(0, "1")
        self.spacing_entry.pack()

        button_frame = tk.Frame(root)
        button_frame.pack(pady=5)

        self.print_button = tk.Button(button_frame, text="Print Points", command=self.print_points)
        self.print_button.pack(side="left", padx=5)

        self.time_label = tk.Label(root, text="Time required for the run (seconds):")
        self.time_label.pack()
        self.time_entry = tk.Entry(root)
        self.time_entry.insert(0, "10")
        self.time_entry.pack()

        self.run_name = tk.Label(root, text="The name of the run (e.g. Run 1):")
        self.run_name.pack()
        self.run_entry = tk.Entry(root)
        self.run_entry.insert(0, "Run 1")
        self.run_entry.pack()

        self.speed_button = tk.Button(button_frame, text="Calculate Speed", command=self.calculate_speed)
        self.speed_button.pack(side="left", padx=5)

        self.save_button = tk.Button(button_frame, text="Save Points", command=self.save_points)
        self.save_button.pack(side="left", padx=5)

        self.clear_points_button = tk.Button(button_frame, text="Clear Points (JSON)", command=self.clear_points)
        self.clear_points_button.pack(side="left", padx=5)

        self.clear_button = tk.Button(root, text="Clear lines on the board", command=self.clear_board)
        self.clear_button.pack(pady=5)

        self.clear_data_button = tk.Button(root, text="Clear all user saved data", command=self.clear_data)
        self.clear_data_button.pack()

        self.enter_robot_data = tk.Button(root, text="Calculate Speed in PID terms (use after calculating the speed and input the data gained)", command=self.enter_data)
        self.enter_robot_data.pack(pady=5)

        self.points = []

    def add_point(self, event):
        x, y = event.x, event.y
        self.points.append((x, y))
        r = 3
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill="black")
        if len(self.points) > 1:
            x1, y1 = self.points[-2]
            self.canvas.create_line(x1, y1, x, y, fill="black", width=2)

    def enter_data(self):
        def inches_per_sec_to_pid_speed(inches_per_sec, wheel_diameter_in, encoder_ticks_per_rev, gear_ratio=1.0):
            circumference = math.pi * wheel_diameter_in
            revs_per_sec = inches_per_sec / circumference
            ticks_per_sec = revs_per_sec * encoder_ticks_per_rev * gear_ratio
            pid_speed_value = ticks_per_sec / 10
            return pid_speed_value
        try:
            speed = float(simpledialog.askstring("Input", "Enter speed (inches/second):"))
            diameter = float(simpledialog.askstring("Input", "Enter wheel diameter (inches):"))
            tpr = int(simpledialog.askstring("Input", "Enter encoder ticks per revolution: (avg in EV3: 360 and spike: 720)"))
            gear_ratio = float(simpledialog.askstring("Input", "Enter gear ratio (default 1.0):") or 1.0)

            pid_speed = inches_per_sec_to_pid_speed(speed, diameter, tpr, gear_ratio)
            messagebox.showinfo("Result", f"PID Speed Value: {pid_speed:.2f} ticks/100ms")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def interpolate_points(self, p1, p2, spacing):
        canvas_height = self.tk_image.height()
        x1, y1 = p1
        x2, y2 = p2
        dist = math.hypot(x2 - x1, y2 - y1)
        steps = int(dist // spacing)
        result = []
        for i in range(steps + 1):
            x = int(x1 + (x2 - x1) * i / steps)
            y = canvas_height - int(y1 + (y2 - y1) * i / steps)
            result.append((x, y))
        return result

    def get_all_interpolated_points(self):
        try:
            spacing = float(self.spacing_entry.get())
            if spacing <= 0:
                raise ValueError
        except ValueError:
            spacing = 1
            print("Invalid spacing input. Defaulted to 1.")

        all_points = []
        for i in range(len(self.points) - 1):
            interpolated = self.interpolate_points(self.points[i], self.points[i + 1], spacing)
            all_points.extend(interpolated)
        return all_points, spacing

    def save_points(self):
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        all_points, spacing = self.get_all_interpolated_points()
        with open(OUTPUT_PATH, "w") as f:
            json.dump(all_points, f)
        print(f"Saved {len(all_points)} points with spacing {spacing} to {OUTPUT_PATH}")

    def print_points(self):
        all_points, spacing = self.get_all_interpolated_points()
        print(f"Printing {len(all_points)} points (spacing: {spacing}):")
        for pt in all_points:
            print(pt)

    def clear_points(self):
        os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
        with open(OUTPUT_PATH, "w") as f:
            json.dump([], f)
        print(f"Cleared all points in {OUTPUT_PATH}")

    def clear_board(self):
        self.canvas.delete("all")
        self.canvas_bg = self.canvas.create_image(0, 0, image=self.tk_image, anchor="nw")
        self.points = []
        print("Canvas and points reset.")

    def clear_data(self):
        self.canvas.delete("all")
        self.canvas_bg = self.canvas.create_image(0, 0, image=self.tk_image, anchor="nw")
        self.points = []
        with open(OUTPUT_PATH, "w") as f:
            json.dump([], f)
        with open(RUN_PATH, "w") as f:
            json.dump([], f)
        print("All user data cleared.")
    def calculate_speed(self):
        try:
            time_seconds = float(self.time_entry.get())
            if time_seconds <= 0:
                raise ValueError
        except ValueError:
            print("Invalid time input.")
            return

        interpolated_points, _ = self.get_all_interpolated_points()

        pixels_wide = self.tk_image.width()
        pixels_tall = self.tk_image.height()

        inch_per_pixel_x = 93 / pixels_wide
        inch_per_pixel_y = 45 / pixels_tall

        total_distance_inches = 0
        for i in range(len(interpolated_points) - 1):
            x1, y1 = interpolated_points[i]
            x2, y2 = interpolated_points[i + 1]
            dx = (x2 - x1) * inch_per_pixel_x
            dy = (y2 - y1) * inch_per_pixel_y
            dist = math.hypot(dx, dy)
            total_distance_inches += dist
        total_distance_cm = total_distance_inches * 2.54

        speed_ips = total_distance_inches / time_seconds
        speed_cm = total_distance_cm / time_seconds
        print(f"Path distance: {total_distance_inches:.2f} inches")
        print(f"Required speed: {speed_ips:.2f} inches/second or {speed_cm:.2f} centimeters/second")
        Run_name = self.run_entry.get()
        ListToJson = [Run_name, total_distance_inches, speed_ips]
        os.makedirs(os.path.dirname(RUN_PATH), exist_ok=True)
        with open(RUN_PATH, "w") as f:
            json.dump(ListToJson, f)
        print(f"Saved speed data to PathData.json")

root = tk.Tk()
app = DrawingAppClick(root)
root.mainloop()