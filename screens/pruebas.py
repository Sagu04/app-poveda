from kivy.uix.screenmanager import Screen
from database import guardar_prueba

from kivymd.uix.pickers import MDDatePicker
import datetime


class PruebasScreen(Screen):

    def guardar_datos(self):

        fecha = self.ids.fecha.text
        sprint30 = self.ids.sprint30.text
        illinois = self.ids.illinois.text
        yoyo = self.ids.yoyo.text

        jugador_id = self.manager.get_screen("seleccion").jugador_id

        if jugador_id is None:
            print("Selecciona un jugador primero")
            return

        guardar_prueba(
            jugador_id,
            fecha,
            sprint30,
            illinois,
            yoyo
        )

        print("Datos guardados")

    def abrir_calendario(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.guardar_fecha)
        date_dialog.open()

    def guardar_fecha(self, instance, value, date_range):
        self.ids.fecha.text = str(value)