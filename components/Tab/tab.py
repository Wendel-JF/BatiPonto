from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.tab import MDTabsBase


class TabComponent(BoxLayout, MDTabsBase):
    title = StringProperty("")

    def add_widget(self, widget, index=0, canvas=None):
        if self.ids and "content_container" in self.ids:
            return self.ids.content_container.add_widget(widget)
        return super().add_widget(widget, index=index, canvas=canvas)
