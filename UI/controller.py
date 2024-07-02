import flet as ft

class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

        self._listYear = []
        self._listCountry = []

    def fillDDcountry(self):
        countries = self._model.getCountries()
        for country in countries:
            self._view.ddcountry.options.append(ft.dropdown.Option(country))


    def handle_graph(self, e):
        self._view.txt_result.controls.clear()

        self._year = self._view.ddyear.value
        self._country = self._view.ddcountry.value

        if self._year is None or self._country is None:
            self._view.txt_result.controls.append(ft.Text("Inserire un anno e una nazione"))
            self._view.update_page()
            return
        else:
            print("Scelta:", self._year, self._country)
            self._model.buildGraph(self._year, self._country)
            self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato"))
            nodes, edges = self._model.getDettagliGraph()
            self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {nodes} nodi e {edges} archi"))
            self._view.btn_volume.disabled = False
            self._view.txtN.disabled = False
            self._view.btn_path.disabled = False

        self._view.update_page()

    def handle_volume(self, e):
        retailers = self._model.getVolumi()
        for r in retailers:
            self._view.txtOut2.controls.append(ft.Text(f"{r[0]} --> {r[1]}"))

        self._view.update_page()

    def handle_path(self, e):
        lenght = self._view.txtN.value

        try:
            self._lenght = int(lenght)
        except ValueError:
            self._view.txtOut3.controls.append(ft.Text("Inserire un numero intero della lunghezza"))
            return

        if self._lenght<2:
            self._view.txtOut3.controls.append(ft.Text("Inserire una lunghezza di almeno 2"))
            return

        path = self._model.getPath(self._lenght)