from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate


#-------------------------------Primera raiz y sus funciones (selección del archivo)----------------------------

primera_raiz=Tk()
primera_raiz.title("E3 - Búsqueda en series meteorológicas")
primera_raiz.iconbitmap("E3.ico")

def seleccion():
    file=filedialog.askopenfilename(title="Seleccionar archivo txt",filetypes=(("Archivos txt","*.txt"),("Todos los archivos","*.*")))
    global f
    f= pd.read_csv(file, delimiter="\t", header=None,parse_dates={"Fecha": [1, 2, 0]},index_col="Fecha")
    f.columns=["Prec","Tmax","Tmin"]
    pd.set_option("display.max_rows",None)
    messagebox.showinfo("Tarea finalizada","Ya puede trabajar con su archivo")

def ingreso():
    primera_raiz.destroy()


Label(primera_raiz,text="Bienvenido a la aplicación E3",font="bold").grid(row=0,column=0,columnspan=2)
Label(primera_raiz,text="Primero seleccione su archivo").grid(row=1,column=0,sticky="e")
ingreso_archivo=Button(primera_raiz,text="Seleccionar archivo",command=seleccion)
ingreso_archivo.grid(row=1,column=1)
Label(primera_raiz,text="Luego, ingrese al programa").grid(row=2,column=0,sticky="e")
ingreso_app=Button(primera_raiz,text="Ingresar al programa",command=ingreso)
ingreso_app.grid(row=2,column=1)

primera_raiz.mainloop()

#-------------------------------Segunda raiz (la principal) y menú con sus funciones----------------------------

raiz=Tk()
raiz.title("E3 - Búsqueda en series meteorológicas")
raiz.iconbitmap("E3.ico")

    
def exportar():
    archivo=open("New_file.txt","w")
    archivo.write(dataText.get("1.0","end"))
    archivo.close()
    
def salir():
    valor=messagebox.askquestion("Salir","¿Desea salir del programa?")
    if valor=="yes":
        raiz.destroy()

def licencia():
    messagebox.showinfo("Sobre el programa","Programa desarrollado por Ezequiel Elias en mayo del 2020.")

fechas=StringVar()

def mostrar_fechas():         #Función de frame1 p4, debe ser definida aquí para su correcta ejecución
    fechas.set("")
    j=f.loc[:].index.date
    texto="Datos desde el {primer_dia} al {ultimo_dia}.".format(primer_dia=j[0],ultimo_dia=j[int(len(j)-1)])
    fechas.set(texto)
mostrar_fechas()

barraMenu=Menu(raiz)
raiz.config(menu=barraMenu)
archivoMenu=Menu(barraMenu,tearoff=0)
archivoMenu.add_command(label="Abrir",command=lambda:[seleccion(),mostrar_fechas()])
archivoMenu.add_command(label="Exportar a .txt",command=exportar)
archivoMenu.add_command(label="Cerrar programa",command=salir)
acercadeMenu=Menu(barraMenu,tearoff=0)
acercadeMenu.add_command(label="Sobre",command=licencia)

barraMenu.add_cascade(label="Archivo",menu=archivoMenu)
barraMenu.add_cascade(label="Acerca de",menu=acercadeMenu)

#-------------------------------Frame 1 -----------------------------------------

miFrame=Frame(raiz)
miFrame.pack(fill="both",expand="True",side="left")
miFrame.config(bg="AliceBlue",width="600",height="450",bd=7)

#-------------------------------Funciones----------------------------------------

mindata=StringVar()
maxdata=StringVar()
opcion=IntVar()
grafico=IntVar()

def desplegardatos():   #Botón ENVIAR de Frame 1 - Lista: Despliega lista de datos según período seleccionado    
    año_i=int(añoCuadro.get())
    mes_i=int(mesCuadro.get())
    dia_i=int(diaCuadro.get())
    año_f=int(añoCuadrof.get())
    mes_f=int(mesCuadrof.get())
    dia_f=int(diaCuadrof.get())
    titulo=str(titGraf1.get())
    dataText.delete(1.0,END)
    
    x=datetime.date(year=año_i,month=mes_i,day=dia_i)
    y=datetime.date(year=año_f,month=mes_f,day=dia_f)

    if opcion.get()==1:
    
        j=f.loc[x:y,["Tmin","Tmax"]]
            
        linea1="Temperatura mínima media: "+ str(np.around(np.mean(f[x:y]["Tmin"]),decimals=1))+"°C"
        linea2="Temperatura máxima media: "+ str(np.around(np.mean(f[x:y]["Tmax"]),decimals=1))+"°C"

        dataText.insert(1.0,j)
        mindata.set(linea1)
        maxdata.set(linea2)

        if grafico.get()==1:
            plt.plot(j)
            plt.xlabel("Fecha",labelpad=10)
            plt.ylabel("Temperatura (°C)")
            plt.xticks(rotation=45)
            plt.title(titulo)
            plt.subplots_adjust(bottom=0.28)
            plt.show()

    if opcion.get()==2:
        
        j=f.loc[x:y,["Prec"]]

        linea1="Acumulado total: "+ str(np.around(np.sum(f[x:y]["Prec"]),decimals=1))+"mm"
        linea2="Máximo diario: "+ str(np.around(np.max(f[x:y]["Prec"]),decimals=1))+"mm"
        
        dataText.insert(1.0,j)
        mindata.set(linea1)
        maxdata.set(linea2)

        if grafico.get()==1:
            plt.bar(j[:].index,j["Prec"])
            plt.xlabel("Fecha")
            plt.ylabel("Precipitaciones(mm)")
            plt.xticks(rotation="vertical")
            plt.subplots_adjust(bottom=0.24)
            plt.title(titulo)
            plt.show()

def borraEntry():    #Botón BORRAR de Frame 1 - Lista
    añoCuadro.delete(0,END)
    mesCuadro.delete(0,END)
    diaCuadro.delete(0,END)
    añoCuadrof.delete(0,END)
    mesCuadrof.delete(0,END)
    diaCuadrof.delete(0,END)
    titGraf1.delete(0,END)
    opcion.set(0)
    graficoBoton.deselect()

opcionPrinc=IntVar()
Tn=IntVar()
Tx=IntVar()
med_extT=IntVar()
min_maxT=IntVar()
graficoT=IntVar()

def temperatura():   #Botón ENVIAR de Frame 1- Valores mensuales Opción TEMPERATURA
    añoinicio=int(añoinicioCuadro.get())
    añofinal=int(añofinalCuadro.get())
    mes=int(mesEscogidoCuadro.get())
    titulo=str(titGraf2T.get())
    dataText.delete(1.0,END)
    mindata.set("")
    maxdata.set("")

    j=f.loc[:].index
    k=f.loc[j[j.year>=añoinicio]&j[j.year<=añofinal]&j[j.month==mes]]
    w=k.loc[:].index

    if opcionPrinc.get()==1:     #Elige Valores Mensuales - Temperatura

        if Tn.get()==1: 

            if Tx.get()==1:  #Elige Valores Mensuales - Temperatura - Tmin y Tmax
        
                if med_extT.get()==1:    #Elige Valores Mensuales - Temperatura - Tmin y Tmax - valores medios
            
                    l=np.around(k.groupby(w.year).mean(),decimals=1)
                    rdo=l[:][["Tmin","Tmax"]]
                    dataText.insert(1.0,rdo)

                elif med_extT.get()==2:  #Elige Valores Mensuales - Temperatura - Tmin y Tmax - valores extremos

                    if min_maxT.get()==1:    #Elige Valores Mensuales - Temperatura - Tmin y Tmax - valores extremos - valor mínimo
                
                        l=np.around(k.groupby(w.year).min(),decimals=1)
                        rdo=l[:][["Tmin","Tmax"]]
                        dataText.insert(1.0,rdo)

                    elif min_maxT.get()==2:  #Elige Valores Mensuales - Temperatura - Tmin y Tmax - valores extremos - valor máximo
                        l=np.around(k.groupby(w.year).max(),decimals=1)
                        rdo=l[:][["Tmin","Tmax"]]
                        dataText.insert(1.0,rdo)

            else:    #Elige Valores Mensuales - Temperatura - Tmin
                
                if med_extT.get()==1:    #Elige Valores Mensuales - Temperatura - Tmin - valores medios
            
                    l=np.around(k.groupby(w.year).mean(),decimals=1)
                    rdo=l[:][["Tmin"]]
                    dataText.insert(1.0,rdo)

                elif med_extT.get()==2:  #Elige Valores Mensuales - Temperatura - Tmin - valores extremos

                    if min_maxT.get()==1:    #Elige Valores Mensuales - Temperatura - Tmin - valores extremos - valor mínimo
                
                        l=np.around(k.groupby(w.year).min(),decimals=1)
                        rdo=l[:][["Tmin"]]
                        dataText.insert(1.0,rdo)

                    elif min_maxT.get()==2:  #Elige Valores Mensuales - Temperatura - Tmin - valores extremos - valor máximo
                        l=np.around(k.groupby(w.year).max(),decimals=1)
                        rdo=l[:][["Tmin"]]
                        dataText.insert(1.0,rdo)

        if Tx.get()==1 and Tn.get()!=1 :    #Elige Valores Mensuales - Temperatura - Tmax

            if med_extT.get()==1:    #Elige Valores Mensuales - Temperatura - Tmax - valores medios
            
                l=np.around(k.groupby(w.year).mean(),decimals=1)
                rdo=l[:][["Tmax"]]
                dataText.insert(1.0,rdo)

            elif med_extT.get()==2:  #Elige Valores Mensuales - Temperatura - Tmax - valores extremos

                if min_maxT.get()==1:    #Elige Valores Mensuales - Temperatura - Tmax - valores extremos - valor mínimo
                
                    l=np.around(k.groupby(w.year).min(),decimals=1)
                    rdo=l[:][["Tmax"]]
                    dataText.insert(1.0,rdo)

                elif min_maxT.get()==2:  #Elige Valores Mensuales - Temperatura - Tmax - valores extremos - valor máximo
                    l=np.around(k.groupby(w.year).max(),decimals=1)
                    rdo=l[:][["Tmax"]]
                    dataText.insert(1.0,rdo)            

        if graficoT.get()==1:  #Elige graficar los datos
            plt.plot(rdo)
            plt.xticks(l[:].index,rotation="vertical")
            plt.xlabel("Año",labelpad=10)
            plt.subplots_adjust(bottom=0.2)
            plt.ylabel("Temperatura (°C)")
            plt.title(titulo)
            plt.show()

def borraEntryT():   #Botón BORRAR de Frame 1- Valores mensuales Opción TEMPERATURA
    añoinicioCuadro.delete(0,END)
    añofinalCuadro.delete(0,END)
    mesEscogidoCuadro.delete(0,END)
    titGraf2T.delete(0,END)
    opcionPrinc.set(0)
    med_extT.set(0)
    min_maxT.set(0)
    Tmin_Chbut.deselect()
    Tmax_Chbut.deselect()
    grafico2BotonT.deselect()

med_extP=IntVar()
min_maxP=IntVar()
graficoP=IntVar()

def precipitaciones():  #Botón ENVIAR de Frame 1- Valores mensuales Opción PRECIPITACIONES
    añoinicio=int(añoinicioCuadro.get())
    añofinal=int(añofinalCuadro.get())
    mes=int(mesEscogidoCuadro.get())
    titulo=str(titGraf2P.get())
    dataText.delete(1.0,END)
    mindata.set("")
    maxdata.set("")

    j=f.loc[:].index
    k=f.loc[j[j.year>=añoinicio]&j[j.year<=añofinal]&j[j.month==mes]]
    w=k.loc[:].index

    if opcionPrinc.get()==2:     #Elige Valores mensuales - opción Precipitaciones
        
        if med_extP.get()==1:    #Elige Valores mensuales - opción Precipitaciones - opción valores totales
            
            l=np.around(k.groupby(w.year).sum(),decimals=1)
            rdo=l[:][["Prec"]]
            dataText.insert(1.0,rdo)

        elif med_extP.get()==2:  #Elige Valores mensuales - opción Precipitaciones - opción valores extremos

            if min_maxP.get()==1:  #Elige Valores mensuales - opción Precipitaciones - opción valores extremos - opción valor mínimo
                
                l=np.around(k.groupby(w.year).min(),decimals=1)
                rdo=l[:][["Prec"]]
                dataText.insert(1.0,rdo)

            elif min_maxP.get()==2:  #Elige Valores mensuales - opción Precipitaciones - opción valores medios - opción valor máximo
                l=np.around(k.groupby(w.year).max(),decimals=1)
                rdo=l[:][["Prec"]]
                dataText.insert(1.0,rdo)

        if graficoP.get()==1:   #Elige graficar los datos
            plt.bar(rdo[:].index,rdo["Prec"])
            plt.xlabel("Año")
            plt.ylabel("Precipitaciones (mm)")
            plt.xticks(rotation="vertical")
            plt.subplots_adjust(bottom=0.16)
            plt.title(titulo)
            plt.show()

def borraEntryP():  #Botón BORRAR de Frame 1- Valores mensuales Opción PRECIPITACIONES
    añoinicioCuadro.delete(0,END)
    añofinalCuadro.delete(0,END)
    mesEscogidoCuadro.delete(0,END)
    titGraf2P.delete(0,END)
    opcionPrinc.set(0)
    med_extP.set(0)
    min_maxP.set(0)
    grafico2BotonP.deselect()

opcionU=IntVar()
Tmin_Tmax=IntVar()
May_Men_T=IntVar()
RankT=IntVar()

def tempU():  #Botón ENVIAR de Frame 1- Umbrales Opción TEMPERATURA
    añoinicio=int(añoUmbralCuadro.get())
    añofinal=int(añoUmbralCuadrof.get())
    mes=int(mesUmbralCuadro.get())
    diainicio=int(diaUmbralCuadro.get())
    diafinal=int(diaUmbralCuadrof.get())
    umbral=float(umbralCuadro.get())
    dataText.delete(1.0,END)
    mindata.set("")
    maxdata.set("")

    j=f.loc[:].index
    k=f.loc[j[j.year>=añoinicio]&j[j.year<=añofinal]&j[j.month==mes]&j[j.day>=diainicio]&j[j.day<=diafinal]]

    if opcionU.get()==1:   #Elige Umbrales - Temperatura

        if Tmin_Tmax.get()==1:    #Elige Umbrales - Temperatura - temperatura mínima

            if May_Men_T.get()==1:   #Elige Umbrales - Temperatura - temperatura mínima - mayor a
                
                rdo=k[k["Tmin"]>=umbral]

                if RankT.get()==1:  #Elige ordenar datos

                    rdo=rdo.sort_values(by="Tmin",ascending=False)
                    
                rdo2=rdo[:][["Tmin"]]
                dataText.insert(1.0,rdo2)

            elif May_Men_T.get()==2: #Elige Umbrales - Temperatura - temperatura mínima - menor a
                
                rdo=k[k["Tmin"]<=umbral]

                if RankT.get()==1:   #Elige ordenar datos

                    rdo=rdo.sort_values(by="Tmin",ascending=True)
                    
                rdo2=rdo[:][["Tmin"]]
                dataText.insert(1.0,rdo2)
            
        elif Tmin_Tmax.get()==2:   #Elige Umbrales - Temperatura - temperatura máxima

            if May_Men_T.get()==1:  #Elige Umbrales - Temperatura - temperatura máxima - mayor a
                
                rdo=k[k["Tmax"]>=umbral]

                if RankT.get()==1:  #Elige ordenar datos

                    rdo=rdo.sort_values(by="Tmax",ascending=False)
                    
                rdo2=rdo[:][["Tmax"]]
                dataText.insert(1.0,rdo2)
            

            elif May_Men_T.get()==2:  #Elige Umbrales - Temperatura - temperatura máxima - menor a
                
                rdo=k[k["Tmax"]<=umbral]

                if RankT.get()==1:  #Elige ordenar datos

                    rdo=rdo.sort_values(by="Tmax",ascending=True)
                    
                rdo2=rdo[:][["Tmax"]]
                dataText.insert(1.0,rdo2)

def borraEntryTU():   #Botón BORRAR de Frame 1- Umbrales Opción TEMPERATURA

    añoUmbralCuadro.delete(0,END)
    añoUmbralCuadrof.delete(0,END)
    mesUmbralCuadro.delete(0,END)
    diaUmbralCuadro.delete(0,END)
    diaUmbralCuadrof.delete(0,END)
    umbralCuadro.delete(0,END)
    opcionU.set(0)
    Tmin_Tmax.set(0)
    May_Men_T.set(0)
    rankingBotonT.deselect()
                            
May_Men_P=IntVar()
RankP=IntVar()

def precU():    #Botón ENVIAR de Frame 1- Umbrales Opción PRECIPITACIONES
    
    añoinicio=int(añoUmbralCuadro.get())
    añofinal=int(añoUmbralCuadrof.get())
    mes=int(mesUmbralCuadro.get())
    diainicio=int(diaUmbralCuadro.get())
    diafinal=int(diaUmbralCuadrof.get())
    umbral=float(umbralCuadro.get())
    dataText.delete(1.0,END)
    mindata.set("")
    maxdata.set("")

    j=f.loc[:].index
    k=f.loc[j[j.year>=añoinicio]&j[j.year<=añofinal]&j[j.month==mes]&j[j.day>=diainicio]&j[j.day<=diafinal]]

    if opcionU.get()==2:    #Elige Umbrales - Precipitaciones

        if May_Men_P.get()==1:   #Elige Umbrales - Precipitaciones - mayor a
                
            rdo=k[k["Prec"]>=umbral]

            if RankP.get()==1:   #Ordena los datos

                rdo=rdo.sort_values(by="Prec",ascending=False)
                    
            rdo2=rdo[:][["Prec"]]
            dataText.insert(1.0,rdo2)

        elif May_Men_P.get()==2: #Elige Umbrales - Precipitaciones - menor a
                
            rdo=k[k["Prec"]<=umbral]

            if RankP.get()==1:   #Ordena los datos

                rdo=rdo.sort_values(by="Prec",ascending=True)
                    
            rdo2=rdo[:][["Prec"]]
            dataText.insert(1.0,rdo2)

def borraEntryPU():   #Botón BORRAR de Frame 1- Umbrales Opción PRECIPITACIONES
    
    añoUmbralCuadro.delete(0,END)
    añoUmbralCuadrof.delete(0,END)
    mesUmbralCuadro.delete(0,END)
    diaUmbralCuadro.delete(0,END)
    diaUmbralCuadrof.delete(0,END)
    umbralCuadro.delete(0,END)
    opcionU.set(0)
    May_Men_P.set(0)
    rankingBotonP.deselect()
    

def unauotra():   #Deselecciona opciones y borra entradas cuando se cambia de sección

    if (opcion.get()==1) | (opcion.get()==2):
        borraEntryT()
        borraEntryP()
        borraEntryTU()
        borraEntryPU()

    elif opcionPrinc.get()==1:
        med_extP.set(0)
        min_maxP.set(0)
        grafico2BotonP.deselect()
        titGraf2P.delete(0,END)
        borraEntry()
        borraEntryTU()
        borraEntryPU()
        

    elif opcionPrinc.get()==2:
        med_extT.set(0)
        min_maxT.set(0)
        grafico2BotonT.deselect()
        titGraf2T.delete(0,END)
        borraEntry()
        borraEntryTU()
        borraEntryPU()

    elif opcionU.get()==1:
        May_Men_P.set(0)
        rankingBotonP.deselect()
        borraEntry()
        borraEntryT()
        borraEntryP()

    elif opcionU.get()==2:
        Tmin_Tmax.set(0)
        May_Men_T.set(0)
        rankingBotonT.deselect()
        borraEntry()
        borraEntryT()
        borraEntryP()
        

def borrarText():  #Botón BORRAR del Frame 2
    dataText.delete(1.0,END)
    mindata.set("")
    maxdata.set("")

def calculo_percentiles():
    j=f.loc[:].index

    tabla_percentiles_minimas=[]
    tabla_percentiles_maximas=[]
    indices=[]
    encabezado=["E","F","M","A","M","J","J","A","S","O","N","D"]
    for percentil in range(5,100,5):
        lista_percentiles_minimas=[]
        lista_percentiles_maximas=[]
        for i in set(j.month):
            k=f.loc[j[j.year>=1981]&j[j.year<=2010]&j[j.month==i]]
            lista_percentiles_minimas.append(np.around(np.nanpercentile(k["Tmin"],percentil),decimals=1))
            lista_percentiles_maximas.append(np.around(np.nanpercentile(k["Tmax"],percentil),decimals=1))
            if len(lista_percentiles_minimas)==12:
                tabla_percentiles_minimas.append(lista_percentiles_minimas)
            if len(lista_percentiles_maximas)==12:
                tabla_percentiles_maximas.append(lista_percentiles_maximas)
        indices.append(percentil)
    archivo=open("Percentiles 1981-2010.txt","a+")
    archivo.write("Temperaturas mínimas \n")
    archivo.write(tabulate(tabla_percentiles_minimas,tablefmt="github",headers=encabezado,showindex=indices,floatfmt=".1f"))
    archivo.write("\n")
    archivo.write("Temperaturas máximas \n")
    archivo.write(tabulate(tabla_percentiles_maximas,tablefmt="github",headers=encabezado,showindex=indices,floatfmt=".1f"))
    archivo.close()
    messagebox.showinfo("Tarea finalizada","Tiene disponible el archivo 'Percentiles 1981-2010' en el directorio de la aplicación. Cambie el nombre del archivo para que no sea sobrescrito.")

#------------------------------Frame 1 - Lista---------------------------------------
    
listLabelFrame=LabelFrame(miFrame,text="Lista",font=("bold","12"),padx=0,pady=0,width="300",height="250")
listLabelFrame.grid(row=0,column=0)
Label(listLabelFrame,text="Fecha de inicio").grid(row=1,column=0,sticky="e")
Label(listLabelFrame,text="Año:").grid(row=2,column=0,sticky="e")
Label(listLabelFrame,text="Mes:").grid(row=3,column=0,sticky="e")
Label(listLabelFrame,text="Dia:").grid(row=4,column=0,sticky="e")
Label(listLabelFrame,text="Fecha final").grid(row=1,column=2,sticky="e")
Label(listLabelFrame,text="Año:").grid(row=2,column=2,sticky="e")
Label(listLabelFrame,text="Mes:").grid(row=3,column=2,sticky="e")
Label(listLabelFrame,text="Dia:").grid(row=4,column=2,sticky="e")

añoCuadro=Entry(listLabelFrame)
añoCuadro.grid(row=2,column=1)
mesCuadro=Entry(listLabelFrame)
mesCuadro.grid(row=3,column=1)
diaCuadro=Entry(listLabelFrame)
diaCuadro.grid(row=4,column=1)
añoCuadrof=Entry(listLabelFrame)
añoCuadrof.grid(row=2,column=3)
mesCuadrof=Entry(listLabelFrame)
mesCuadrof.grid(row=3,column=3)
diaCuadrof=Entry(listLabelFrame)
diaCuadrof.grid(row=4,column=3)

Label(listLabelFrame,text="Escoger opcion").grid(row=5,column=0,sticky="e")
opcionTemp=Radiobutton(listLabelFrame,text="Temperatura",variable=opcion,value=1,command=unauotra)
opcionTemp.grid(row=5,column=1,sticky="w")
opcionPrec=Radiobutton(listLabelFrame,text="Precipitaciones",variable=opcion,value=2,command=unauotra)
opcionPrec.grid(row=6,column=1,sticky="w")
graficoBoton=Checkbutton(listLabelFrame,text="Gráfico",variable=grafico,onvalue=1,offvalue=0)
graficoBoton.grid(row=5,column=3,sticky="w")
Label(listLabelFrame,text="Título").grid(row=6,column=2,sticky="e")
titGraf1=Entry(listLabelFrame)
titGraf1.grid(row=6,column=3)
botonEnvio=Button(listLabelFrame,text="Enviar",command=desplegardatos)
botonEnvio.grid(row=7,column=3,sticky="w")
borrarEntries=Button(listLabelFrame,text="Borrar",command=borraEntry)
borrarEntries.grid(row=7,column=2,sticky="e")

#------------------------------Frame 1 -Valores Mensuales---------------------------------------

mensLabelFrame=LabelFrame(miFrame,text="Valores mensuales",font=("bold","12"),padx=0,pady=0,width="300",height="200")
mensLabelFrame.grid(row=8,column=0)
Label(mensLabelFrame,text="Año inicio").grid(row=9,column=0,sticky="e")
Label(mensLabelFrame,text="Año final").grid(row=10,column=0,sticky="e")
Label(mensLabelFrame,text="Mes").grid(row=11,column=0,sticky="e")

añoinicioCuadro=Entry(mensLabelFrame)
añoinicioCuadro.grid(row=9,column=1)
añofinalCuadro=Entry(mensLabelFrame)
añofinalCuadro.grid(row=10,column=1)
mesEscogidoCuadro=Entry(mensLabelFrame)
mesEscogidoCuadro.grid(row=11,column=1)

Label(mensLabelFrame,text="Opción 1").grid(row=9,column=2,sticky="e")
opcionTemp=Radiobutton(mensLabelFrame,text="Temperatura",variable=opcionPrinc,value=1,command=unauotra)
opcionTemp.grid(row=9,column=3,sticky="w")
Label(mensLabelFrame,text="Elegir").grid(row=10,column=2,sticky="e")
Tmin_Chbut=Checkbutton(mensLabelFrame,text="Tmin",variable=Tn,onvalue=1,offvalue=0)
Tmin_Chbut.grid(row=10,column=3,sticky="w")
Tmax_Chbut=Checkbutton(mensLabelFrame,text="Tmax",variable=Tx,onvalue=1,offvalue=0)
Tmax_Chbut.grid(row=11,column=3,sticky="w")
Label(mensLabelFrame,text="Elegir").grid(row=12,column=2,sticky="e")
opcion1Tm=Radiobutton(mensLabelFrame,text="Media",variable=med_extT,value=1)
opcion1Tm.grid(row=12,column=3,sticky="w")
opcion1Te=Radiobutton(mensLabelFrame,text="Extrema",variable=med_extT,value=2)
opcion1Te.grid(row=13,column=3,sticky="w")
Label(mensLabelFrame,text="Valor extremo").grid(row=14,column=2,sticky="e")
opcion2Tmin=Radiobutton(mensLabelFrame,text="Mínimo",variable=min_maxT,value=1)
opcion2Tmin.grid(row=14,column=3,sticky="w")
opcion2Tmax=Radiobutton(mensLabelFrame,text="Máximo",variable=min_maxT,value=2)
opcion2Tmax.grid(row=15,column=3,sticky="w")
grafico2BotonT=Checkbutton(mensLabelFrame,text="Gráfico",variable=graficoT,onvalue=1,offvalue=0)
grafico2BotonT.grid(row=16,column=3,sticky="w")
Label(mensLabelFrame,text="Título").grid(row=17,column=2,sticky="e")
titGraf2T=Entry(mensLabelFrame)
titGraf2T.grid(row=17,column=3)
botonEnvioT=Button(mensLabelFrame,text="Enviar",command=temperatura)
botonEnvioT.grid(row=18,column=3,sticky="w")
borrarEntriesT=Button(mensLabelFrame,text="Borrar",command=borraEntryT)
borrarEntriesT.grid(row=18,column=2,sticky="e")


Label(mensLabelFrame,text="Opción 2").grid(row=12,column=0,sticky="e")
opcionPrec=Radiobutton(mensLabelFrame,text="Precipitaciones",variable=opcionPrinc,value=2,command=unauotra)
opcionPrec.grid(row=12,column=1,sticky="w")
Label(mensLabelFrame,text="Elegir").grid(row=13,column=0,sticky="e")
opcion1Pm=Radiobutton(mensLabelFrame,text="Total",variable=med_extP,value=1)
opcion1Pm.grid(row=13,column=1,sticky="w")
opcion1Pe=Radiobutton(mensLabelFrame,text="Extrema",variable=med_extP,value=2)
opcion1Pe.grid(row=14,column=1,sticky="w")
Label(mensLabelFrame,text="Valor extremo").grid(row=15,column=0,sticky="e")
opcion2Pmin=Radiobutton(mensLabelFrame,text="Mínimo",variable=min_maxP,value=1)
opcion2Pmin.grid(row=15,column=1,sticky="w")
opcion2Pmax=Radiobutton(mensLabelFrame,text="Máximo",variable=min_maxP,value=2)
opcion2Pmax.grid(row=16,column=1,sticky="w")
grafico2BotonP=Checkbutton(mensLabelFrame,text="Gráfico",variable=graficoP,onvalue=1,offvalue=0)
grafico2BotonP.grid(row=17,column=1,sticky="w")
Label(mensLabelFrame,text="Título").grid(row=18,column=0,sticky="e")
titGraf2P=Entry(mensLabelFrame)
titGraf2P.grid(row=18,column=1)
botonEnvioP=Button(mensLabelFrame,text="Enviar",command=precipitaciones)
botonEnvioP.grid(row=19,column=1,sticky="w")
borrarEntriesP=Button(mensLabelFrame,text="Borrar",command=borraEntryP)
borrarEntriesP.grid(row=19,column=0,sticky="e")

#------------------------------Frame 1 - Umbrales---------------------------------------

umbLabelFrame=LabelFrame(miFrame,text="Umbrales",font=("bold","12"),padx=0,pady=0,width="300",height="250")
umbLabelFrame.grid(row=8,column=4,sticky="e")
Label(umbLabelFrame,text="Año inicio").grid(row=9,column=4,sticky="e")
Label(umbLabelFrame,text="Año final").grid(row=10,column=4,sticky="e")
Label(umbLabelFrame,text="Mes").grid(row=11,column=4,sticky="e")
Label(umbLabelFrame,text="Dia inicio").grid(row=9,column=6,sticky="e")
Label(umbLabelFrame,text="Dia final").grid(row=10,column=6,sticky="e")
Label(umbLabelFrame,text="Umbral").grid(row=11,column=6,sticky="e")

añoUmbralCuadro=Entry(umbLabelFrame)
añoUmbralCuadro.grid(row=9,column=5)
añoUmbralCuadrof=Entry(umbLabelFrame)
añoUmbralCuadrof.grid(row=10,column=5)
mesUmbralCuadro=Entry(umbLabelFrame)
mesUmbralCuadro.grid(row=11,column=5)
diaUmbralCuadro=Entry(umbLabelFrame)
diaUmbralCuadro.grid(row=9,column=7)
diaUmbralCuadrof=Entry(umbLabelFrame)
diaUmbralCuadrof.grid(row=10,column=7)
umbralCuadro=Entry(umbLabelFrame)
umbralCuadro.grid(row=11,column=7)

Label(umbLabelFrame,text="Opción 1").grid(row=12,column=4,sticky="e")
opcionTempU=Radiobutton(umbLabelFrame,text="Temperatura",variable=opcionU,value=1,command=unauotra)
opcionTempU.grid(row=12,column=5,sticky="w")
Label(umbLabelFrame,text="Elegir").grid(row=13,column=4,sticky="e")
opcion1TnxU=Radiobutton(umbLabelFrame,text="Tmin",variable=Tmin_Tmax,value=1)
opcion1TnxU.grid(row=13,column=5,sticky="w")
opcion2TnxU=Radiobutton(umbLabelFrame,text="Tmax",variable=Tmin_Tmax,value=2)
opcion2TnxU.grid(row=14,column=5,sticky="w")
Label(umbLabelFrame,text="Elegir").grid(row=15,column=4,sticky="e")
opcion1TUmm=Radiobutton(umbLabelFrame,text="Mayor o igual",variable=May_Men_T,value=1)
opcion1TUmm.grid(row=15,column=5,sticky="w")
opcion2TUmm=Radiobutton(umbLabelFrame,text="Menor o igual",variable=May_Men_T,value=2)
opcion2TUmm.grid(row=16,column=5,sticky="w")
rankingBotonT=Checkbutton(umbLabelFrame,text="Ranking",variable=RankT,onvalue=1,offvalue=0)
rankingBotonT.grid(row=17,column=5,sticky="w")
botonEnvioT=Button(umbLabelFrame,text="Enviar",command=tempU)
botonEnvioT.grid(row=18,column=5,sticky="w")
borrarEntriesTU=Button(umbLabelFrame,text="Borrar",command=borraEntryTU)
borrarEntriesTU.grid(row=19,column=5,sticky="w")


Label(umbLabelFrame,text="Opción 2").grid(row=12,column=6,sticky="e")
opcionPrecU=Radiobutton(umbLabelFrame,text="Precipitaciones",variable=opcionU,value=2,command=unauotra)
opcionPrecU.grid(row=12,column=7,sticky="w")
Label(umbLabelFrame,text="Elegir").grid(row=13,column=6,sticky="e")
opcion1PU=Radiobutton(umbLabelFrame,text="Mayor o igual",variable=May_Men_P,value=1)
opcion1PU.grid(row=13,column=7,sticky="w")
opcion2PU=Radiobutton(umbLabelFrame,text="Menor o igual",variable=May_Men_P,value=2)
opcion2PU.grid(row=14,column=7,sticky="w")
rankingBotonP=Checkbutton(umbLabelFrame,text="Ranking",variable=RankP,onvalue=1,offvalue=0)
rankingBotonP.grid(row=15,column=7,sticky="w")
botonEnvioP=Button(umbLabelFrame,text="Enviar",command=precU)
botonEnvioP.grid(row=16,column=7,sticky="w")
borrarEntriesPU=Button(umbLabelFrame,text="Borrar",command=borraEntryPU)
borrarEntriesPU.grid(row=17,column=7,sticky="w")

#------------------------------Frame 1 - p4---------------------------------------

cuarto_labelframe=LabelFrame(miFrame,text="Información",font=("bold","12"),padx=0,pady=0,width="300",height="250")
cuarto_labelframe.grid(row=0,column=4)

fechas_limites=Label(cuarto_labelframe,textvariable=fechas)
fechas_limites.grid(row=1,column=4,sticky="e")
boton_percentiles=Button(cuarto_labelframe,text="Percentiles 1981-2010",command=calculo_percentiles)
boton_percentiles.grid(row=2,column=4,sticky="w")


#-----------------------------Frame 2 - Despliegue de datos------------------------------------------

miFrame2=Frame(raiz)
miFrame2.pack(fill="both",expand="True",side="right")
miFrame2.config(bg="grey",width="150",height="450",bd=27,relief="groove")

dataText=Text(miFrame2)
dataText.grid(row=0,column=0)
dataText.config(width="30")

scrollVert=Scrollbar(miFrame2,command=dataText.yview)
scrollVert.grid(row=0,column=1,sticky="nsew")
dataText.config(yscrollcommand=scrollVert.set)

minLabel=Label(miFrame2,textvariable=mindata)
minLabel.grid(row=1,column=0,sticky="w")
maxLabel=Label(miFrame2,textvariable=maxdata)
maxLabel.grid(row=2,column=0,sticky="w")

botonBorrar=Button(miFrame2,text="Borrar",command=borrarText)
botonBorrar.grid(row=3,column=0)


raiz.mainloop()
