import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleAnalizzaAeroporti(self,e):
        # metodo che verrà chiamato dal view quando l'utente premerà il bottone ""
        distanza = self._view.txt_distanza.value
        try:
            float(distanza)
        except ValueError:
            self._view.lst_result.controls.clear()
            self._view.lst_result.controls.append(ft.Text("Please provide a numerical value for distance."))
            self._view.update_page()
            return
        self._model.buildGraph(float(distanza))

        self._view.lst_result.controls.clear()
        self._view.lst_result.controls.append(ft.Text("Grafo correttamente creato!"))
        self._view.lst_result.controls.append(ft.Text(f"Il grafo contiene {self._model.getNumNodes()} nodi."))
        self._view.lst_result.controls.append(ft.Text(f"Il grafo contiene {self._model.getNumEdges()} archi."))
        # aggiungere l’elenco di tutti gli archi con la relativa distanza
        self._view.lst_result.controls.append(ft.Text(f"Archi che rispettano il requisito di distanza selezionato:"))

        for edge in self._model.getAllEdges():
            self._view.lst_result.controls.append(ft.Text(f"{edge[0].AIRPORT}->{edge[1].AIRPORT} -- AvgDist: {self._model.getAvgDistance(edge[0],edge[1])}"))

        self._view.update_page()