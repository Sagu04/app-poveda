from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty

from database import obtener_temporadas, obtener_equipos, obtener_jugadores


class SeleccionScreen(Screen):

    temporadas = ListProperty([])
    equipos = ListProperty([])
    jugadores = ListProperty([])

    temporada_id = None
    equipo_id = None
    jugador_id = None

    def on_enter(self):

        datos = obtener_temporadas()

        self.temporadas = [t[1] for t in datos]
        self.temporadas_ids = {t[1]: t[0] for t in datos}

    def seleccionar_temporada(self, nombre):

        if nombre not in self.temporadas_ids:
            return

        self.temporada_id = self.temporadas_ids[nombre]

        equipos = obtener_equipos(self.temporada_id)

        self.equipos = [e[1] for e in equipos]
        self.equipos_ids = {e[1]: e[0] for e in equipos}

        self.jugadores = []

    def seleccionar_equipo(self, nombre):

        if nombre not in self.equipos_ids:
            return

        self.equipo_id = self.equipos_ids[nombre]

        jugadores = obtener_jugadores(self.equipo_id)

        self.jugadores = [j[1] for j in jugadores]
        self.jugadores_ids = {j[1]: j[0] for j in jugadores}

    def seleccionar_jugador(self, nombre):

        if nombre not in self.jugadores_ids:
            return

        self.jugador_id = self.jugadores_ids[nombre]