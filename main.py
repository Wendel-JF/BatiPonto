
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.bottomnavigation import (MDBottomNavigation,
                                         MDBottomNavigationItem)


class MeuApp(MDApp):
    def build(self):
        # Carrega o KV externo
        screen = Builder.load_file("layout.kv")

        # Configurações do tema
        self.theme_cls.theme_style_switch_animation = True
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        # pode ser "200", "500", "700", "A100" etc.
        self.theme_cls.primary_hue = "900"

        return screen

    # Funcao para troca de tela
    def on_switch_tabs(self, bar, item, item_icon, item_text):
        # Troca a tela do MDScreenManager pelo nome
        self.root.ids.screen_manager.current = item_text

    # Funcao para troca de tema
    def switch_theme_style(self):
        # alterna tema claro / escuro
        self.theme_cls.theme_style = "Dark" if self.theme_cls.theme_style == "Light" else "Light"

    # muda a paleta de acordo com o tema
        if self.theme_cls.theme_style == "Light":
            self.theme_cls.primary_palette = "LightBlue"   # azul claro
        else:
            self.theme_cls.primary_palette = "Blue"        # azul escuro


if __name__ == '__main__':
    MeuApp().run()
