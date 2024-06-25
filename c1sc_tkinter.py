import tkinter as tk
from tkinter import ttk
import math, os, sys, pickle, tempfile

from manual_switch_control import Switch_Class
sc = Switch_Class()

# import button name dictionary
from switch_connector_name_dict import Switch_Connector_Name_Dict
button_name_dict = Switch_Connector_Name_Dict()
button_name_dict = button_name_dict.tkinter_buttons_dictionary

# Add keys for the new circle groups to the dictionary
additional_keys = [
    "top1_circle_1", "top1_circle_2", "top1_circle_3",
    "top2_circle_1", "top2_circle_2", "top2_circle_3",
    "bottom1_circle_1", "bottom1_circle_2", "bottom1_circle_3",
    "bottom2_circle_1", "bottom2_circle_2", "bottom2_circle_3"
]

for key in additional_keys:
    if key not in button_name_dict:
        button_name_dict[key] = key  # Set the key itself as the value or set it to an empty string ""

class CircleGenerator(tk.Tk):
    def __init__(self, big_radius, small_radius, distance, distance_out, label_distance, group_label_distance):
        super().__init__()

        self.title("Switch Controller")
        if getattr(sys, 'frozen', False):
            # we are running in a bundle
            bundle_dir = sys._MEIPASS
        else:
            # we are running in a normal Python environment
            bundle_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(bundle_dir, 'remote-control.ico')
        self.iconbitmap(icon_path)
        self.resizable(False,False)

        self.big_radius = big_radius
        self.small_radius = small_radius
        self.distance = distance
        self.distance_out = distance_out
        self.label_distance = label_distance
        self.group_label_distance = group_label_distance
        self.selected_circles = {}
        self.button_names = []

        self.global_width = 1200
        self.global_height = 550

        self.canvas = tk.Canvas(self, width=self.global_width, height=self.global_height, bg="#b0ada8")  # Adjust height to accommodate new sets
        self.canvas.pack()

        # Frame for IP address entry and Connect button
        self.frame1 = tk.Frame(self)
        self.frame1.pack(fill="x")

        self.ip_combobox = ttk.Combobox(self.frame1)
        self.ip_combobox.grid(row=0, column=0, padx=5)
        self.load_ip_history()

        self.connect_button = tk.Button(self.frame1, text="Connect", command=self.connect)
        self.connect_button.grid(row=0, column=1, padx=5)

        self.indicator = tk.Label(self.frame1, text=" ", bg="grey", width=2, height=1)
        self.indicator.grid(row=0, column=2, padx=5)

        # Bottom frame with copyright notice
        self.frame2 = tk.Frame(self, relief="ridge", borderwidth=2)
        self.frame2.pack(fill="x")

        self.copyright_label = tk.Label(self.frame2, text="© 2024 Sivan Zusin", anchor="e")
        self.copyright_label.pack(side="right", padx=5)

        self.update_canvas()
        #self.print_button_names()


    def update_canvas(self):
        self.canvas.delete("all")
        big_radius = self.big_radius
        small_radius = self.small_radius
        distance = self.distance

        width, height = self.global_width, self.global_height  # Adjust height to accommodate new sets
        center_x1, center_y1 = width // 4, height // 2  # Center for first set
        center_x2, center_y2 = 3 * width // 4, height // 2  # Center for second set

        # Draw the first set of circle groups
        self.draw_circle_group(center_x1, center_y1, big_radius, small_radius, distance, "center1")

        for i in range(6):
            angle = math.radians(i * 60)
            group_center_x = center_x1 + (2 * self.distance_out + big_radius + small_radius) * math.cos(angle)
            group_center_y = center_y1 + (2 * self.distance_out + big_radius + small_radius) * math.sin(angle)
            self.draw_circle_group(group_center_x, group_center_y, big_radius, small_radius, distance, f"group1_{i+1}")

        # Draw the second set of circle groups
        self.draw_circle_group(center_x2, center_y2, big_radius, small_radius, distance, "center2")

        for i in range(6):
            angle = math.radians(i * 60)
            group_center_x = center_x2 + (2 * self.distance_out + big_radius + small_radius) * math.cos(angle)
            group_center_y = center_y2 + (2 * self.distance_out + big_radius + small_radius) * math.sin(angle)
            self.draw_circle_group(group_center_x, group_center_y, big_radius, small_radius, distance, f"group2_{i+1}")

        # Draw the additional instances of 3 circles each
        y = (self.global_height + 300 )/ 2
        self.draw_three_circle_group(width // 2, y, "bottom1")
        self.draw_three_circle_group(width // 2, y + 50, "bottom2")

    def draw_circle_group(self, center_x, center_y, big_radius, small_radius, distance, group_tag):
        # Draw the label for the group
        label_x = center_x
        label_y = center_y - big_radius - self.group_label_distance
        self.canvas.create_text(label_x, label_y, text=button_name_dict.get(group_tag, group_tag), fill="black", font=("Helvetica", 11, "bold"))

        # Draw the big circle
        self.canvas.create_oval(center_x - big_radius, center_y - big_radius, center_x + big_radius, center_y + big_radius, outline="#d7d4d3", fill="#d7d4d3", tags=group_tag)
        self.selected_circles[group_tag] = None

        for i in range(6):
            angle = math.radians(i * 60)
            small_center_x = center_x + distance * math.cos(angle)
            small_center_y = center_y + distance * math.sin(angle)
            tag_name = f"{group_tag}_circle_{i+1}"
            self.button_names.append(tag_name)
            self.canvas.create_oval(small_center_x - small_radius, small_center_y - small_radius, small_center_x + small_radius, small_center_y + small_radius, outline="#888888", fill="#888888", tags=tag_name)
            self.canvas.tag_bind(tag_name, "<Button-1>", self.on_circle_click)

            # Add label
            label_x = center_x + (distance + self.label_distance) * math.cos(angle)
            label_y = center_y + (distance + self.label_distance) * math.sin(angle)
            self.canvas.create_text(label_x, label_y, text=button_name_dict.get(tag_name, tag_name), fill="black", font=("Helvetica", 10))

    def draw_three_circle_group(self, base_x, base_y, group_tag):
        spacing = self.distance_out * 0.8
        for i in range(3):
            center_x = base_x + (i - 1) * spacing
            center_y = base_y
            tag_name = f"{group_tag}_circle_{i+1}"
            self.button_names.append(tag_name)
            self.canvas.create_oval(center_x - self.small_radius, center_y - self.small_radius, center_x + self.small_radius, center_y + self.small_radius, outline="#888888", fill="#888888", tags=tag_name)
            if i in [0,2]:
                self.canvas.tag_bind(tag_name, "<Button-1>", self.on_circle_click)
                self.canvas.create_text(center_x, center_y - self.label_distance + 15, text=button_name_dict[tag_name], fill="black", font=("Helvetica", 10))

    def on_circle_click(self, event):
        clicked_item = self.canvas.find_withtag("current")[0]
        tags = self.canvas.gettags(clicked_item)
        group_tag = tags[0].rsplit("_circle_", 1)[0]

        # Reset the previous selected circle in the same group to its original color
        if self.selected_circles.get(group_tag):
            self.canvas.itemconfig(self.selected_circles[group_tag], fill="#888888")

        # Set the clicked circle to red
        self.canvas.itemconfig(clicked_item, fill="#ff0000")
        self.selected_circles[group_tag] = clicked_item
        closed_relay = button_name_dict[tags[0]]
        print(f"Clicked on: {closed_relay}")
        if sc.switch_obj:
            sc.close_relay(closed_relay)

    def print_button_names(self):
        print("Button names:")
        for name in self.button_names:
            print(name)

    def connect(self):
        ip_address = self.ip_combobox.get()
        # Simulate a connection attempt (this should be replaced with actual connection logic)
        if sc.connect(ip_address):  # Example condition for a successful connection
            self.indicator.config(bg="#00ee00")
            self.init_relays(True)
            self.save_ip_history(ip_address)
        else:
            self.indicator.config(bg="red")
            self.init_relays(False)

    def paint_all_circles_grey(self):
        for tag_name in self.button_names:
            self.canvas.itemconfig(tag_name, fill="#888888")

    def init_relays(self, success):
        if success:
            self.paint_all_circles_grey()
            for tag_name in self.button_names:
                if button_name_dict[tag_name]:
                    print(button_name_dict[tag_name])
                    status = sc.get_individual_relay_status(button_name_dict[tag_name])
                    status = int(status.strip())
                    if not status:
                        self.canvas.itemconfig(tag_name, fill="#ff0000")
                        self.on_circle_click_with_tag(tag_name)
        else:
            self.paint_all_circles_grey()

    def on_circle_click_with_tag(self, tag_name):
        clicked_item = self.canvas.find_withtag(tag_name)[0]
        tags = self.canvas.gettags(clicked_item)
        group_tag = tags[0].rsplit("_circle_", 1)[0]

        # Reset the previous selected circle in the same group to its original color
        if self.selected_circles.get(group_tag):
            self.canvas.itemconfig(self.selected_circles[group_tag], fill="#888888")

        # Set the clicked circle to red
        self.canvas.itemconfig(clicked_item, fill="#ff0000")
        self.selected_circles[group_tag] = clicked_item

    def load_ip_history(self):
        try:
            with open(os.path.join(tempfile.gettempdir(), 'ip_history.pkl'), 'rb') as f:
                ip_history = pickle.load(f)
                self.ip_combobox['values'] = ip_history
                if ip_history:
                    self.ip_combobox.set(ip_history[0])
        except (FileNotFoundError, EOFError):
            self.ip_combobox['values'] = []

    def save_ip_history(self, ip_address):
        ip_history = list(self.ip_combobox['values'])
        if ip_address in ip_history:
            ip_history.remove(ip_address)
        ip_history.insert(0, ip_address)
        with open(os.path.join(tempfile.gettempdir(), 'ip_history.pkl'), 'wb') as f:
            pickle.dump(ip_history, f)
        self.ip_combobox['values'] = ip_history

if __name__ == "__main__":
    # Set your desired values here
    big_circle_radius = 50
    small_circle_radius = 10
    distance_from_center = 33
    distance_out = 60
    label_distance = 35
    group_label_distance = 22

    app = CircleGenerator(big_circle_radius, small_circle_radius, distance_from_center, distance_out, label_distance, group_label_distance)
    app.mainloop()
    sc.disconnect()
