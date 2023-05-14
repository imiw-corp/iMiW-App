from kivy.graphics import Color, Rectangle
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.image import Image
from kivy.app import App
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.lang import Builder
import webbrowser
import requests
import json


# Animated logo and preparation (Only one time)
class WelcomeMenu(Screen):
    def __init__(self, **kwargs):
        super(WelcomeMenu, self).__init__(**kwargs)

        self.add_widget(Image(size_hint=(None, None),
                              size=(Window.width*0.4, Window.width*0.4),
                              pos_hint={'center_x': 0.5, 'center_y': 0.5},
                              source='img/Logo_white.png'))

        Clock.schedule_once(self.change_screen, 1.5)

    def change_screen(self, *args):
        # try to make a GET request
        try:
            check = requests.get('http://google.com/', timeout=5)
            self.manager.current = "MainMenu"
        except:
            self.manager.current = "NoInternet"


class NoInternet(Screen):
    def __init__(self, **kwargs):
        super(NoInternet, self).__init__(**kwargs)

        self.add_widget(Label(text="No internet",
                              font_size='32sp',
                              size_hint=(0.5, 0.2),
                              pos_hint={'center_x': 0.5, 'center_y': 0.7}))

        self.add_widget(Button(text="Repeat",
                               on_press=self.change_screen,
                               size_hint=(0.5, 0.2),
                               pos_hint={'center_x': 0.5, 'center_y': 0.3}))

    def change_screen(self, *args):
        # try to make a GET request
        try:
            check = requests.get('http://google.com/', timeout=5)
            self.manager.current = "MainMenu"
        except:
            pass


# Main menu (Scroll) with events
class MainMenu(Screen):
    def __init__(self, **kwargs):
        super(MainMenu, self).__init__(**kwargs)
        self.canvas.before.add(Color(1, 1, 1, 1))
        self.canvas.before.add(Rectangle(size=(Window.width, Window.height)))

        layout = FloatLayout()

        grid = GridLayout(cols=1,
                          spacing=30,
                          padding=30,
                          size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        # Parse JSON data
        url = 'https://raw.githubusercontent.com/imiw-corp/iMiW-App/main/news.json'
        response = requests.get(url)
        fcc_data = json.loads(response.text)

        # Generate block with count of news
        for news in reversed(fcc_data['news']):
            btn = Button(text=news['title'] + '\n\n' + news['date'],
                         halign='center',
                         valign='center',
                         font_size='24sp',
                         size_hint=(None, None),
                         size=(Window.width-60, Window.width-60),
                         background_color=[120/255, 120/255, 120/255, 1],
                         on_press=lambda x: webbrowser.open(news['url']))
            grid.add_widget(btn)

        root = ScrollView(size_hint=(None, None), size=(Window.width, Window.height))
        root.add_widget(grid)
        layout.add_widget(root)

        button = Button(size_hint=(None, None),
                        pos_hint={'center_x': 0.5, 'y': 0.02},
                        on_press=self.change_screen,
                        background_normal='img/1.png',
                        background_down='img/1.png',
                        border=[0, 0, 0, 0])

        layout.add_widget(button)

        self.add_widget(layout)

    def change_screen(self, *args):
        self.manager.current = "PersonalMenu"


# Personal information
class PersonalMenu(Screen):
    def __init__(self, **kwargs):
        super(PersonalMenu, self).__init__(**kwargs)

        box_personal = Builder.load_file('kv_menu/personal.kv')

        self.add_widget(box_personal)
        self.add_widget(Button(size_hint=(None, None),
                               pos_hint={'center_x': 0.5, 'y': 0.02},
                               on_press=self.change_screen,
                               background_normal='img/2.png',
                               background_down='img/2.png',
                               border=[0, 0, 0, 0]))

    def change_screen(self, *args):
        self.manager.current = "MainMenu"


class iMiW_App(App):
    def build(self):
        Window.size = (400, 800)

        screen_manager = ScreenManager(transition=FadeTransition())
        screen_1 = WelcomeMenu(name="WelcomeMenu")
        screen_2 = MainMenu(name="MainMenu")
        screen_3 = PersonalMenu(name="PersonalMenu")
        screen_4 = NoInternet(name="NoInternet")
        screen_manager.add_widget(screen_1)
        screen_manager.add_widget(screen_2)
        screen_manager.add_widget(screen_3)
        screen_manager.add_widget(screen_4)

        return screen_manager


if __name__ == '__main__':
    iMiW_App().run()
