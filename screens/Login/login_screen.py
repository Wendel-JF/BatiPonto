from kivy.clock import Clock
from kivymd.app import MDApp
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen

from database.users_db import verify_user


class LoginScreen(MDScreen):
    def do_login(self):
        email = self.ids.email.text
        password = self.ids.password.text

        user = verify_user(email, password)

        if user:
            toast("Login realizado!")
            self.clear_inputs()

            app = MDApp.get_running_app()
            app.login(user)  # <--- GUARDA A SESSÃO

            # Trocar de tela
            self.manager.current = "home"

            # Mostrar menu após 0.1s
            Clock.schedule_once(self.show_menu, 0.1)

        else:
            toast("Email ou senha incorretos")

    def clear_inputs(self):
        self.ids.email.text = ""
        self.ids.password.text = ""

    def go_register(self):
        self.manager.current = "register"

    def show_menu(self, dt):
        app = MDApp.get_running_app()
        nav = app.root.ids.nav_container  
        nav.opacity = 1
        nav.disabled = False
        app.theme_cls.theme_style = "Light"
        app.switch_theme_style()
