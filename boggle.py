from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import logging


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

        self.buttons = []
        self.ignore = []

        self.render_menu_screen()

    def cancel_callback(self, widget=None):
        logging.info("Menu Screen cancel callback.")
        exit()
        return

    def confirm_callback(self, widget=None):
        logging.info("Menu Screen confirm callback.")
        self.num_columns = int(self.num_columns_input.text)
        self.num_rows = int(self.num_rows_input.text)
        self.render_boggle_setup_screen()

    def button_configuration_callback(self, widget=None):
        if widget:
            obj = widget
        else:
            obj = self
        if obj.text == "enabled":
            obj.text = "disabled"
        else:
            obj.text = "enabled"

    def confirm_game_button(self, widget=None):
        for i, button in enumerate(self.buttons):
            if button.text != "enabled":
                self.ignore.append(i)
        print(self.ignore)
        # clear the buttons so the new ones can be added.
        self.buttons = []
        self.render_boggle_game_screen()

    def render_menu_screen(self):
        logging.info("Rendering Menu Screen.")
        self.clear_widgets()
        self.cols = 2
        self.add_widget(Label(text='Rows'))
        self.num_rows_input = TextInput()
        self.add_widget(self.num_rows_input)
        self.add_widget(Label(text='Columns'))
        self.num_columns_input = TextInput()
        self.add_widget(self.num_columns_input)
        self.cancel_button = Button(text="Cancel Boggle")
        self.cancel_button.bind(on_press=self.cancel_callback)
        self.add_widget(self.cancel_button)
        self.confirm_button = Button(text="Confirm Inputs")
        self.confirm_button.bind(on_press=self.confirm_callback)
        self.add_widget(self.confirm_button)

    def render_boggle_setup_screen(self):
        logging.info("Rendering Boggle Setup Screen.")

        self.clear_widgets()
        self.render_boggle_layout("enabled", self.button_configuration_callback)
        self.confirm_board_button = Button(text="Confirm Board")
        self.confirm_board_button.bind(on_press=self.confirm_game_button)
        self.add_widget(self.confirm_board_button)

    def render_boggle_game_screen(self):
        logging.info("Rendering game screen.")

        self.clear_widgets()

        def handle_swipe_callback(self):
            # TODO: add in swipes or keyboard for user to input words.
            pass

        self.render_boggle_layout("a", handle_swipe_callback)

    def render_boggle_layout(self, text, callback):
        logging.info("Rendering Boggle Layout.")

        self.cols = self.num_columns
        
        for index in range(0, self.num_rows * self.num_columns):
            self.buttons.append(Button(text=text))
            self.buttons[index].bind(on_press=callback)
            self.add_widget(self.buttons[index])


class MyApp(App):

    def build(self):
        wid = MenuScreen()
        print(wid)
        return wid


if __name__ == '__main__':
    MyApp().run()