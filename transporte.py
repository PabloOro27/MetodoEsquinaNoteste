import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
from copy import deepcopy
from modeloTransporte import ModeloTransporte

class AplicacionTransporte:
    def __init__(self, root):
        self.root = root
        self.root.title("Solucionador de Problemas de Transporte")
        self.root.geometry("1000x700")
        
        self.modelo = ModeloTransporte()
        
        style = ttk.Style()
        style.theme_use('clam')
        
        mainFrame = ttk.Frame(root, padding="10")
        mainFrame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.crearSeccionEntrada(mainFrame)
        self.crearBotonesControl(mainFrame)
        self.crearAreaResultados(mainFrame)
        
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        mainFrame.columnconfigure(0, weight=1)
        mainFrame.rowconfigure(2, weight=1)
        
    def crearSeccionEntrada(self, parent):
        frameEntrada = ttk.LabelFrame(parent, text="Entrada de Datos", padding="10")
        frameEntrada.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        ttk.Label(frameEntrada, text="Numero de Fuentes:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.varFuentes = tk.IntVar(value=3)
        ttk.Spinbox(frameEntrada, from_=1, to=10, textvariable=self.varFuentes, width=10).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(frameEntrada, text="Numero de Destinos:").grid(row=0, column=2, padx=5, pady=5, sticky=tk.W)
        self.varDestinos = tk.IntVar(value=4)
        ttk.Spinbox(frameEntrada, from_=1, to=10, textvariable=self.varDestinos, width=10).grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(frameEntrada, text="Crear Tabla", command=self.crearTabla).grid(row=0, column=4, padx=20, pady=5)
        
        self.frameTabla = ttk.Frame(frameEntrada)
        self.frameTabla.grid(row=1, column=0, columnspan=5, pady=10)
        
        self.cargarEjemplo()
        
    def crearBotonesControl(self, parent):
        frameBotones = ttk.Frame(parent)
        frameBotones.grid(row=1, column=0, pady=10)
        
        ttk.Button(frameBotones, text="Cargar Ejemplo", command=self.cargarEjemplo).pack(side=tk.LEFT, padx=5)
        ttk.Button(frameBotones, text="Resolver", command=self.resolverProblema).pack(side=tk.LEFT, padx=5)
        ttk.Button(frameBotones, text="Limpiar", command=self.limpiarTodo).pack(side=tk.LEFT, padx=5)
        
    def crearAreaResultados(self, parent):
        self.textResultados = scrolledtext.ScrolledText(parent, wrap=tk.WORD, width=80, height=20)
        self.textResultados.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
    def crearTabla(self):
        # Limpiar tabla anterior
        for widget in self.frameTabla.winfo_children():
            widget.destroy()
        
        m = self.varFuentes.get()
        n = self.varDestinos.get()
        
        ttk.Label(self.frameTabla, text="", width=10).grid(row=0, column=0)
        for j in range(n):
            ttk.Label(self.frameTabla, text=f"C{j+1}", width=10).grid(row=0, column=j+1)
        ttk.Label(self.frameTabla, text="Suministro", width=10).grid(row=0, column=n+1)
        
        self.entriesCostos = []
        self.entriesOferta = []
        
        for i in range(m):
            ttk.Label(self.frameTabla, text=f"P{i+1}", width=10).grid(row=i+1, column=0)
            filaCostos = []
            
            for j in range(n):
                entry = ttk.Entry(self.frameTabla, width=10)
                entry.grid(row=i+1, column=j+1, padx=2, pady=2)
                filaCostos.append(entry)
            
            self.entriesCostos.append(filaCostos)
            
            entryOferta = ttk.Entry(self.frameTabla, width=10)
            entryOferta.grid(row=i+1, column=n+1, padx=2, pady=2)
            self.entriesOferta.append(entryOferta)
        
        ttk.Label(self.frameTabla, text="DEMANDA", width=10).grid(row=m+1, column=0)
        self.entriesDemanda = []
        
        for j in range(n):
            entry = ttk.Entry(self.frameTabla, width=10)
            entry.grid(row=m+1, column=j+1, padx=2, pady=2)
            self.entriesDemanda.append(entry)
        
        self.labelTotalOferta = ttk.Label(self.frameTabla, text="", width=10)
        self.labelTotalOferta.grid(row=m+1, column=n+1)
        
    def cargarEjemplo(self):
        self.varFuentes.set(3)
        self.varDestinos.set(4)
        self.crearTabla()
        
        costosEjemplo = [
            [15, 30, 80, 50],
            [70, 90, 30, 40],
            [80, 40, 110, 90]
        ]
        
        ofertaEjemplo = [15, 35, 40]
        demandaEjemplo = [35, 25, 10, 20]
        
        for i in range(3):
            for j in range(4):
                valor = costosEjemplo[i][j]
                if valor == 'X':
                    self.entriesCostos[i][j].insert(0, "9999")
                else:
                    self.entriesCostos[i][j].insert(0, str(valor))
            
            self.entriesOferta[i].insert(0, str(ofertaEjemplo[i]))
        
        for j in range(4):
            self.entriesDemanda[j].insert(0, str(demandaEjemplo[j]))
            
    def obtenerDatosEntrada(self):
        try:
            m = self.varFuentes.get()
            n = self.varDestinos.get()
            
            costos = []
            for i in range(m):
                fila = []
                for j in range(n):
                    valor = float(self.entriesCostos[i][j].get())
                    fila.append(valor)
                costos.append(fila)
            
            oferta = []
            for i in range(m):
                oferta.append(float(self.entriesOferta[i].get()))
            
            demanda = []
            for j in range(n):
                demanda.append(float(self.entriesDemanda[j].get()))
            
            return costos, oferta, demanda
            
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores numericos validos")
            return None, None, None
    
    def resolverProblema(self):
        costos, oferta, demanda = self.obtenerDatosEntrada()
        
        if costos is None:
            return
        
        self.modelo.configurarProblema(costos, oferta, demanda)
        
        self.textResultados.delete(1.0, tk.END)
        self.textResultados.insert(tk.END, "="*80 + "\n")
        self.textResultados.insert(tk.END, "PROBLEMA DE TRANSPORTE - MINIMIZACION DE COSTOS\n")
        self.textResultados.insert(tk.END, "="*80 + "\n\n")
        
        sumaOferta = sum(oferta)
        sumaDemanda = sum(demanda)
        self.textResultados.insert(tk.END, f"Suma de Oferta: {sumaOferta}\n")
        self.textResultados.insert(tk.END, f"Suma de Demanda: {sumaDemanda}\n")
        
        if not self.modelo.esBalanceado:
            self.textResultados.insert(tk.END, "\nPROBLEMA NO BALANCEADO\n")
            if sumaOferta > sumaDemanda:
                self.textResultados.insert(tk.END, f"Se agrego un destino ficticio con demanda: {sumaOferta - sumaDemanda}\n")
            else:
                self.textResultados.insert(tk.END, f"Se agrego una fuente ficticia con oferta: {sumaDemanda - sumaOferta}\n")
        else:
            self.textResultados.insert(tk.END, "\nPROBLEMA BALANCEADO\n")
        
        self.textResultados.insert(tk.END, "\n" + "-"*50 + "\n")
        self.textResultados.insert(tk.END, "SOLUCION INICIAL Metodo de la Esquina Noroeste\n")
        self.textResultados.insert(tk.END, "-"*50 + "\n")
        
        solucionInicial = self.modelo.metodoEsquinaNoroeste()
        costoInicial = self.modelo.calcularCostoTotal()
        
        self.mostrarTablaSolucion(solucionInicial, "Asignaciones iniciales:")
        self.textResultados.insert(tk.END, f"\nCosto Total: Q{costoInicial:,.2f}\n")
        
        self.textResultados.insert(tk.END, "\n" + "-"*50 + "\n")        
        
        self.mostrarDetallesAsignaciones(solucionInicial)
        
    def mostrarTablaSolucion(self, solucion, titulo):
        self.textResultados.insert(tk.END, f"\n{titulo}\n\n")
        
        m, n = solucion.shape
        
        nReal = self.varDestinos.get()
        mReal = self.varFuentes.get()
        
        self.textResultados.insert(tk.END, " "*15)
        for j in range(n):
            if j < nReal:
                self.textResultados.insert(tk.END, f"C{j+1}".center(12))
            else:
                self.textResultados.insert(tk.END, "Ficticio".center(12))
        self.textResultados.insert(tk.END, "Suministro".center(15) + "\n")
        
        self.textResultados.insert(tk.END, "-"*(15 + n*12 + 15) + "\n")
        
        for i in range(m):
            if i < mReal:
                self.textResultados.insert(tk.END, f"P{i+1}".ljust(15))
            else:
                self.textResultados.insert(tk.END, "Ficticia".ljust(15))
            
            for j in range(n):
                valor = solucion[i, j]
                costo = self.modelo.costos[i, j]
                
                if valor > 0:
                    texto = f"{int(valor)}"
                    if costo < 9999:
                        texto += f"({int(costo)})"
                    self.textResultados.insert(tk.END, texto.center(12))
                else:
                    if costo >= 9999:
                        self.textResultados.insert(tk.END, "X".center(12))
                    else:
                        self.textResultados.insert(tk.END, "-".center(12))
            
            self.textResultados.insert(tk.END, f"{int(self.modelo.oferta[i])}".center(15) + "\n")
        
        self.textResultados.insert(tk.END, "-"*(15 + n*12 + 15) + "\n")
        
        self.textResultados.insert(tk.END, "DEMANDA".ljust(15))
        for j in range(n):
            self.textResultados.insert(tk.END, f"{int(self.modelo.demanda[j])}".center(12))
        
        total = sum(self.modelo.oferta)
        self.textResultados.insert(tk.END, f"{int(total)}".center(15) + "\n")
        
    def mostrarDetallesAsignaciones(self, solucion):
        self.textResultados.insert(tk.END, "\n" + "="*50 + "\n")
        self.textResultados.insert(tk.END, "RESUMEN DE ASIGNACIONES OPTIMAS:\n")
        self.textResultados.insert(tk.END, "="*50 + "\n\n")
        
        m, n = solucion.shape
        nReal = self.varDestinos.get()
        mReal = self.varFuentes.get()
        
        totalTransportado = 0
        
        for i in range(m):
            for j in range(n):
                if solucion[i, j] > 0:
                    cantidad = solucion[i, j]
                    costoUnitario = self.modelo.costos[i, j]
                    costoTotal = cantidad * costoUnitario
                    
                    if i < mReal and j < nReal and costoUnitario < 9999:
                        origen = f"P{i+1}"
                        destino = f"C{j+1}"
                        self.textResultados.insert(tk.END, 
                            f"* {origen} -> {destino}: {int(cantidad)} unidades x Q{costoUnitario} = Q{costoTotal:,.2f}\n")
                        totalTransportado += cantidad
                    elif costoUnitario < 9999:
                        if i >= mReal:
                            origen = "Fuente Ficticia"
                            destino = f"C{j+1}"
                        else:
                            origen = f"P{i+1}"
                            destino = "Destino Ficticio"
                        self.textResultados.insert(tk.END, 
                            f"* {origen} -> {destino}: {int(cantidad)} unidades (ficticio)\n")
        
        self.textResultados.insert(tk.END, f"\nTotal transportado: {int(totalTransportado)} unidades\n")
        
        self.textResultados.insert(tk.END, "\n" + "-"*50 + "\n")
        self.textResultados.insert(tk.END, "ANALISIS DE CUMPLIMIENTO:\n")
        self.textResultados.insert(tk.END, "-"*50 + "\n")
        
        self.textResultados.insert(tk.END, "\nOferta satisfecha:\n")
        for i in range(mReal):
            totalEnviado = sum(solucion[i, :])
            self.textResultados.insert(tk.END, f"  P{i+1}: {int(totalEnviado)}/{int(self.modelo.oferta[i])}\n")
        
        self.textResultados.insert(tk.END, "\nDemanda satisfecha:\n")
        for j in range(nReal):
            totalRecibido = sum(solucion[:, j])
            self.textResultados.insert(tk.END, f"  C{j+1}: {int(totalRecibido)}/{int(self.modelo.demanda[j])}\n")
    
    def limpiarTodo(self):
        self.textResultados.delete(1.0, tk.END)
        
        for fila in self.entriesCostos:
            for entry in fila:
                entry.delete(0, tk.END)
        
        for entry in self.entriesOferta:
            entry.delete(0, tk.END)
        
        for entry in self.entriesDemanda:
            entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = AplicacionTransporte(root)
    root.mainloop()

if __name__ == "__main__":
    main()