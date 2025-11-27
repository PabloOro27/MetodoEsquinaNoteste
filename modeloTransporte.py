import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import numpy as np
from copy import deepcopy

class ModeloTransporte:
    def __init__(self):
        self.costos = None
        self.oferta = None
        self.demanda = None
        self.solucion = None
        self.esBalanceado = True
        self.costoTotal = 0
        self.iteraciones = []
        
    def configurarProblema(self, costos, oferta, demanda):
        self.costos = np.array(costos)
        self.oferta = np.array(oferta)
        self.demanda = np.array(demanda)
        
        # Verificar balance
        sumaOferta = sum(self.oferta)
        sumaDemanda = sum(self.demanda)
        
        if sumaOferta != sumaDemanda:
            self.esBalanceado = False
            self.balancearProblema(sumaOferta, sumaDemanda)
        else:
            self.esBalanceado = True
            
    def balancearProblema(self, sumaOferta, sumaDemanda):
        if sumaOferta > sumaDemanda:
            # Agregar destino ficticio
            diferencia = sumaOferta - sumaDemanda
            self.demanda = np.append(self.demanda, diferencia)
            
            nuevaColumna = np.zeros((self.costos.shape[0], 1))
            self.costos = np.hstack((self.costos, nuevaColumna))
        else:
            # Agregar fuente ficticia  
            diferencia = sumaDemanda - sumaOferta
            self.oferta = np.append(self.oferta, diferencia)
            
            nuevaFila = np.zeros((1, self.costos.shape[1]))
            self.costos = np.vstack((self.costos, nuevaFila))
    
    def metodoEsquinaNoroeste(self):
        m, n = self.costos.shape
        self.solucion = np.zeros((m, n))
        
        ofertaTemp = self.oferta.copy()
        demandaTemp = self.demanda.copy()
        
        i, j = 0, 0
        
        while i < m and j < n:
            cantidad = min(ofertaTemp[i], demandaTemp[j])
            self.solucion[i, j] = cantidad
            
            ofertaTemp[i] -= cantidad
            demandaTemp[j] -= cantidad
            
            if ofertaTemp[i] == 0:
                i += 1
            if demandaTemp[j] == 0:
                j += 1
                
        return self.solucion
    
    def calcularCostoTotal(self):
        self.costoTotal = np.sum(self.solucion * self.costos)
        return self.costoTotal        
               
