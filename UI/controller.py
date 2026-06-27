import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._r1 = None
        self._r2 = None


    def fillDDsRating(self):
        ratings = self._model.getRatings()
        for r in ratings:
            self._view._ddrating1.options.append(ft.dropdown.Option(r))
            self._view._ddrating2.options.append(ft.dropdown.Option(r))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        self._r1 = self._view._ddrating1.value
        self._r2 = self._view._ddrating2.value
        if self._r1 is None or self._r2 is None:
            self._view.txt_result.controls.append(ft.Text("inserire i valori di ratings", color="red"))
            self._view.update_page()
            return
        if self._r1 >= self._r2:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(ft.Text("il primo valore deve essere minore del secondo"
                                                          , color="red"))
            self._view.update_page()
            return

        self._view.txt_result.controls.clear()
        self._model.buildGraph(self._r1, self._r2)
        self._view.txt_result.controls.append(ft.Text("il grafo è stato creato correttamente"
                                                      , color="green"))
        self._view.txt_result.controls.append(ft.Text(f"il grafo contiene {len(self._model._grafo.nodes())} nodi"
                                                      f" e {len(self._model._grafo.edges())} archi"))
        self._view.update_page()

        self._view.txt_result.controls.append(ft.Text("i top 5 archi sono: ", color="green"))
        archibest = self._model.getArchiBest()
        for a in archibest:
            self._view.txt_result.controls.append(ft.Text(f"{a[0]} ---> {a[1]} con peso di {a[2]["weight"]}"))

        lungCompConn, nodiCompConn = self._model.getConnessaInfo()
        self._view.txt_result.controls.append(ft.Text(f"il numero di componeneti connesse è {lungCompConn}"
                                                      f" mentre la più grande è formata da {len(nodiCompConn)} nodi: "))
        for n in nodiCompConn:
            self._view.txt_result.controls.append(ft.Text(n.name))
        self._view.update_page()



    def handleCammino(self, e):
        bestPath = self._model.getBestPath()
        self._view.txt_result.controls.append(ft.Text(f"il percorso piu lungo che ho trovato  è: {len(bestPath)}", color="green"))
        for n in bestPath:
            self._view.txt_result.controls.append(ft.Text(f"{n} con eta pari a {n.date_of_birth}"))
        self._view.update_page()