from kivymd.uix.card import MDCard
from kivy.properties import StringProperty

class HistoricoCard(MDCard):
    data_text = StringProperty()
    entrada = StringProperty()
    saida = StringProperty()
    horas = StringProperty()
    status = StringProperty()