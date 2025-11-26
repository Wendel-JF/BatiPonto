from kivy.config import Config
from kivy.graphics.fbo import Fbo

Config.set('graphics', 'multisamples', '0')  # Desativa anti-aliasing que usa FBO

Config.set('graphics', 'show_fps', '1')
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '800')
Config.set('kivy', 'log_level', 'debug')  # ou 'trace' para ainda mais detalhes
Config.set('kivy', 'log_enable', 1)

import locale

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ColorProperty, ObjectProperty, StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import NoTransition
from kivy.utils import get_color_from_hex
from kivymd.app import MDApp
from kivymd.color_definitions import colors
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.tab import MDTabsBase

from database.ponto_db import create_pontos_table
from database.users_db import create_users_table
#from components.ExpansionPanel.expansion_panel import ExpansionPanelComponent
from fonts.fonts_config import register_fonts
from screens.Home.home_screen import HomeScreen
from screens.Login.login_screen import LoginScreen
from screens.Login.register_screen import RegisterScreen
from screens.Splash.splash_screen import SplashScreen


class ContentPanel(BoxLayout):
    pass


class HistoricScreen(MDScreen): pass


class TabComponent(BoxLayout, MDTabsBase):
    pass

class Tab(BoxLayout, MDTabsBase):
    title = StringProperty("")   # ← OBRIGATÓRIO!
    icon = StringProperty("")    # ← OBRIGATÓRIO para evitar o erro
    

class SettingsScreen(MDScreen): pass
class ProfileScreen(MDScreen): pass

class MeuApp(MDApp):
    user = None   # Guarda o usuário logado
    is_logged = False  # Guarda o estado de sessão
    # Define o tipo de fonte do app configurar no arquivo fonts/fonts_config.py
    font_name = "Roboto"
    # Define uma cor padrão ANTES do KV ser carregado
    text_color = ColorProperty([1, 1, 1, 1]) # começa com branco

    # Colors "BlueGray" "Pink" "Purple" "DeepPurple" "Indigo" "Blue" "LightBlue" "Cyan" "Teal" "Green" "LightGreen" "Lime" "Yellow" "Amber" "Orange" "DeepOrange" "Brown" "Gray"
    primary_theme_color = "Indigo"
    secondary_theme_color = "BlueGray"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):

        try:
            locale.setlocale(locale.LC_TIME, "pt_BR.utf8")
        except locale.Error:
            try:
                locale.setlocale(locale.LC_TIME, "pt_BR")
            except locale.Error:
                pass
        
        register_fonts()  # Inserir as fontes
        # Criar tabela no banco de dados
        create_users_table() 
        create_pontos_table()

        # Carregar layout principal com a navbar
        root = Builder.load_file("layout.kv")
        
        # Carrega arquivos KV das telas
        for kv_file in [
            "screens/Splash/splash.kv",
            "screens/Home/home.kv",
            "screens/Login/login.kv",
            "screens/Login/register.kv",
            "screens/Historics/historics.kv",
            "screens/settings.kv",
            "screens/profile.kv"
        ]:
            Builder.load_file(kv_file)


        # Criar o gerenciador de telas
        self.sm = MDScreenManager(size_hint=(1, 1), transition=NoTransition())

        #Clock.schedule_once(lambda dt: root.ids.screen_container.add_widget(self.sm))

        # Adicionar as telas
        self.sm.add_widget(SplashScreen(name="splash"))
        self.sm.add_widget(HomeScreen(name="home"))
        self.sm.add_widget(LoginScreen(name="login"))
        self.sm.add_widget(RegisterScreen(name="register"))
        self.sm.add_widget(HistoricScreen(name="historic"))
        self.sm.add_widget(SettingsScreen(name="settings"))
        self.sm.add_widget(ProfileScreen(name="profile"))


        # Define tela inicial
        Clock.schedule_once(lambda dt: setattr(self.sm, 'current', 'login'), 0)

        # Garante que o menu comece invisível
        Clock.schedule_once(lambda dt: self.hide_menu(), 0)

        # Injetar o screenmanager dentro do layout
        Clock.schedule_once(lambda dt: root.ids.screen_container.add_widget(self.sm))
       
        Clock.schedule_once(lambda dt: self.switch_theme_style(), 0.2)
        return root

    def on_switch_tabs(self, screen_name):
        if hasattr(self, "sm"):
            self.sm.current = screen_name
            print(f"🔄 Trocando para a tela: {screen_name}")
        else:
            print("⚠️ ScreenManager ainda não inicializado.")

    def hide_menu(self):
        nav = self.root.ids.nav_container
        nav.opacity = 0
        nav.disabled = True

    # Funcao para troca de tema
    def switch_theme_style(self):
       
        # alterna tema claro / escuro
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"
       
    # muda a paleta de acordo com o tema
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.primary_palette = self.primary_theme_color   # azul claro
            self.theme_cls.primary_hue = "800" # mais escuro
            self.theme_cls.accent_palette = self.secondary_theme_color

            # texto escuro para o modo claro
            self.text_color = get_color_from_hex(colors["Gray"]["900"])
        else:
            self.theme_cls.primary_palette = self.primary_theme_color # azul escuro
            self.theme_cls.primary_hue = "800"   # mais claro
            self.theme_cls.accent_palette = self.secondary_theme_color
            self.theme_cls.accent_hue = "600"

            # texto claro para o modo escuro
            self.text_color = get_color_from_hex(colors["Gray"]["50"])
          
        self.apply_navbar_theme()

    def apply_navbar_theme(self):
        """Atualiza as cores da NavBar dinamicamente."""
        try:
            bottom_nav = self.root.ids.bottom_nav
        except KeyError:
            print("⚠ bottom_nav ainda não está disponível.")
            return  

        theme = self.theme_cls

        if theme.theme_style == "Light":
            normal_color = theme.bg_dark
        else:
            normal_color = theme.opposite_bg_dark

        active_color = theme.primary_color

        # Define a cor do painel (se existir)
        if hasattr(bottom_nav, "panel_color"):
            bottom_nav.panel_color = theme.bg_dark
        try:
            container = bottom_nav.children[0]          # BoxLayout interno
            items = container.children                  # Tabs
        except Exception as e:
            print("Erro ao acessar itens da navbar:", e)
            return

        for item in items:
            if hasattr(item, "text_color_normal"):
                item.text_color_normal = normal_color

            if hasattr(item, "text_color_active"):
                item.text_color_active = active_color

    def login(self, user_object):
        self.user = user_object
        self.is_logged = True

    def logout(self):
        print("Saindo...")

        # remover dados de sessão
        self.user = None
        self.is_logged = False

        # Voltar para a tela de login
        self.hide_menu()
        self.on_switch_tabs('login') 

if __name__ == '__main__':
    MeuApp().run()