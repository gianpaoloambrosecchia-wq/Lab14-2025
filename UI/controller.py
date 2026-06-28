import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._storeSelected = None
        self._nodeSelected = None


    def handleCreaGrafo(self, e):
        k = self._view._txtIntK.value
        if self._storeSelected is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Seleziona uno store dal menu", color="red")
            )
            self._view.update_page()
            return
        if k=="":
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserisci un numero di giorni massimo", color="red")
            )
            self._view.update_page()
            return
        try:
            k = int(k)
        except ValueError:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserisci un numero intero di giorni massimo", color="red")
            )
            self._view.update_page()
            return
        if k<=0:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Inserisci un numero intero positivo", color="red")
            )
            self._view.update_page()
            return

        self._model.buildGraph(self._storeSelected, k)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text("Grafo creato correttamente", color="green")
        )
        self._view._btnCerca.disabled = False
        self._view._btnRicorsione.disabled = False
        self._fillDDNodes()
        numNodes, numEdges = self._model.getGraphDetails()
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di nodi: {numNodes}", color="purple")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Numero di archi: {numEdges}", color="purple")
        )
        self._view.update_page()


    def handleCerca(self, e):
        if self._nodeSelected is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Seleziona un nodo dall'apposito menù", color="red")
            )
            self._view.update_page()
            return

        path = self._model.getLongestPath(self._nodeSelected)
        self._view.txt_result.controls.append(
            ft.Text(f"Nodo di partenza : {self._nodeSelected}")
        )
        for p in path:
            self._view.txt_result.controls.append(
                ft.Text(p)
            )
        self._view.update_page()



    def handleRicorsione(self, e):
        if self._nodeSelected is None:
            self._view.txt_result.controls.clear()
            self._view.txt_result.controls.append(
                ft.Text("Seleziona un nodo dall'apposito menù", color="red")
            )
            self._view.update_page()
            return
        path, score = self._model.getPath(self._nodeSelected)
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Il percorso ha peso massimo {score}", color = "purple")
        )
        for p in path:
            self._view.txt_result.controls.append(
                ft.Text(p)
            )
        self._view.update_page()


    def fillDDStores(self):
        stores = self._model.getAllStores()
        for store in stores:
            self._view._ddStore.options.append(
                ft.dropdown.Option(data = store,
                                   text = store.store_id,
                                   on_click=self._readStoreSelect)
            )
        self._view.update_page()


    def _fillDDNodes(self):
        nodes = self._model.getNodes()
        for n in nodes:
            self._view._ddNode.options.append(
                ft.dropdown.Option(data = n,
                                   text=n.order_id,
                                   on_click=self._readNodeSelect)
            )
        self._view.update_page()


    def _readStoreSelect(self, e):
        self._storeSelected = e.control.data


    def _readNodeSelect(self, e):
        self._nodeSelected = e.control.data



