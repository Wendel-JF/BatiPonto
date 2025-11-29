from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivymd.uix.screen import MDScreen


class SplashScreen(MDScreen):
    def on_enter(self):
        Clock.schedule_once(self.go_login, 6)  
        self.start_animation()
        
    def start_animation(self):
        icon = self.ids.splash_icon
        text = self.ids.splash_text
        container = self.ids.anim_container

        final_icon_size = dp(40)
        final_text_size = dp(30)

        container.opacity = 0

      
        Animation(font_size=final_icon_size, d=4, t='in_out_sine').start(icon)
        Animation(font_size=final_text_size, d=4, t='in_out_sine').start(text)
        Animation(opacity=1, d=4).start(container)
    
    def go_login(self, *args):
        self.manager.current = "login"

    
