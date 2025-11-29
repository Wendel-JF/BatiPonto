from kivy.properties import ListProperty, StringProperty
from kivymd.app import MDApp
from kivymd.uix.card import MDCard


class PontoCard(MDCard):
    bgcolor = ListProperty([1, 1, 1, 1]) 

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        app = MDApp.get_running_app()
        self.bgcolor = app.theme_cls.bg_dark
    
    data = StringProperty("")
    dia_semana = StringProperty("")
    p1 = StringProperty("")
    p2 = StringProperty("")
    p3 = StringProperty("")
    p4 = StringProperty("")
    
    def update_pontos(self, p1, p2, p3, p4):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4