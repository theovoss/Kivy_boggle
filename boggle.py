from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

import logging
import re

from bogglesolver.solve_boggle import SolveBoggle

class IntInput(TextInput):

    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        s = re.sub(pat, '', substring)
        return super(IntInput, self).insert_text(s, from_undo=from_undo)

class MenuScreen(GridLayout):
    """First screen to ask how big"""

    def __init__(self, **kwargs):
        logging.info("Menu Screen init.")
        super(MenuScreen, self).__init__(**kwargs)
        
        self.cols = 2

        self.num_columns_input = None
        self.num_rows_input = None
        self.num_columns = 0
        self.num_rows = 0
        self.game_time = 20

        self.buttons = []
        self.ignore = []

        self.solve_boggle = SolveBoggle()

        self.render_menu_screen()
        self.grid = None

    def get_font(self, button, text):
        print("Button size is: %s" % button.size)

    def reset_callback(self, widget=None):
        logging.info("Reset Game Button Callback.")
        self.render_menu_screen()

    def cancel_callback(self, widget=None):
        logging.info("Menu Screen cancel callback.")
        exit()
        return

    def confirm_callback(self, widget=None):
        logging.info("Confirm Button Callback.")
        logging.info("Menu Screen confirm callback.")
        self.num_columns = int(self.num_columns_input.text)
        self.num_rows = int(self.num_rows_input.text)
        self.render_boggle_setup_screen()

    def button_configuration_callback(self, widget=None):
        logging.info("Configuration Game Callback.")
        if widget:
            obj = widget
        else:
            obj = self
        if "enabled" in obj.text:
            obj.text = "[size=%s][color=ff3333]disabled[/color][/size]" % int(self.font)
        else:
            obj.text = "[size=%s][color=52D017]enabled[/color][/size]" % int(self.font)

    def confirm_game_button(self, widget=None):
        logging.info("Confirm Game Button Callback.")
        for i, button in enumerate(self.buttons):
            if "enabled" not in button.text:
                self.ignore.append(i)
        logging.info("Ignore indexes are: %s" % self.ignore)
        self.game_time = int(self.game_time_input.text)
        # clear the buttons so the new ones can be added.
        self.buttons = []
        self.render_boggle_game_screen()

        logging.info("Time to sleep.")

    def render_menu_screen(self):
        logging.info("Rendering Menu Screen.")
        self.clear_widgets()
        self.cols = 2
        self.grid = None
        self.add_widget(Label(text='Rows'))
        self.num_rows_input = IntInput(text='4')
        self.add_widget(self.num_rows_input)
        self.add_widget(Label(text='Columns'))
        self.num_columns_input = IntInput(text='4')
        self.add_widget(self.num_columns_input)
        self.add_widget(Label(text='Game Time (sec)'))
        self.game_time_input = IntInput(text=str(self.game_time))
        self.add_widget(self.game_time_input)
        self.cancel_button = Button(text="Cancel Boggle")
        self.cancel_button.bind(on_press=self.cancel_callback)
        self.add_widget(self.cancel_button)
        self.confirm_button = Button(text="Confirm Inputs")
        self.confirm_button.bind(on_press=self.confirm_callback)
        self.add_widget(self.confirm_button)

    def render_boggle_setup_screen(self):
        logging.info("Rendering Boggle Setup Screen.")

        self.clear_widgets()
        self.cols = 1
        if self.grid:
            self.grid = None
        
        self.grid = GridLayout(size_hint=(1, self.num_rows / (self.num_rows + 1.0)))
        self.render_boggle_layout("[color=52D017]enabled[/color]", self.button_configuration_callback, self.grid)
        self.add_widget(self.grid)
        h_box = BoxLayout(orientation='horizontal', size_hint=(1, 1 / (self.num_rows + 1.0)))
        self.reset_button = Button(text="Reset")
        self.reset_button.bind(on_press=self.reset_callback)
        h_box.add_widget(self.reset_button)
        self.confirm_board_button = Button(text="Confirm Board")
        self.confirm_board_button.bind(on_press=self.confirm_game_button)
        h_box.add_widget(self.confirm_board_button)
        self.add_widget(h_box)

    def render_boggle_game_screen(self):
        logging.info("Rendering game screen.")

        self.clear_widgets()

        def handle_swipe_callback(self):
            # TODO: add in swipes or keyboard for user to input words.
            pass

        self.solve_boggle.set_board(self.num_columns, self.num_rows, None)
        logging.info("Solve Boggle created.")
        self.render_boggle_layout("", handle_swipe_callback, self.grid)
        logging.info("About to loop through buttons.")
        for i, button in enumerate(self.buttons):
            if i not in self.ignore:
                button.text = "[size=%s]%s[/size]" % (int(self.font), self.solve_boggle.boggle.boggle_array[i].upper())
            else:
                button.text = ""

        timer = Label(text="%s" % self.game_time, size_hint=(1, 1.0/self.num_rows), font_size=self.font)

        def timer_callback(dt):
            timer.text = str(int(timer.text) -1)
            if int(timer.text) == 0:
                self.render_boggle_solution_screen()

        Clock.schedule_interval(timer_callback, 1)

        self.add_widget(self.grid)
        self.add_widget(timer)

        # TODO: make this part of a function for a timer callback so it doesn't take time away from displaying the screen.
        self.words = self.solve_boggle.solve(ignore_indexes=self.ignore)
        logging.info("Got words.")

    def render_boggle_layout(self, text, callback, grid_layout):
        logging.info("Rendering Boggle Layout.")
        grid_layout.clear_widgets()
        self.buttons = []

        grid_layout.cols = self.num_columns
        if len(text) > 1:
            self.font = self.width / (self.num_columns + len(text) - 2)
        else:
            self.font = self.height / (self.num_rows * 2)

        for index in range(0, self.num_rows * self.num_columns):
            self.buttons.append(Button(text="[size=%s]%s[/size]" % (int(self.font), text), markup=True))
            self.buttons[index].bind(on_press=callback)
            grid_layout.add_widget(self.buttons[index])

    def render_boggle_solution_screen(self):
        logging.info("Rendering Boggle Solution Screen.")

        self.clear_widgets()
        self.buttons = []

        hor_lay = GridLayout(cols=2)
        vert_lay = GridLayout(cols=1, size_hint=(0.25, 1))

        grid_lay = GridLayout(cols=self.num_columns)

        for index in range(0, self.num_rows * self.num_columns):
            self.buttons.append(Button(text="", markup=True))
            grid_lay.add_widget(self.buttons[index])

        for i, button in enumerate(self.buttons):
            if i not in self.ignore:
                button.text = "[size=%s]%s[/size]" % (int(self.font), self.solve_boggle.boggle.boggle_array[i].upper())
            else:
                button.text = ""

        hor_lay.add_widget(grid_lay)

        scroll = ScrollView()

        lay = GridLayout(cols=1, spacing=20, size_hint=(1, None))
        lay.bind(minimum_height=lay.setter('height'))

        lay.add_widget(Label(text=""))

        lay.add_widget(Label(text="%s words." % len(self.words)))
        # scrollview of labels
        for word in self.words:
            lay.add_widget(Label(text=word))
            # add word label to scrollview

        lay.add_widget(Label(text=""))

        self.reset_button = Button(text="Reset", size_hint=(self.x, 0.08))
        self.reset_button.bind(on_press=self.reset_callback)

        lay.add_widget(Label(text=""))
        scroll.add_widget(lay)

        vert_lay.add_widget(scroll)
        vert_lay.add_widget(self.reset_button)
        hor_lay.add_widget(vert_lay)

        self.add_widget(hor_lay)


class MyApp(App):

    def build(self):
        wid = MenuScreen()
        print(wid)
        return wid


if __name__ == '__main__':
    MyApp().run()
