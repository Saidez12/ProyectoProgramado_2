# Proyecto programado 2
# Rubén David Abarca Ramírez - 2022017072
# Saimon Hernández Venegas - 2022090508
# Daniel Rubén Arce Madriz - 2022200437


from asyncio.windows_events import NULL
import tkinter as tk
import pickle
from tkinter import *
from tkinter import messagebox
import random
import winsound
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# DICCIONARIO DE ALMACENAMIENTO
estadoActual = {
"indice" : -1,
"equipos" : NULL, 
"equipoActual": NULL, 
"codigo": 0, 
"listaDeClasificacion" : NULL, 
"equiposOrdenados": [],
"nombresOrdenados": NULL,
"datosTorneo": NULL,
"FaseFinalDelTorneo": []
} 


# VENTANA MADRE
cantidadEquiposVentana = tk.Tk()
cantidadEquiposVentana.resizable(False, False)
cantidadEquiposVentana.geometry("275x125")
cantidadEquiposVentana.title("Equipos")


# INGRESO DE EQUIPOS
def ingresoEquipos (event):
    infoEquiposVentana= tk.Toplevel(cantidadEquiposVentana)
    infoEquiposVentana.protocol("WM_DELETE_WINDOW", on_closing)
    infoEquiposVentana.resizable(False, False)
    infoEquiposVentana.geometry("430x225")
    infoEquiposVentana.title("Información de los equipos")
    x = cantidadEquiposVentana.winfo_x()
    y = cantidadEquiposVentana.winfo_y()
    infoEquiposVentana.geometry("+%d+%d" % (x+75, y+75))
    entNombreEquipo = tk.Entry(
        infoEquiposVentana, fg="White", bg="Black", width=10)
    entLugarProcedencia = tk.Entry(
        infoEquiposVentana, fg="White", bg="Black", width=10)
    entCantidadJugadores = tk.Entry(
        infoEquiposVentana, fg="White", bg="Black", width=10)
    entValorPlanilla = tk.Entry(
        infoEquiposVentana, fg="White", bg="Black", width=10)
    lblNombreEquipo = tk.Label(
        infoEquiposVentana, text="Indique el nombre del equipo: ")
    lblLugarProcedencia = tk.Label(
        infoEquiposVentana, text="Indique el lugar de procedencia del equipo: ")
    lblCantidadJugadores = tk.Label(
        infoEquiposVentana, text="Indique la cantidad de jugadores: ")
    lblValorPlanilla = tk.Label(
        infoEquiposVentana, text="Indique el valor de la planilla: ")
    lblNombreEquipo.place(x=10, y=25)
    entNombreEquipo.place(x=330, y=25)
    lblLugarProcedencia.place(x=10, y=50)
    entLugarProcedencia.place(x=330, y=50)
    lblCantidadJugadores.place(x=10, y=75)
    entCantidadJugadores.place(x=330, y=75)
    lblValorPlanilla.place(x=10, y=100)
    entValorPlanilla.place(x=330, y=100)
    btnContinuarIngreso = tk.Button(
        infoEquiposVentana, text="CONTINUAR", bg="#926359", fg="#FFFFFF")
    btnContinuarIngreso.place(x=175, y=175)
    btnContinuarIngreso.unbind("<Button-1>")
    equipoActual  = estadoActual["equipoActual"]


# ELIMINACIÓN DE EQUIPOS
    def eliminarEquipo(event):
        winVentana5= tk.Toplevel(cantidadEquiposVentana)
        winVentana5.resizable(False, False)
        winVentana5.geometry("375x125")
        winVentana5.title("Modificar un equipo")
        x = 100
        y = 200
        winVentana5.geometry("+%d+%d" % (x+75, y+75))
        winVentana5.protocol("WM_DELETE_WINDOW", on_closing)
        #winVentana4.withdraw()
        lblEquipoAModificar = tk.Label(
            winVentana5, text="Indique el nombre del equipo que desea eliminar: ")
        lblEquipoAModificar.place(x=10, y=25)
        entEquipoAModificar = tk.Entry(
            winVentana5, fg="White", bg="Black", width=15)
        entEquipoAModificar.place(x=125, y=55)
        btnProcesarEquipo = tk.Button(
            winVentana5, text="ELIMINAR", bg="#926359", fg="#FFFFFF")
        btnProcesarEquipo.place(x=25, y=75)
        #btnProcesarEquipo.bind("<Button-1>", procesarEquipoAEliminar)

        def procesarEquipoAEliminar(event):
            try:
                equipoAEliminar = entNombreEquipo.get()
            except:
                messagebox.showinfo(message="Indique parámetros válidos")
            equipos = estadoActual["equipos"]
            codigo = estadoActual["codigo"]
            tableroDePuntosAnotados = {}
            if (equipoAEliminar in tableroDePuntosAnotados == True):
                estadoActual["equipos"] = equipos
                for y in range(len(equipos)):
                    codigo = y
                    equipoEliminar=list(equipos[codigo].values())
                    equipo = equipoEliminar[2]
                    if(equipo == equipoAEliminar):
                        print(equipos[codigo])
                        estadoActual["equipoActual"] = equipos[codigo]
                        estadoActual["codigo"] = codigo
                        equipos[codigo].clear()
                        messagebox.showinfo(message="El equipo se ha eliminado")
                        intermedio()
                        break
                    else:
                        continue
            else:
                messagebox.showinfo(message="Debe ingresar un equipo que se encuentre en el tablero de punto anotados")


# GUARDADO DE EQUIPOS
    def obtenerYGuardar():
        try:
            cantidadJugadores = int(entCantidadJugadores.get())
            valorPlanilla = int(entValorPlanilla.get())
        except:
            messagebox.showinfo(message="Indique valores numéricos de índole entera")
        procedencia = entLugarProcedencia.get()
        nombre = entNombreEquipo.get()
        entCantidadJugadores.delete (0,"end")
        entLugarProcedencia.delete (0,"end")
        entNombreEquipo.delete (0,"end")
        entValorPlanilla.delete (0,"end")
        guardarDiccionario(cantidadJugadores,procedencia, nombre, valorPlanilla)

    def agregarEquipo(event):
        indice  = estadoActual["indice"]
        indice+=1
        estadoActual["indice"] = indice
        if(indice < cantidadEquipos):
            obtenerYGuardar()
            if(indice == cantidadEquipos-1):
                intermedio()
        else:
            intermedio()

    def guardarDiccionario (cantidadJugadores,procedencia, nombre, valorPlanilla):
        equipos = estadoActual["equipos"]
        codigo = estadoActual["codigo"]
        if(codigo < cantidadEquipos):
            equipos[codigo] = {"Cantidad de jugadores": cantidadJugadores, "Lugar de procedencia": procedencia, "Nombre del equipo": nombre, "Valor de la planilla":valorPlanilla}
            estadoActual["codigo"] = estadoActual["codigo"]+1
        with open("data.json","wb") as fp:
            pickle.dump(equipos,fp)
        with open("data.json","rb") as fp:
            data = pickle.load(fp)
        print(equipos)


# GENERACIÓN DE PUNTAJES
    def puntajeAletorio(): 
        return random.randint(0,150)

    def matrizEquipos(event):
        winMatrizPuntos = tk.Toplevel(cantidadEquiposVentana)
        winMatrizPuntos.resizable(False, False)
        winMatrizPuntos.geometry("1250x600")
        winMatrizPuntos.title("Tabla de Resultados")
        x = 100
        y = 200
        winMatrizPuntos.geometry("+%d+%d" % (x+75, y+75))
        winMatrizPuntos.protocol("WM_DELETE_WINDOW", on_closing)
        equiposDic = {}
        codigo = estadoActual["codigo"] 
        equipos1 = estadoActual["equipos"]
        for y in range(len(equipos1)):
            codigo = y
            equiposD=list(equipos1[codigo].values())
            nombreD = equiposD[2]
            equiposDic[codigo] = nombreD
        inicio = 0
        EquiposT = [[""]]
        for x in range(len(equiposDic)):
            EquiposT[0].append([equiposDic[inicio]]) 
            EquiposT.append([equiposDic[inicio], puntajeAletorio(), puntajeAletorio(), puntajeAletorio(), puntajeAletorio(), puntajeAletorio(), puntajeAletorio()])
            inicio+=1
        btnEliminarEquipo= tk.Button(
            winMatrizPuntos, text="ELIMINAR EQUIPO", bg="#926359", fg="#FFFFFF")
        btnEliminarEquipo.place(x=25, y=300)
        btnEliminarEquipo.bind("<Button-1>", eliminarEquipo)


        class Table:
            def __init__(self, winMatrizPuntos):
                puntoEquipo = [] 
                dataPorEquipo = []
                for iFila in range(total_rows):
                    dataPorEquipo = []
                    for iColumna in range(total_columns):
                        self.e = Entry(winMatrizPuntos, width=15, fg='black',
                                        font=('Arial', 12, 'bold'))
                        self.e.grid(row=iFila, column=iColumna)
                        if iFila != iColumna:
                            self.e.insert(END, lst[iFila][iColumna])
                            if iFila != 0:
                                dataPorEquipo.append(lst[iFila][iColumna])
                        else:
                            if iFila == 0 and iColumna == 0:
                                self.e.insert(END, "")
                            else:
                                self.e.insert(END, -1)
                                dataPorEquipo.append(-1)        
                    puntoEquipo.append(dataPorEquipo)
                puntoEquipo = puntoEquipo[1:]
                
                def estadisticasTablas():  
                    listaDeClasificacion = []
                    indiceColumnaDato = 0
                    for fila in range(len(puntoEquipo)):
                        listaPorEquipo = []
                        indiceColumnaDato += 1
                        sumaDeClasificacion = 0
                        indiceFilaDato = 0
                        partidosGanados = 0
                        partidosPerdidos = 0
                        partidosEmpatados = 0
                        totalPuntosAFavor = 0
                        totalPuntosEnContra = 0
                        totalDiferenciaDePuntos = 0
                        estadoPartidos = True
                        for columna in range(len(puntoEquipo[0])):
                            if type(puntoEquipo[fila][columna]) == str:
                                listaPorEquipo.append(puntoEquipo[fila][columna])
                            else:
                                if puntoEquipo[fila][columna] == -1:
                                    continue
                                if indiceFilaDato == fila:
                                    indiceFilaDato+=1
                                if puntoEquipo[fila][columna] > puntoEquipo[indiceFilaDato][indiceColumnaDato]:
                                    sumaDeClasificacion += 3
                                    partidosGanados += 1
                                elif puntoEquipo[fila][columna] < puntoEquipo[indiceFilaDato][indiceColumnaDato]:
                                    partidosPerdidos += 1
                                elif puntoEquipo[fila][columna] == puntoEquipo[indiceFilaDato][indiceColumnaDato]:
                                    if puntoEquipo[fila][columna] == 0 and puntoEquipo[indiceFilaDato][indiceColumnaDato] == 0:
                                        estadoPartido = False
                                    sumaDeClasificacion += 1
                                    partidosEmpatados += 1
                                indiceFilaDato += 1
                                totalPuntosAFavor += puntoEquipo[fila][columna]
                                if type(puntoEquipo[indiceFilaDato-1][indiceColumnaDato] ) == int:
                                    totalPuntosEnContra += puntoEquipo[indiceFilaDato-1][indiceColumnaDato]    
                        totalDiferenciaDePuntos = totalPuntosAFavor - totalPuntosEnContra
                        if totalPuntosAFavor == 0 and totalPuntosEnContra == 0:
                            estadoPartido = False
                        listaPorEquipo.append(partidosGanados)
                        listaPorEquipo.append(partidosEmpatados)
                        listaPorEquipo.append(partidosPerdidos)
                        listaPorEquipo.append(sumaDeClasificacion)
                        listaPorEquipo.append(totalPuntosAFavor)
                        listaPorEquipo.append(totalPuntosEnContra)
                        listaPorEquipo.append(totalDiferenciaDePuntos)
                        listaPorEquipo.append(estadoPartidos)
                        listaDeClasificacion.append(listaPorEquipo)
                    return listaDeClasificacion

                def ordenarEquipos():
                    equipos = estadisticasTablas()
                    equiposOrdenados = []
                    equiposOrdenados.append(equipos[0])
                    equipos = equipos[1:]
                    for posicionEquipo in range(len(equipos)):
                        for equipoComparacion in range(len(equiposOrdenados)):
                            if equipos[posicionEquipo][4] > equiposOrdenados[equipoComparacion][4]:
                                equiposOrdenados.insert(equipoComparacion, equipos[posicionEquipo])
                                break
                        if equipos[posicionEquipo] not in equiposOrdenados:
                            equiposOrdenados.append(equipos[posicionEquipo])
                    estadoActual["listaDeClasificacion"] = equiposOrdenados
                    return equiposOrdenados

                def verTablaEstadisticas(event):
                    winStats= tk.Toplevel(winMatrizPuntos)
                    winStats.resizable(False, False)
                    winStats.geometry("1400x500")
                    winStats.title("Equipos a la final")
                    x = 100
                    y = 200
                    winStats.geometry("+%d+%d" % (x+75, y+75))
                    class Table:
                        def __init__(self, winStats):
                            for iFila in range(total_rows):
                                for iColumna in range(total_columns):
                                    self.e = Entry(winStats, width=18, fg='black',
                                                    font=('Arial', 12, 'bold'))
                                    self.e.grid(row=iFila, column=iColumna)
                                    self.e.insert(END, lst[iFila][iColumna])

# TABLA DE RESULTADOS
                    def equiposGanadores():
                        Tabla1=estadoActual["FaseFinalDelTorneo"]
                        print(Tabla1)
                        EquiposGanadores=[]
                        indice=1
                        if(Tabla1!=[]):
                            while(indice<len(Tabla1)):
                                EquiposGanadores.append(Tabla1[indice][4])
                                indice+=1
                            print(EquiposGanadores)
                            return EquiposGanadores
                        return EquiposGanadores

                    def puntajeAleatorio(): 
                        return random.randint(0,150)

                    def nombresDeEquiposOrdenados(nombresOrdenados=[],Lista=ordenarEquipos(),indice=0):
                        if(indice>=len(Lista)):
                            return nombresOrdenados
                        Equipo=[(Lista[indice][0])]
                        return nombresDeEquiposOrdenados(nombresOrdenados+[Equipo],Lista,indice+1)

                    def Tabla(NumeroDeEquiposEnLaFinal,equiposDic=nombresDeEquiposOrdenados(),d=[["Equipo","Puntos Anotados","Equipo","Puntos Anotados","Ganador"]],inicio=0,EquipoGanador=""):
                        if(NumeroDeEquiposEnLaFinal<len(equiposDic) and inicio==0):
                            equiposDic=equiposDic[:NumeroDeEquiposEnLaFinal]
                        if(inicio>=len(equiposDic)):
                            return d
                        Equipo1=equiposDic[inicio]
                        Equipo2=equiposDic[inicio+1]
                        puntaje1=puntajeAleatorio()
                        puntaje2=puntajeAleatorio()
                        if(puntaje1>puntaje2):
                            EquipoGanador=Equipo1

                        elif(puntaje1<puntaje2):
                            EquipoGanador=Equipo2
                        elif(puntaje1==puntaje2):
                            puntaje1=puntajeAleatorio()
                        return Tabla(NumeroDeEquiposEnLaFinal,equiposDic,d+([[Equipo1,puntaje1,Equipo2,puntaje2,EquipoGanador]]),inicio+2,"")


                    def cantidadEquiposAFinal(event):
                        winVentana6= tk.Toplevel(winStats)
                        winVentana6.resizable(False, False)
                        winVentana6.geometry("375x125")
                        winVentana6.title("Equipos a la final")
                        x = 100
                        y = 200
                        winVentana6.geometry("+%d+%d" % (x+75, y+75))
                        winVentana6.protocol("WM_DELETE_WINDOW", on_closing)
                        lblEquiposFinal = tk.Label(
                            winVentana6, text="Indique la cantidad de equipos que desea en la final ")
                        lblEquiposFinal.place(x=10, y=25)
                        entEquiposFinal = tk.Entry(
                            winVentana6, fg="White", bg="Black", width=15)
                        entEquiposFinal.place(x=125, y=55)
                        def iniciarFinal(event):
                            state=True
                            NumeroDeEquiposEnLaFinal=entEquiposFinal.get()
                            NumeroDeEquiposEnLaFinal=int(NumeroDeEquiposEnLaFinal)
                            equipos10=ordenarEquipos()
                            if(NumeroDeEquiposEnLaFinal%2!=0):
                                messagebox.showinfo(message="El Numero de equipos en la final debe ser un número par")
                                state=False
                            if(NumeroDeEquiposEnLaFinal>len(equipos10)):
                                messagebox.showinfo(message="El número de equipos en la final debe ser un número igual o menor a la cantidad inicial de equipos")
                                state=False
                            if(NumeroDeEquiposEnLaFinal==0):
                                messagebox.showinfo(message="El número de equipos en la final debe ser un número mayor a cero")
                                state=False
                            if(state==True):
                                winMatrizFinal = tk.Toplevel(winVentana6)
                                winMatrizFinal.resizable(False, False)
                                winMatrizFinal.geometry("1250x500")
                                winMatrizFinal.title("Tabla de Fase Final de campeonato")
                                x = 100
                                y = 200
                                winMatrizFinal.geometry("+%d+%d" % (x+75, y+75))
                                winMatrizFinal.protocol("WM_DELETE_WINDOW", on_closing)
                                class Table:
                                        def __init__(self, winMatrizFinal):
                                            for i in range(total_rows):
                                                for j in range(total_columns):
                                                    self.e = Entry(winMatrizFinal, width=15, fg='black',
                                                                    font=('Arial', 12, 'bold'))
                                                    self.e.grid(row=i, column=j)
                                                    self.e.insert(END, lst[i][j])
                                Equiposganadores=equiposGanadores()
                                if(Equiposganadores!=[]):
                                    lst = Tabla(NumeroDeEquiposEnLaFinal,equiposDic=Equiposganadores)
                                    estadoActual["FaseFinalDelTorneo"]+=lst
                                else:
                                    lst = Tabla(NumeroDeEquiposEnLaFinal)
                                    estadoActual["FaseFinalDelTorneo"]+=lst
                                print (lst)        
                                print(estadoActual["FaseFinalDelTorneo"]) 
                                print(Equiposganadores)     
                                total_rows = len(lst)
                                total_columns = len(lst[0])
                                t = Table(winMatrizFinal)
                                if(len(Equiposganadores)==2):
                                    btnFinal= tk.Button(winMatrizFinal, text="Menú de estadisticas", bg="#926359", fg="#FFFFFF")
                                    btnFinal.place(x=1000, y=75)
                                    #Hacer el menú de estadisticas
                                    btnFinal.bind("<Button-1>",)
                                elif(NumeroDeEquiposEnLaFinal>2 ):
                                    btnFinal= tk.Button(winMatrizFinal, text="SIGUIENTE RONDA", bg="#926359", fg="#FFFFFF")
                                    btnFinal.place(x=1000, y=75)
                                    
                                    btnFinal.bind("<Button-1>",iniciarFinal )
                                else:
                                    btnFinal= tk.Button(winMatrizFinal, text="Menú de estadisticas", bg="#926359", fg="#FFFFFF")
                                    btnFinal.place(x=1000, y=75)
                                    #Hacer el menú de estadisticas
                                    btnFinal.bind("<Button-1>", grafico1)
                                    def grafico1(event):
                                        dataEquipos = estadoActual["listaDeClasificacion"]
                                        
                                        df = pd.DataFrame(data=dataEquipos)

                                        my_dict =pd.read_json("data.json")
                                        df = pd.DataFrame(data=my_dict)
                                        lbl=["Tigres", "Ratones", "Leones", "Elefantes"]
                                        fig1=df.plot.area(title="Total de puntos recibidos en todo el campeonato", y='TotalDePuntos',
                                                figsize=(8,8),stacked=False).get_figure();

                                        import tkinter  as tk 
                                        winGrafico = tk.Toplevel(winMatrizFinal)
                                        winGrafico .geometry("800x800")   
                                        winGrafico .title("Graphics")
                                        plot1 = FigureCanvasTkAgg(fig1, winGrafico)
                                        plot1.get_tk_widget().grid(row=1,column=1,padx=30,pady=30)
                                        winGrafico.mainloop() 
                                
                        btnFinal= tk.Button(winVentana6, text="Iniciar Final", bg="#926359", fg="#FFFFFF")
                        btnFinal.place(x=25, y=75)
                        btnFinal.bind("<Button-1>",iniciarFinal )
                    btnIniciar = tk.Button(winStats, text="SIMULACIÓN", bg="#926359", fg="#FFFFFF")
                    btnIniciar.place(x=25, y=300)
                    btnIniciar.bind("<Button-1>", cantidadEquiposAFinal)
                        
                    lst = [["Equipo", "Partidos Ganados", "Partidos Empatados", "Partidos Perdidos", "Puntaje", "Puntos A Favor", "Puntos En Contra", "Diferencia De Puntos"]] + ordenarEquipos()
                    total_rows = len(lst)
                    total_columns = len(lst[0])
                    t = Table(winStats)
                    winStats.mainloop()
                    
                btnResultados= tk.Button(
                winMatrizPuntos, text="RESULTADOS", bg="#926359", fg="#FFFFFF")
                btnResultados.place(x=150, y=300)
                btnResultados.bind("<Button-1>", verTablaEstadisticas)                    
                
                #Campeonato
                def estadisticasDelCampeonato(event):
                    equiposOrdenados = ordenarEquipos()
                    codigo = estadoActual["codigo"] 
                    equipos3= estadoActual["equipos"]
                    estadisticas = estadoActual["listaDeClasificacion"]

                    def topPlanilla():
                        valorPlanillaLista = []
                        for y in range(len(equipos3)):
                            codigo = y
                            equipos4= list(equipos3[codigo].values())
                            valorPlanillaLista.append(equipos4[3]) 
                        valorPlanillaLista.sort(reverse = True)
                        return valorPlanillaLista
                    
                    def distPorProcedencia():
                        lugarProcendencia = []
                        for y in range(len(equipos3)):
                            codigo = y
                            equipos4= list(equipos3[codigo].values())
                            lugarProcendencia.append(equipos4[1])
        
                  

        lst = EquiposT
        total_rows = len(lst)
        total_columns = len(lst[0])
        t = Table(winMatrizPuntos)
        cantidadEquiposVentana.mainloop()


# LOBBY
    def intermedio():
        winVentana3= tk.Toplevel(infoEquiposVentana)
        winVentana3.resizable(False, False)
        winVentana3.geometry("285x175")
        winVentana3.title("Modificar un equipo")
        x = infoEquiposVentana.winfo_x()
        y = infoEquiposVentana.winfo_y()
        winVentana3.geometry("+%d+%d" % (x+75, y+75))
        #.withdraw a winVentana4 en la "segunda corrida"
        infoEquiposVentana.withdraw()
        winVentana3.protocol("WM_DELETE_WINDOW", on_closing)
        lblEquiposGuardados = tk.Label(
            winVentana3, text="Los equipos se han guardado satisfactoriamente")
        lblEquiposGuardados.place(x=15, y=25)
        btnModificar = tk.Button(
            winVentana3, text="MODIFICAR", bg="#926359", fg="#FFFFFF")
        btnModificar.place(x=25, y=75)
        btnModificar.bind("<Button-1>", modificarDiccionario)
        btnTablaResultados= tk.Button(
            winVentana3, text="VER TABLA", bg="#926359", fg="#FFFFFF")
        btnTablaResultados.place(x=150, y=125)
        btnTablaResultados.bind("<Button-1>", matrizEquipos)





# MODIFICACIONES DE EQUIPOS
    def editarEquipo(event):
        almacenarModificaciones()
        intermedio()

    def almacenarModificaciones():
        codigo = estadoActual["codigo"]
        equipos = estadoActual["equipos"]
        try:
            cantidadJugadores = int(entCantidadJugadores.get())
            valorPlanilla = int(entValorPlanilla.get())
        except:
            messagebox.showinfo(message="Indique valores numéricos de índole entero")
        procedencia = entLugarProcedencia.get()
        nombre = entNombreEquipo.get()
        equipos[codigo] = {"Cantidad de jugadores": cantidadJugadores, "Lugar de procedencia": procedencia, "Nombre del equipo": nombre, "Valor de la planilla":valorPlanilla}
        with open("data.json","wb") as fp:
            pickle.dump(equipos,fp)
        with open("data.json","rb") as fp:
            data = pickle.load(fp)
        print(data)

    def modificarDiccionario(event):
        winVentana4= tk.Toplevel(cantidadEquiposVentana)
        winVentana4.resizable(False, False)
        winVentana4.geometry("375x125")
        winVentana4.title("Modificar un equipo")
        x = 100
        y = 200
        winVentana4.geometry("+%d+%d" % (x+75, y+75))
        winVentana4.protocol("WM_DELETE_WINDOW", on_closing)
        #winVentana3.withdraw()
        lblEquipoAModificar = tk.Label(
            winVentana4, text="Indique el nombre del equipo que desea modificar la información: ")
        lblEquipoAModificar.place(x=10, y=25)
        entEquipoAModificar = tk.Entry(
            winVentana4, fg="White", bg="Black", width=15)
        entEquipoAModificar.place(x=125, y=55)
        btnModificarEquipo = tk.Button(
            winVentana4, text="MODIFICAR", bg="#926359", fg="#FFFFFF")
        btnModificarEquipo.place(x=25, y=75)

        def buscarEquipo (event):
            try:
                nombreEquipoAModificar = entEquipoAModificar.get()
            except:
                messagebox.showinfo(message="Debe indicar parámetros válidos")
            estadoActual["equipos"] = equipos
            for y in range(len(equipos)):
                codigo = y
                equipoAModificar = list(equipos[codigo].values())
                equipo = equipoAModificar[2]
                if(equipo == nombreEquipoAModificar):
                    print(equipos[codigo])
                    estadoActual["equipoActual"] = equipos[codigo]
                    estadoActual["codigo"] = codigo
                    ingresoEquipos(event)
                    break
                else:
                    continue
        btnModificarEquipo.bind("<Button-1>", buscarEquipo)


# INICIO DEL PROGRAMA
    if(equipoActual == NULL):
        try:
            cantidadEquipos = int(entCantidadEquipos.get())
        except:
            messagebox.showinfo(message="Debe indicar un valor numérico de índole entero")
        equipos = {}
        estadoActual["equipos"] = equipos
        cantidadEquiposVentana.withdraw()
        btnContinuarIngreso.bind("<Button-1>", agregarEquipo)
    else:
        entNombreEquipo.insert(0, equipoActual["Nombre del equipo"])
        entValorPlanilla.insert(0, equipoActual["Valor de la planilla"])
        entLugarProcedencia.insert(0, equipoActual["Lugar de procedencia"])
        entCantidadJugadores.insert(0, equipoActual["Cantidad de jugadores"])
        btnContinuarIngreso.bind("<Button-1>", editarEquipo)


# CERRADO DE PESTAÑAS
def on_closing():
    if messagebox.askokcancel("Salir", "Desea salir de la aplicación?"):
        cantidadEquiposVentana.quit()


# VENTANA INICIAL
cantidadEquiposVentana.title("Ingreso al campeonato")
cantidadEquiposVentana.eval("tk::PlaceWindow . center")
entCantidadEquipos = tk.Entry(
    cantidadEquiposVentana, fg="White", bg="Black", width=10,text="2")
lblCantidadEquipos = tk.Label(
    cantidadEquiposVentana, text="Indique la cantidad de equipos: ")
btnContinuar = tk.Button(
    cantidadEquiposVentana, text="Continuar...", bg="#926359", fg="#FFFFFF")
lblCantidadEquipos.place(x=10, y=25)
entCantidadEquipos.place(x=190, y=25)
btnContinuar.place(x=100, y=75)
btnContinuar.bind("<Button-1>", ingresoEquipos)
cantidadEquiposVentana.protocol("WM_DELETE_WINDOW", on_closing)
cantidadEquiposVentana.mainloop()



