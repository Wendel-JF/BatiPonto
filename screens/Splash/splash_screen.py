from kivymd.uix.screen import MDScreen
from kivy.clock import Clock

class SplashScreen(MDScreen):
    def on_enter(self):
        Clock.schedule_once(self.go_login, 2)  # 2 segundos de splash

    def go_login(self, *args):
        self.manager.current = "login"
