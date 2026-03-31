from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty

from database import añadir_equipo, añadir_jugador, obtener_temporadas, obtener_equipos
from database import borrar_jugador, borrar_equipo, obtener_jugadores_equipo
from database import ( insertar_temporada )
from kivy.uix.button import Button


class GestionScreen(Screen):

    temporadas = ListProperty([])
    equipos = ListProperty([])

    def on_enter(self):

        self.recargar_temporadas()
        self.equipos_ids = {}

    def crear_equipo(self):

        nombre = self.ids.nuevo_equipo.text.strip()
        temporada = self.ids.temporada.text

        if nombre == "":
            return

        if temporada not in self.temporadas_ids:
            return

        temporada_id = self.temporadas_ids[temporada]

        añadir_equipo(nombre, temporada_id)

        self.ids.nuevo_equipo.text = ""
        self.cargar_equipos()

    def cargar_equipos(self):

        temporada = self.ids.temporada.text

        if temporada not in self.temporadas_ids:
            return

        temporada_id = self.temporadas_ids[temporada]

        datos = obtener_equipos(temporada_id)

        self.equipos = [e[1] for e in datos]
        self.equipos_ids = {e[1]: e[0] for e in datos}

        self.ids.equipo.values = self.equipos

    def crear_jugador(self):

        nombre = self.ids.nuevo_jugador.text.strip()
        equipo = self.ids.equipo.text

        if nombre == "":
            return

        if equipo not in self.equipos_ids:
            return

        equipo_id = self.equipos_ids[equipo]

        añadir_jugador(nombre, equipo_id)

        self.ids.nuevo_jugador.text = ""
        self.mostrar_jugadores()

    def mostrar_jugadores(self):

        if not hasattr(self, 'equipos_ids'):
            print("No hay equipos para mostrar")
            return

        equipo = self.ids.equipo.text

        if equipo not in self.equipos_ids:
            return

        equipo_id = self.equipos_ids[equipo]

        datos = obtener_jugadores_equipo(equipo_id)

        contenedor = self.ids.lista_jugadores
        contenedor.clear_widgets()

        for jugador in datos:
            btn = Button(
                text=f"{jugador[1]}  (Eliminar)",
                size_hint_y=None,
                height=40
            )

            btn.bind(on_press=lambda x, jid=jugador[0]: self.eliminar_jugador(jid))

            contenedor.add_widget(btn)

    def eliminar_jugador(self, jugador_id):

        borrar_jugador(jugador_id)

        self.mostrar_jugadores()

    def eliminar_equipo(self):

        equipo = self.ids.equipo.text

        if equipo not in self.equipos_ids:
            return

        equipo_id = self.equipos_ids[equipo]

        borrar_equipo(equipo_id)

        self.cargar_equipos()

    def crear_temporada(self):

        nombre = self.ids.nueva_temporada.text.strip()

        if nombre == "":
            print("Escribe una temporada")
            return

        try:
            insertar_temporada(nombre)
        except:
            print("La temporada ya existe")
            return

        self.ids.nueva_temporada.text = ""
        self.recargar_temporadas()

    def recargar_temporadas(self):
        datos = obtener_temporadas()

        self.temporadas = [t[1] for t in datos]
        self.temporadas_ids = {t[1]: t[0] for t in datos}

        self.ids.temporada.values = self.temporadas