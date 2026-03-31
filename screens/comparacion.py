from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from kivy.uix.label import Label

from database import obtener_todos_jugadores, obtener_resultados_jugador

import matplotlib.pyplot as plt
from database import obtener_historial_jugador


class ComparacionScreen(Screen):

    jugadores = ListProperty([])

    def on_enter(self):

        datos = obtener_todos_jugadores()

        self.jugadores = [j[1] for j in datos]
        self.jugadores_ids = {j[1]: j[0] for j in datos}

    def comparar(self):

        j1 = self.ids.jugador1.text
        j2 = self.ids.jugador2.text

        if j1 not in self.jugadores_ids or j2 not in self.jugadores_ids:
            return

        id1 = self.jugadores_ids[j1]
        id2 = self.jugadores_ids[j2]

        datos1 = obtener_resultados_jugador(id1)
        datos2 = obtener_resultados_jugador(id2)

        contenedor = self.ids.resultado_comparacion
        contenedor.clear_widgets()

        if not datos1 or not datos2:
            contenedor.add_widget(Label(text="Faltan datos"))
            return

        texto = f"""
        {j1}
        Sprint30: {datos1[0]}
        Illinois: {datos1[1]}
        YoYo: {datos1[2]}

        ----------------------

        {j2}
        Sprint30: {datos2[0]}
        Illinois: {datos2[1]}
        YoYo: {datos2[2]}
        """

        contenedor.add_widget(
            Label(
                text=texto,
                color=(0, 0, 0, 1)
            )
        )

    def grafica_jugador(self):

        jugador = self.ids.jugador1.text

        if jugador not in self.jugadores_ids:
            return

        jugador_id = self.jugadores_ids[jugador]

        datos = obtener_historial_jugador(jugador_id)

        if not datos:
            return

        fechas = [d[0] for d in datos]
        sprint = [d[1] for d in datos]
        illinois = [d[2] for d in datos]
        yoyo = [d[3] for d in datos]

        # -------- Sprint --------
        plt.figure()
        plt.plot(fechas, sprint, marker="o")
        plt.title(f"Sprint 30m - {jugador}")
        plt.xlabel("Fecha")
        plt.ylabel("Tiempo (s)")
        plt.grid(True)

        # -------- Illinois --------
        plt.figure()
        plt.plot(fechas, illinois, marker="o")
        plt.title(f"Illinois - {jugador}")
        plt.xlabel("Fecha")
        plt.ylabel("Tiempo (s)")
        plt.grid(True)

        # -------- YoYo --------
        plt.figure()
        plt.plot(fechas, yoyo, marker="o")
        plt.title(f"YoYo Test - {jugador}")
        plt.xlabel("Fecha")
        plt.ylabel("Nivel")
        plt.grid(True)

        plt.show()