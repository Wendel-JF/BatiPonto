
import locale
from datetime import datetime, timedelta

from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.factory import Factory
from kivy.properties import ListProperty, StringProperty
from kivymd.toast import toast
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

from database.ponto_db import listar_pontos, verificar_ponto_no_dia
from screens.Home.ponto_card import PontoCard

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')


class HomeScreen(MDScreen):
    registros_do_dia = ListProperty([])  
    data_atual = StringProperty("")

    def on_pre_enter(self):
        self.ids.registro_container.clear_widgets()

        self.carregar_pontos()
        #Clock.schedule_interval(self.carregar_pontos, 20)

        self.atualizar_data_de_hoje()
        Clock.schedule_interval(self.atualizar_data_de_hoje, 30)

        self.calcular_horas_trabalhadas()
        Clock.schedule_interval(self.calcular_horas_trabalhadas, 60)

    def registrar_click(self):
        agora = datetime.now()

        data_str = agora.strftime("%d/%m/%Y")
        hora_str = agora.strftime("%H:%M")
        dia_semana = dia_semana_ptbr(agora)

        # ------------------------------------------------------------------
        # 1) SE A DATA MUDAR → cria novo card e zera registros
        # ------------------------------------------------------------------
        if self.data_atual != data_str:
           
            if verificar_ponto_no_dia(data_str):
                toast(f"Já existe registro de ponto para {data_str}")
                self.data_atual = data_str
                self.registros_do_dia = []
                return
        
                # --- RESETAR HORAS ---
            if "lbl_total_horas" in self.ids:
                self.ids.lbl_total_horas.text = "0.00 h"

            if "lbl_porcentagem" in self.ids:
                self.ids.lbl_porcentagem.text = "0%"
        
            self.data_atual = data_str         # atualiza data
            self.registros_do_dia = []  
                   # zera registros do dia

            # cria card vazio para a nova data
            novo_card = PontoCard(
                data=data_str,
                dia_semana=dia_semana,
                p1="",
                p2="",
                p3="",
                p4="",
            )

            # adiciona esse card no container
            self.ids.registro_container.add_widget(novo_card, index=0)

        if verificar_ponto_no_dia(data_str):
            toast(f"Já existe registro de ponto para {data_str}")
            self.data_atual = data_str
            self.registros_do_dia = []
            return
        
        # ------------------------------------------------------------------
        # 2) Registra o horário do clique
        # ------------------------------------------------------------------
        self.registros_do_dia.append(hora_str)

        # impede mais de 4 pontos
        if len(self.registros_do_dia) > 4:
            return

        # preenche p1–p4 dinamicamente
        horarios = self.registros_do_dia
        p1 = horarios[0] if len(horarios) > 0 else ""
        p2 = horarios[1] if len(horarios) > 1 else ""
        p3 = horarios[2] if len(horarios) > 2 else ""
        p4 = horarios[3] if len(horarios) > 3 else ""

        # ------------------------------------------------------------------
        # Atualiza o ÚLTIMO card criado (que é o da data atual)
        # ------------------------------------------------------------------
        ultimo_card = self.ids.registro_container.children[0]
        ultimo_card.update_pontos(p1, p2, p3, p4)

        # Atualiza também os cards da barra superior
        if "lbl_p1" in self.ids:
            self.ids.lbl_p1.text = p1
        if "lbl_p2" in self.ids:
            self.ids.lbl_p2.text = p2
        if "lbl_p3" in self.ids:
            self.ids.lbl_p3.text = p3
        if "lbl_p4" in self.ids:
            self.ids.lbl_p4.text = p4

        # ------------------------------------------------------------------
        #  Salvar no banco de dados QUANDO HOUVER OS 4 PONTOS
        # ------------------------------------------------------------------
        if len(self.registros_do_dia) == 4:
            from database.ponto_db import inserir_ponto

            app = App.get_running_app()
            id_user = app.user["id"]  # ou app.user.id dependendo do formato
            
            inserir_ponto(
                id_user,
                self.data_atual,   # dia
                dia_semana,        # dia da semana
                p1,                # entrada
                p2,                # intervalo
                p3,                # retorno
                p4                 # saída
            )

        # Mostrar mensagem com barra por 10 segundos
        self.mostrar_mensagem_sucesso()

    def mostrar_mensagem_sucesso(self):
        box = self.ids.msg_sucesso
        barra = self.ids.barra_progresso

        # anima para aparecer
        Animation(height=60, opacity=1, d=0.3).start(box)

        # zera barra
        barra.value = 0

        # animação da barra (10 segundos)
        Animation(value=100, d=10).start(barra)

        # depois de 10s, esconder
        Clock.schedule_once(lambda dt: self.esconder_mensagem_sucesso(), 10)

    def esconder_mensagem_sucesso(self):
        box = self.ids.msg_sucesso
        barra = self.ids.barra_progresso

        # anima para desaparecer
        anim = Animation(height=0, opacity=0, d=0.3)
        anim.bind(on_complete=lambda *x: setattr(barra, "value", 0))
        anim.start(box)

    def atualizar_data_de_hoje(self, dt=None):
        agora = datetime.now()

        # Dicionários para traduzir quando vier em inglês
        dias_en = {
            "Monday": "segundaa",
            "Tuesday": "terça",
            "Wednesday": "quarta",
            "Thursday": "quinta",
            "Friday": "sexta",
            "Saturday": "sábado",
            "Sunday": "domingo"
        }

        meses_en = {
            "January": "janeiro",
            "February": "fevereiro",
            "March": "março",
            "April": "abril",
            "May": "maio",
            "June": "junho",
            "July": "julho",
            "August": "agosto",
            "September": "setembro",
            "October": "outubro",
            "November": "novembro",
            "December": "dezembro"
        }

        # Capturar o que o SO está retornando
        dia_raw = agora.strftime("%A")
        mes_raw = agora.strftime("%B")

        try:
            dia_raw_corrigido = dia_raw.encode("latin1").decode("utf-8")
        except:
            dia_raw_corrigido = dia_raw

        try:
            mes_raw_corrigido = mes_raw.encode("latin1").decode("utf-8")
        except:
            mes_raw_corrigido = mes_raw

        # Se vier em inglês → traduz
        dia_semana = dias_en.get(dia_raw_corrigido, dia_raw_corrigido)
        mes = meses_en.get(mes_raw_corrigido, mes_raw_corrigido)

        # Montar string final
        data_formatada = f"{dia_semana}, {agora.day:02d} de {mes} de {agora.year}"

        # Primeira letra maiúscula
        data_formatada = data_formatada[0].upper() + data_formatada[1:]

        self.ids.lbl_date.text = data_formatada

    def carregar_pontos(self, dt=None):
        registros = listar_pontos()   # pega do banco

        if not registros:
            return


         # LIMPA os cards antes de adicionar de novo
        self.ids.registro_container.clear_widgets()
        

        for reg in registros:
            # registro = (id, id_user, dia, dia_semana, p1, p2, p3, p4)
            _, _, dia, dia_semana, p1, p2, p3, p4 = reg

            # cria card de histórico
            card = PontoCard(
                data=dia,
                dia_semana=dia_semana,
                p1=p1,
                p2=p2,
                p3=p3,
                p4=p4
            )

            # adiciona no container
            self.ids.registro_container.add_widget(card)

        # ----------------------------------------------------------------------
        # Atualizar os horários da barra superior com o último registro do banco
        # ----------------------------------------------------------------------
        ultimo = registros[0]
        _, _, dia, dia_semana, entrada, intervalo, retorno, saida = ultimo

        # Data atual (AAAA-MM-DD ou outro formato, depende do banco)
        data_hoje = datetime.now().strftime("%d/%m/%Y")

        # Se o formato da data do banco estiver diferente, me diga para ajustar

        if dia == data_hoje:
            # Atualiza com os valores do banco
            if self.ids.get("lbl_p1"): self.ids.lbl_p1.text = entrada
            if self.ids.get("lbl_p2"): self.ids.lbl_p2.text = intervalo
            if self.ids.get("lbl_p3"): self.ids.lbl_p3.text = retorno
            if self.ids.get("lbl_p4"): self.ids.lbl_p4.text = saida
        else:
            # Deixa todos vazios
            if self.ids.get("lbl_p1"): self.ids.lbl_p1.text = "8:00"
            if self.ids.get("lbl_p2"): self.ids.lbl_p2.text = "12:00"
            if self.ids.get("lbl_p3"): self.ids.lbl_p3.text = "13:00"
            if self.ids.get("lbl_p4"): self.ids.lbl_p4.text = "15:00"

    def calcular_horas_trabalhadas(self, dt=None):
        try:
            formato = "%H:%M"

            # captura os horários
            entrada = self.ids.lbl_p1.text.strip()
            intervalo = self.ids.lbl_p2.text.strip()
            retorno = self.ids.lbl_p3.text.strip()
            saida = self.ids.lbl_p4.text.strip()

            # carga horária padrão
            inicio_padrao = datetime.strptime("08:00", formato)
            fim_padrao = datetime.strptime("15:00", formato)
            carga_total_horas = (fim_padrao - inicio_padrao).total_seconds() / 3600

            # ------------------------------------------
            # CASOS (PARA PARAR / CONTINUAR O CÁLCULO)
            # ------------------------------------------

            # Sem entrada → nada pra calcular
            if not entrada:
                self.ids.lbl_total_horas.text = "0 h"
                self.ids.lbl_porcentagem.text = "0%"
                return

            t_entrada = datetime.strptime(entrada, formato)

            # ❌ Sem intervalo → ainda está trabalhando desde a entrada
            if not intervalo:
                agora = datetime.now()
                tempo = agora.replace(year=1900, month=1, day=1) - t_entrada
                horas = tempo.total_seconds() / 3600
            else:
                t_intervalo = datetime.strptime(intervalo, formato)

                # → Trabalhou até o intervalo
                tempo_antes_intervalo = t_intervalo - t_entrada

                # ❌ Tem intervalo mas não tem retorno → está NO INTERVALO → PAUSAR cálculo
                if not retorno:
                    horas = tempo_antes_intervalo.total_seconds() / 3600
                else:
                    t_retorno = datetime.strptime(retorno, formato)

                    # ❌ Tem retorno mas não tem saída → está TRABALHANDO
                    if not saida:
                        agora = datetime.now()
                        agora = agora.replace(year=1900, month=1, day=1)

                        tempo_depois_intervalo = agora - t_retorno
                    else:
                        # ✔ Com saída → cálculo FECHADO
                        t_saida = datetime.strptime(saida, formato)
                        tempo_depois_intervalo = t_saida - t_retorno

                    horas = (tempo_antes_intervalo + tempo_depois_intervalo).total_seconds() / 3600

            # ------------------------------------------
            # Calcula porcentagem
            # ------------------------------------------
            porcentagem = (horas / carga_total_horas) * 100
            if porcentagem < 0:
                porcentagem = 0
            if porcentagem > 100:
                porcentagem = 100

            # ------------------------------------------
            # Atualiza telas
            # ------------------------------------------
            self.ids.lbl_total_horas.text = f"{horas:.2f} h"
            self.ids.lbl_porcentagem.text = f"{porcentagem:.1f}%"

        except Exception as e:
            print("Erro ao calcular:", e)


def dia_semana_ptbr(data=None):
        dias = [
            "segunda-feira",
            "terça-feira",
            "quarta-feira",
            "quinta-feira",
            "sexta-feira",
            "sábado",
            "domingo",
        ]

        if data is None:
            data = datetime.now()

        # weekday(): segunda = 0 ... domingo = 6
        return dias[data.weekday()]