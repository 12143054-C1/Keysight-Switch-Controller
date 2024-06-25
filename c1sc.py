from kivy.config import Config
# Disable resizing the window
Config.set('graphics', 'resizable', False)
Config.set('input', 'mouse', 'mouse,disable_multitouch')

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Ellipse, Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.image import Image  # Import Image widget
from kivy.core.window import Window
from math import sin, cos, pi
from switch_connector_name_dict import Switch_Connector_Name_Dict
from manual_switch_control import Switch_Class

switch_connector_name_dict = Switch_Connector_Name_Dict()
switch_connector_name_dict = switch_connector_name_dict.switch_connector_name_dict

switch_api = Switch_Class()

class CircleGroup(Widget):
    ellipse_count = 0  # Class-level variable to keep track of ellipses

    def __init__(self, center_x, center_y, circle_radius, distance, **kwargs):
        super(CircleGroup, self).__init__(**kwargs)
        self.center_x = center_x
        self.center_y = center_y
        self.circle_radius = circle_radius
        self.distance = distance
        self.ellipses = {}  # Dictionary to store ellipses with unique names
        self.selected_ellipse = None  # Instance-level variable to keep track of selected ellipse
        self.draw_group()

    def draw_group(self):
        with self.canvas:
            Color(0.8706, 0.8706, 0.8627, 1)  # Set the color to grey
            large_radius = (self.distance + self.circle_radius) * 1.1
            Ellipse(pos=(self.center_x - large_radius, self.center_y - large_radius), size=(2 * large_radius, 2 * large_radius))

            radius = self.circle_radius
            distance = self.distance

            Color(0.5, 0.5, 0.5, 1)  # Set the color to grey for the small circles
            x = self.center_x - radius
            y = self.center_y - radius
            ellipse = Ellipse(pos=(x, y), size=(2 * radius, 2 * radius))
            big_ellipse_name = switch_connector_name_dict[f"g_{CircleGroup.ellipse_count}"]
            # Add label for the ellipse name
            label_x = x - 33
            label_y = y + 110
            label = Label(
                color='black',
                text=big_ellipse_name,
                pos=(label_x, label_y),
                size_hint=(None, None),
                size=(100, 30),
                halign='center',
                valign='middle',
                font_name='Roboto-Bold'  # Make the text bold
            )

            self.add_widget(label)


            label_distance = 45  # Distance from the ellipse center to the label
            for i in range(6):
                Color(0.5, 0.5, 0.5, 1)  # Set the color to grey for the small circles
                angle = i * (2 * pi / 6)  # Divide the circle into 6 parts
                x = self.center_x + distance * cos(angle) - radius
                y = self.center_y + distance * sin(angle) - radius
                ellipse = Ellipse(pos=(x, y), size=(2 * radius, 2 * radius))

                # Assign a unique name to each ellipse
                CircleGroup.ellipse_count += 1
                ellipse_name = switch_connector_name_dict[f"{CircleGroup.ellipse_count}"]
                self.ellipses[ellipse_name] = {
                    'ellipse': ellipse,
                    'pos': (x, y),
                    'size': (2 * radius, 2 * radius)
                }

                # Add label for the ellipse name
                label_x = x - 33 + label_distance * cos(angle)
                label_y = y + label_distance * sin(angle)
                label = Label(
                    color='black',
                    text=ellipse_name,
                    pos=(label_x, label_y),
                    size_hint=(None, None),
                    size=(100, 30),
                    halign='center',
                    valign='middle'
                )
                self.add_widget(label)

    def on_touch_down(self, touch):
        for name, ellipse_data in self.ellipses.items():
            x, y = ellipse_data['pos']
            w, h = ellipse_data['size']
            if x <= touch.x <= x + w and y <= touch.y <= y + h:
                self.on_ellipse_press(name)
                break
        return super().on_touch_down(touch)

    def on_ellipse_press(self, name):
        if self.selected_ellipse is not None:
            self.reset_ellipse_color(self.selected_ellipse)
        self.set_ellipse_color(name)
        self.selected_ellipse = name
        print(name)

    def set_ellipse_color(self, name):
        ellipse_data = self.ellipses[name]
        ellipse = ellipse_data['ellipse']
        self.canvas.add(Color(1, 0, 0, 1))  # Set the color
        self.canvas.add(Ellipse(pos=ellipse_data['pos'], size=ellipse_data['size']))

    def reset_ellipse_color(self, name):
        ellipse_data = self.ellipses[name]
        ellipse = ellipse_data['ellipse']
        self.canvas.add(Color(0.5, 0.5, 0.5, 1))  # Reset the color to grey
        self.canvas.add(Ellipse(pos=ellipse_data['pos'], size=ellipse_data['size']))


class ThreeCircles(Widget):
    ellipse_count = 0  # Class-level variable to keep track of ellipses

    def __init__(self, center_x, center_y, circle_radius, distance, **kwargs):
        super(ThreeCircles, self).__init__(**kwargs)
        self.center_x = center_x
        self.center_y = center_y
        self.circle_radius = circle_radius
        self.distance = distance
        self.ellipses = {}  # Dictionary to store ellipses with unique names
        self.selected_ellipse = None  # Instance-level variable to keep track of selected ellipse
        self.draw_circles()

    def draw_circles(self):
        with self.canvas:
            radius = self.circle_radius
            distance = self.distance

            for i in range(3):
                Color(0.5, 0.5, 0.5, 1)  # Set the color to grey for the small circles
                x = self.center_x + distance * (i - 1)  # Place circles in a row
                y = self.center_y
                ellipse = Ellipse(pos=(x - radius, y - radius), size=(2 * radius, 2 * radius))
                if i in [0, 2]:
                    # Assign a unique name to each ellipse
                    ThreeCircles.ellipse_count += 1
                    ellipse_name = switch_connector_name_dict[f"{ThreeCircles.ellipse_count}_mid"]
                    self.ellipses[ellipse_name] = {
                        'ellipse': ellipse,
                        'pos': (x - radius, y - radius),
                        'size': (2 * radius, 2 * radius)
                    }

                    # Add label for the ellipse name
                    label_x = x - distance
                    label_y = y + 12
                    label = Label(
                        color='black',
                        text=ellipse_name,
                        pos=(label_x, label_y),
                        size_hint=(None, None),
                        size=(100, 30),
                        halign='center',
                        valign='middle'
                    )
                    self.add_widget(label)

    def on_touch_down(self, touch):
        for name, ellipse_data in self.ellipses.items():
            x, y = ellipse_data['pos']
            w, h = ellipse_data['size']
            if x <= touch.x <= x + w and y <= touch.y <= y + h:
                self.on_ellipse_press(name)
                break
        return super().on_touch_down(touch)

    def on_ellipse_press(self, name):
        if self.selected_ellipse is not None:
            self.reset_ellipse_color(self.selected_ellipse)
        self.set_ellipse_color(name)
        self.selected_ellipse = name
        print(name)

    def set_ellipse_color(self, name):
        ellipse_data = self.ellipses[name]
        ellipse = ellipse_data['ellipse']
        self.canvas.add(Color(1, 0, 0, 1))  # Set the color 
        self.canvas.add(Ellipse(pos=ellipse_data['pos'], size=ellipse_data['size']))

    def reset_ellipse_color(self, name):
        ellipse_data = self.ellipses[name]
        ellipse = ellipse_data['ellipse']
        self.canvas.add(Color(0.5, 0.5, 0.5, 1))  # Reset the color to grey
        self.canvas.add(Ellipse(pos=ellipse_data['pos'], size=ellipse_data['size']))


class CustomFloatLayout(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.7216, 0.7098, 0.6902, 1)  # Set the background color
            self.bg_rect = Rectangle(size=Window.size)

        Window.bind(on_resize=self.update_background)

    def update_background(self, *args):
        self.bg_rect.size = Window.size


class SwitchApp(App):
    def build(self):
        # Set the window size and make it non-resizable
        Window.size = (1600, 900)
        Window.minimum_width = 1600
        Window.minimum_height = 900

        layout = CustomFloatLayout()
        self.layout = layout

        # Parameters for the groups
        self.circle_radius = 17
        self.group_distance = 260  # Distance from the center to the surrounding groups
        self.group_radius = 60

        # Add the image to the top left corner
        self.logo = Image(source='Keysight-Logo.png', size_hint=(None, None), size=(200, 100), pos=(10, Window.height - 90))
        layout.add_widget(self.logo)

        self.add_group_sets()
        self.add_middle_circles()

        # Add the IP entry box, connect button, and indicator light
        self.add_connection_widgets()

        #Window.bind(on_resize=self.on_window_resize)

        return layout

    def add_group_sets(self):
        self.layout.clear_widgets()

        # Re-add the logo after clearing widgets
        self.layout.add_widget(self.logo)

        self.center_y = Window.height / 2
        self.center_x = Window.width / 2

        left_offset = self.center_x - 400
        right_offset = self.center_x + 400

        # Function to add a set of 7 groups centered at (center_x, center_y)
        def add_group_set(center_x):
            # Add the central group
            central_group = CircleGroup(center_x, self.center_y, self.circle_radius, self.group_radius)
            self.layout.add_widget(central_group)

            # Calculate and add the surrounding groups
            for i in range(6):
                angle = i * (2 * pi / 6)  # Divide the circle into 6 parts
                group_center_x = center_x + self.group_distance * cos(angle)
                group_center_y = self.center_y + self.group_distance * sin(angle)
                group_widget = CircleGroup(group_center_x, group_center_y, self.circle_radius, self.group_radius)
                self.layout.add_widget(group_widget)

        # Add the two sets of groups
        add_group_set(left_offset)
        add_group_set(right_offset)

    def add_middle_circles(self):
        center_y = Window.height / 2
        center_x = Window.width / 2

        # Add the first set of 3 circles
        three_circles_1 = ThreeCircles(center_x, center_y - 310, self.circle_radius, 50)
        self.layout.add_widget(three_circles_1)

        # Add the second set of 3 circles
        three_circles_2 = ThreeCircles(center_x, center_y - 230, self.circle_radius, 50)
        self.layout.add_widget(three_circles_2)

    def add_connection_widgets(self):
        self.ip_input = TextInput(
            hint_text="Enter IP address",
            size_hint=(None, None),
            size=(200, 30),
            pos=(10, 10)
        )

        self.connect_button = Button(
            text="Connect",
            size_hint=(None, None),
            size=(100, 30),
            pos=(220, 10)
        )
        self.connect_button.bind(on_press=self.connect_to_switch)

        with self.layout.canvas:
            self.indicator_color = Color(0.5, 0.5, 0.5, 1)  # Grey color for the indicator light
            self.indicator = Ellipse(pos=(330, 14), size=(20, 20))

        self.layout.add_widget(self.ip_input)
        self.layout.add_widget(self.connect_button)

    def connect_to_switch(self, instance):
        self.update_indicator_color((.5, .5, .5, 1))
        ip_address = self.ip_input.text
        if self.validate_ip(ip_address):
            self.update_indicator_color((0, 1, 0, 1))  # Green color for connected
            print("IP OK")
        else:
            self.update_indicator_color((1, 0, 0, 1))  # Red color for error
            print("Connection Failed")

    def update_indicator_color(self, color):
        self.indicator_color.rgba = color  # Update the color directly

    def validate_ip(self, ip):
        if switch_api.connect(ip):
            return True
        else:
            return False

    def on_window_resize(self, *args):
        self.update_logo_position()
        self.add_group_sets()
        self.add_middle_circles()

    def update_logo_position(self):
        self.logo.pos = (10, Window.height - self.logo.height - 10)


if __name__ == "__main__":
    SwitchApp().run()
