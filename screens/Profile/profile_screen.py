from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

from database.users_db import get_user_data 


class ProfileScreen(MDScreen):

    def on_pre_enter(self):
        app = MDApp.get_running_app()

        dados = get_user_data(app.user_id)
        if dados:
            name, email = dados

            self.ids.profile_name.text = name
            self.ids.profile_email.text = email