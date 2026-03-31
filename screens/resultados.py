from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from database import obtener_resultados_filtrados
from kivy.graphics import Color, Rectangle


class ResultadosScreen(Screen):

    def on_enter(self):
        self.cargar_resultados()

    def cargar_resultados(self):

        datos = obtener_resultados_filtrados()

        tabla = self.ids.tabla_resultados
        tabla.clear_widgets()

        # cabecera
        cabecera = ["Jugador", "Fecha", "Sprint 30m", "Illinois", "YoYo"]

        for c in cabecera:
            tabla.add_widget(Label(text=c, color=(0, 0, 0, 1), size_hint_y=None, height=40))

        equipo_actual = None

        for r in datos:

            equipo = r[0]
            jugador = r[1]
            fecha = r[2]
            sprint = r[3]
            illinois = r[4]
            yoyo = r[5]

            # si cambia el equipo
            if equipo != equipo_actual:
                tabla.add_widget(Label(text="", size_hint_y=None, height=30))
                tabla.add_widget(
                    Label(text=f"[b]{equipo}[/b]", markup=True, color=(0, 0, 0, 1), size_hint_y=None, height=30))
                tabla.add_widget(Label(text="", size_hint_y=None, height=30))
                tabla.add_widget(Label(text="", size_hint_y=None, height=30))
                tabla.add_widget(Label(text="", size_hint_y=None, height=30))

                equipo_actual = equipo

            fila = [jugador, fecha, sprint, illinois, yoyo]

            for valor in fila:
                tabla.add_widget(Label(text=str(valor), color=(0, 0, 0, 1), size_hint_y=None, height=40))

    def crear_cabecera(self, tabla):

        cabecera = ["Jugador", "Fecha", "Sprint 30m", "Illinois", "YoYo"]

        for texto in cabecera:
            label = Label(
                text=texto,
                color=(0, 0, 0, 1),
                bold=True
            )

            tabla.add_widget(label)