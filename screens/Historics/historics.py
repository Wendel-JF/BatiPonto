from kivy.animation import Animation
from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.screen import MDScreen

from database.ponto_db import buscar_ontem, buscar_pontos_mes, buscar_semana
from screens.Historics.historic_card import HistoricoCard


class HistoricScreen(MDScreen):
    def on_enter(self):
        self.carregar_mes("2025", "11")
        self.carregar_ontem()
        self.carregar_semana()

    def carregar_ontem(self):
        self.ids.yesterday_content.clear_widgets()

        dados = buscar_ontem()

        if not dados:
            return

        for dia, dia_semana, entrada, intervalo, retorno, saida in dados:
            card = HistoricoCard(
                data_text=f"{dia} - {dia_semana}",
                entrada=entrada,
                saida=saida,
                horas=self.calcular_horas(entrada, saida),
                status="Ponto Confirmado"
            )
            self.ids.yesterday_content.add_widget(card)

    def carregar_semana(self):
        self.ids.week_content.clear_widgets()

        dados = buscar_semana()

        if not dados:
            return

        for _id, user_id, dia, dia_semana, entrada, intervalo, retorno, saida in dados:
            card = HistoricoCard(
                data_text=f"{dia} - {dia_semana}",
                entrada=entrada,
                saida=saida,
                horas=self.calcular_horas(entrada, saida),
                status="Ponto Confirmado"
            )
            self.ids.week_content.add_widget(card)

    def carregar_mes(self, ano, mes):
            dados = buscar_pontos_mes(ano, mes)
            
            container = self.ids.month_content
            container.clear_widgets()

            for item in dados:

                _id, user_id, dia, dia_semana, entrada, intervalo, retorno, saida = item

                card = HistoricoCard(
                    data_text=f"{dia} - {dia_semana}",
                    entrada=entrada,
                    saida=saida,
                    horas=self.calcular_horas(entrada, saida),
                    status="Ponto Confirmado"
                )

                container.add_widget(card)

    def calcular_horas(self, entrada, saida):
        from datetime import datetime

        e = datetime.strptime(entrada, "%H:%M")
        s = datetime.strptime(saida, "%H:%M")

        diff = s - e
        horas = round(diff.total_seconds() / 3600)
        return f"{horas}h"