from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.lang import Builder

from screens.seleccion import SeleccionScreen
from screens.pruebas import PruebasScreen
from screens.resultados import ResultadosScreen
from screens.comparacion import ComparacionScreen
from screens.gestion import GestionScreen

from database import crear_tablas

import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class WindowManager(ScreenManager):
    pass

class DatosFisicosApp(MDApp):

    def build(self):

        crear_tablas()

        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"

        Builder.load_file(resource_path("kv/seleccion.kv"))
        Builder.load_file(resource_path("kv/pruebas.kv"))
        Builder.load_file(resource_path("kv/resultados.kv"))
        Builder.load_file(resource_path("kv/comparacion.kv"))
        Builder.load_file(resource_path("kv/gestion.kv"))

        sm = WindowManager()

        sm.add_widget(SeleccionScreen(name="seleccion"))
        sm.add_widget(PruebasScreen(name="pruebas"))
        sm.add_widget(ResultadosScreen(name="resultados"))
        sm.add_widget(ComparacionScreen(name="comparacion"))
        sm.add_widget(GestionScreen(name="gestion"))

        return sm

if __name__ == "__main__":
    DatosFisicosApp().run()