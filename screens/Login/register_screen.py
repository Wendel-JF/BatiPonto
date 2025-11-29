from kivy.clock import Clock
from kivymd.toast import toast
from kivymd.uix.screen import MDScreen

from database.users_db import registrar_usuario


class RegisterScreen(MDScreen):

    def do_register(self):
        name = self.ids.name.text.strip()
        email = self.ids.email.text.strip()
        password = self.ids.password.text.strip()

        if not name or not email or not password:
            toast("Preencha todos os campos")
            return

        # cadastrar o usuário
        registrar_usuario(name, email, password)

        self.clear_inputs()

        # Volta para a tela de login
        Clock.schedule_once(lambda dt: setattr(self.manager, "current", "login"), 0.1)

    def clear_inputs(self):
        self.ids.name.text = ""
        self.ids.email.text = ""
        self.ids.password.text = ""

    def go_login(self):
        self.manager.current = "login"
