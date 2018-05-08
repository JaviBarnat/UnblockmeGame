# -*- coding: utf-8 -*-

#Barrientos González, Javier.
#González García, Eduardo.

import pygtk
from gtk._gtk import VBox
pygtk.require('2.0')
import gtk
import random

#Funciones para leer, escribir y analizar las estadísticas, junto a las de leer el fichero niveles.txt

def Matriz(m, hor,fil, col, long, data):
    
    fil = fil - 1
    col = col - 1
    long = long - 1
    
    if hor == 'H':
        m[fil][col] = data
        while long != 0:
            col = col + 1
            m[fil][col] = data
            long = long - 1

    else:
        m[fil][col] = data
        while long != 0:
            fil = fil + 1
            m[fil][col] = data
            long = long - 1

def LeerNivel(num, coches):                 #Funcion para leer el nivel seleccionado
    
    f = open("niveles.txt","r")
    
    f.readline()                            #Sirve para mover el puntero a la segunda linea sin importar el numero de bytes que tenga la primera
    
    
    for i in range(num-1):                  #Da los saltos dentro del fichero para pasar de un nivel a otro
        Saltos = int(f.readline())
        for j in range(Saltos):
            f.readline()
    
    NumCoch = int(f.readline())             #Guarda el numero de coches del nivel
    
    for i in range(NumCoch):
        cadena = f.readline()
        coches[i] = cadena.rstrip("\n")
    
    f.close()
    
def LeerEstadisticas(FEstasts):

    f = open("Estadisticas.txt","r")
    n=0
    
    for i in f:                         #Lee el fichero y lo guarda en un diccionario
        FEstasts[n]=i
        n+=1
        
    f.close()
    
def CrearFicheroEstadisticas():

    f = open("Estadisticas.txt","w")
    
    for j in range(20):                     #Crea un fichero de estadísticas lleno de ceros (20 niveles, 20 ceros)
        f.write('0'+"\n")
    
    f.close()

def GuardarEstadisticas(Nivel,Pasos,FEstasts):   #Guarda los pasos utilizados para terminar un nivel
    
    Pasos = Pasos + 1
    
    FEstasts = {}
    
    f = open("Estadisticas.txt","r")
    n=0
    
    for i in f:                                 #Lee el fichero y lo guarda en un diccionario
        FEstasts[n]=i
        n+=1
        
    if int(FEstasts[int(Nivel)-1]) == 0:            #Comprueba el numero de pasos y lo cambia en caso de ser mejor puntuacion
        FEstasts[int(Nivel)-1]=str(Pasos)+'\n'
    elif int(FEstasts[int(Nivel)-1]) > Pasos:       #Comprueba el numero de pasos y lo cambia en caso de ser mejor puntuacion
        FEstasts[int(Nivel)-1]=''
        FEstasts[int(Nivel)-1]=str(Pasos)+'\n'

    f = open("Estadisticas.txt","w")
    
    for j in FEstasts:                          #Vuelve a Guardar el fichero
        f.write(str(FEstasts[j]))
                
    f.close()
    
def NivelesPermitidos2(N_niveles):      #Analiza cuál es el máximo nivel jugable

    f = open("Estadisticas.txt", "r")       #Abre el fichero de estadísticas existente
    Ceros = 0
    Niveles = 1

    for i in f:                             #Leemos el fichero y devolvemos el valor de la posición del primer cero, más uno.
        if int(i) == 0:
            Ceros += 1
        if Ceros == 0 and Niveles < N_niveles:
            Niveles += 1
      
    return Niveles

#El juego en sí y sus caracteristicas
     
class Juego:
    
    #Colocamos las varibles que serán usadas a lo largo de todo el código, para no repetirlas por todo el código
    #Dichas variables presentan el valor 0 o vacío, para luego escribir sobre ellas o modificarlas sin que su valor afecte
    
    nivel = '0'
    arrastrando = False
    x0=0
    y0=0
    FEstasts = {}
    m = []
    
    #Leemos el archivo de estadísticas. Si este no existe, se crea uno
    
    try:
        LeerEstadisticas(FEstasts)
    except:
        CrearFicheroEstadisticas()
        LeerEstadisticas(FEstasts)
        
    #Inicio de la pantalla de selección de nivel
    
    def __init__(self):
        
        #Leemos las estadísticas y analizamos el nivel máximo jugable, y lo imprimimos por pantalla
        
        LeerEstadisticas(self.FEstasts)
        nivelesPosibles = NivelesPermitidos2(20)
        
        #Creación de la ventana con el título
        self.ventana = gtk.Window()
        self.ventana.set_icon_from_file('data/UnblockMe.png')
        self.ventana.size_request()
        self.ventana.set_resizable(False)
        self.ventana.set_title('Desbloquea')
        self.ventana.connect("destroy", gtk.main_quit)
        
        #Crear caja vertical
        cajaV = gtk.VBox()
        
        #Crear label (titulo de bienvenida más el nivel máximo jugable)
        titulo = gtk.Label('\n\nSeleccione un nivel. Niveles disponibles: '+str(nivelesPosibles)+'\n\n')
        cajaV.add(titulo)
        
        #Crear caja horizontal
        cajaH = gtk.HBox()
        
        #Crear imagen inicial
        imagenCoche = gtk.Image()
        imagenCoche.set_from_file("data/inicio.png")
        cajaV.add(imagenCoche)
        
        #Menu_Desplegable (todos los niveles presentes)
        
        self.combo = gtk.Combo()
        slist = ["01", "02", "03", "04", '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
        self.combo.set_popdown_strings(slist)
        self.combo.set_use_arrows(False)
        cajaV.add(self.combo)
        
        #Boton aceptar (ejecuta la ventana de juego, con el nivel previamente seleccionado en la lista desplegable)
        
        boton2 = gtk.Button('Aceptar')
        boton2.set_size_request(100,30)
        boton2.connect('clicked', self.Adelante)
        cajaH.add(boton2)
        
        #Boton salir (ejecuta el cierre completo del programa)
        
        botonE = gtk.Button('Salir')
        botonE.set_size_request(100,30)
        botonE.connect('clicked', self.CerrarTodo)
        cajaH.add(botonE)
        
        cajaV.add(cajaH)
        
        #Boton para borrar estadísticas (ejecuta la creación de un nuevo archivo de estadisticas, con todo a cero)
        
        botonEstadisticas = gtk.Button('Borrar estadísticas')
        botonEstadisticas.set_size_request(100,30)
        botonEstadisticas.connect('clicked', self.BorrarEst)
        cajaV.add(botonEstadisticas)
        
        self.ventana.add(cajaV)
        self.ventana.show_all()
        
    #Inicio de la pantalla de juego principal
       
    def Adelante(self, widget):
        
        LeerEstadisticas(self.FEstasts)
        
        #Creamos una matriz donde guardar la posicion de los coches, para usarla mas adelante con el fin de analizar los movimientos
        #y las posiciones vacías
                 
        self.m = []
        for i in range(6):
            self.m.append([])
            for j in range(7):
                self.m[i].append('69')
        
        self.coches = {}

        self.cont = 0

        #Leemos el nivel introducido por lista

        self.nivel = self.combo.entry.get_text()
        
        #Calculamos el número máximo posible y lo comparamos con el número introducido
        
        maximo = NivelesPermitidos2(20)
        
        if maximo < 10:
            maximo = '0'+str(maximo)
        else:
            maximo = maximo

        #Si el número es incorrecto, y o inválido, se abre una ventana de error

        if (self.nivel < '01' or self.nivel > str(maximo)):
            
            #Ventana de error
            
            Caja = gtk.VBox()
            self.ventanaE = gtk.Window()
            self.ventanaE.set_default_size(600,50)
            self.ventanaE.set_resizable(False)
            self.ventanaE.set_icon_from_file('data/UnblockMe.png')
            self.ventanaE.set_title('Error')
            
            #Mensaje de error junto al botón para cerrar la pantalla
            
            error = gtk.Label('El número introducido es incorrecto. Nivel bloqueado. Por favor, inserte otro número.')
            error.set_size_request(600,40)
            Caja.add(error)
            
            boton_exit = gtk.Button('OK')
            boton_exit.set_size_request(600,40)
            boton_exit.connect_object('clicked', gtk.Widget.destroy, self.ventanaE)
            Caja.add(boton_exit)
            
            self.ventanaE.add(Caja)
            self.ventanaE.show_all()
        
        #En cambio, si el nivel es correcto, se abre la ventana de juego
        
        else:
            
            LeerNivel(int(self.nivel), self.coches)
            
            #Ocultamos la ventana del menú, para evitar problemas a la hora de seleccionar varios niveles
            
            self.ventana.hide()
            
            #Creación de la ventana
            
            self.ventanaJuego = gtk.Window()
            self.ventanaJuego.set_icon_from_file('data/UnblockMe.png')
            self.ventanaJuego.set_default_size(700,700)
            self.ventanaJuego.set_resizable(False)
            self.ventanaJuego.set_title('Desbloquea - Nivel: ' + self.nivel)
            self.ventanaJuego.connect("destroy", self.volverMenu)          

            cajaTodo = VBox()

            #Creación del fixed, el contenedor principal de los coches

            self.fixed = gtk.Fixed()
            cajaTodo.add(self.fixed)
            
            #Elección aleatoria entre varios fondos para el juego
            
            fondos = ['data/fondo1.png', 'data/fondo2.png', 'data/fondo3.png']
            
            imagenFondo = gtk.Image()
            imagenFondo.set_from_file(fondos[random.randrange(3)])
            imagenFondo.show()
            self.fixed.add(imagenFondo)
            
            self.fixed.show()
      
            C = self.coches.values()
            NumCoch = len(C)

            #Creación de las eventboxes de los coches, con sus caracteristicas y sus imágenes, también escogidas de manera aleatoria
            #Colocación de las eventboxes en el fixed. Guardamos los valores en la matriz para la ayuda con los movimientos.
            
            for i in range(NumCoch):

                self.caja = gtk.EventBox()
                self.caja.set_visible_window(False)
                self.caja.show()
                
                dataCoche = self.coches[i]
                hor = dataCoche[0]
                col = int(dataCoche[1])
                fil = int(dataCoche[2])
                long = int(dataCoche[3])
                
                self.caja.set_events(gtk.gdk.BUTTON_PRESS_MASK | gtk.gdk.BUTTON_RELEASE_MASK | gtk.gdk.POINTER_MOTION_MASK)     
                self.caja.connect("button_press_event", self.evento_pulsar, i)     
                self.caja.connect("button_release_event", self.evento_soltar, i)   
                self.caja.connect("motion_notify_event", self.evento_arrastrar, i)
                
                if hor == 'H':
                    
                    if long == 2:
                        
                        cochesHorizontales = ['data/Coche1H.png','data/Coche2H.png','data/Coche3H.png','data/Coche4H.png','data/Coche5H.png','data/Coche6H.png']
                        
                        imagenCH = gtk.Image()
                        imagenCH.show()
                        if i == 0:
                            imagenCH.set_from_file('data/CocheSalir.png')
                        else:
                            imagenCH.set_from_file(cochesHorizontales[random.randrange(6)])
                        self.caja.add(imagenCH)
                        
                        Matriz(self.m, hor, fil, col, long, i)

                        self.fixed.put(self.caja, (col*100)-100, (fil*100)-100)
                        
                    else:
                        
                        camionesHorizontales = ['data/Camion1H.png', 'data/Camion2H.png']
                        
                        imagenCH = gtk.Image()
                        imagenCH.show()
                        imagenCH.set_from_file(camionesHorizontales[random.randrange(2)])
                        self.caja.add(imagenCH)

                        Matriz(self.m, hor, fil, col, long, i)

                        self.fixed.put(self.caja, (col*100)-100, (fil*100)-100)

                        imagenCH.show()
                        
                                            
                        imagenCH.show()
                
                else:
                     
                    if long == 2: 
                        
                        cochesVerticales = ['data/Coche1V.png','data/Coche2V.png','data/Coche3V.png','data/Coche4V.png','data/Coche5V.png','data/Coche6V.png']
                                      
                        imagenCV = gtk.Image()
                        imagenCV.show()
                        imagenCV.set_from_file(cochesVerticales[random.randrange(6)])
                        self.caja.add(imagenCV)
                        
                        Matriz(self.m, hor, fil, col, long, i)

                        self.fixed.put(self.caja, (col*100)-100, (fil*100)-100)

                        imagenCV.show()
                        
                    else:
                        
                        camionesVerticales = ['data/Camion1V.png', 'data/Camion2V.png']
                        
                        imagenCV = gtk.Image()
                        imagenCV.show()
                        imagenCV.set_from_file(camionesVerticales[random.randrange(2)])
                        self.caja.add(imagenCV)
                        
                        Matriz(self.m, hor, fil, col, long, i)

                        self.fixed.put(self.caja, (col*100)-100, (fil*100)-100)

                        imagenCV.show()
                        
            cajaH = gtk.HBox()
            
            #Botón para ejecutar el cierre de la ventana de juego y para volver a abrir el selector de niveles (menú)
            
            boton_menu = gtk.Button('Menú')
            boton_menu.set_size_request(100,60)
            boton_menu.connect('clicked', self.volverMenu2)
            cajaH.add(boton_menu)
            
            #Botón para cerrar la ventana de juego actual y volver a abrir el mismo nivel, pero con los movimientos eliminados
            
            boton_retry = gtk.Button('Retry')
            boton_retry.set_size_request(100,60)
            boton_retry.connect('clicked', self.reintentar)
            cajaH.add(boton_retry)
            
            #Impresión por pantalla del nivel presente, los pasos actuales y el récord de dicho nivel
            
            self.contador_record = gtk.Label('\nNivel: '+str(self.nivel)+'\nPasos realizados hasta el momento: ' + str(self.cont)+'\nRécord: '+ self.FEstasts[int(self.nivel)-1])
            self.contador_record.set_size_request(100, 80)
            cajaH.add(self.contador_record)
            
            cajaTodo.add(cajaH)
            
            self.ventanaJuego.add(cajaTodo)
            cajaTodo.show_all()
            self.ventanaJuego.show()  
        
    def evento_pulsar(self, widget, event, data):    
        
        #Distinguimos arrastrar de mover el ratón, y obtenemos las coordenadas relativas
        
        self.arrastrando = True     
        self.x0 = int(event.x_root)     
        self.y0 = int(event.y_root)
        
        self.derecha = 0
        self.izquierda = 0
        self.up = 0
        self.down = 0
        
        #Con el dato del coche pasado por 'data', desglosamos sus valores (los del fichero) para su futura utilización
        
        movCoche = self.coches[data]
        movhor = movCoche[0]
        movcol = int(movCoche[1])
        movfil = int(movCoche[2])
        movlong = int(movCoche[3])
        
        #Obtenemos la posición del puntero donde se ha hecho 'click'
        
        self.xInicio = (widget.allocation.x)
        self.yInicio = (widget.allocation.y)
        
        elLimite = False
        
        #Diferenciamos si el coche es horizontal o vertical
        
        #Horizontal (establecemos los límites posibles del coche)
        
        if movhor == 'H':
            j = self.xInicio/100
            i = self.yInicio/100
            
            while(j < 6 and elLimite == False):
                if(self.m[i][j] != data and self.m[i][j] != '69'):
                    elLimite = True
                    self.derecha = j*100
                    
                j = j + 1
                
            if(elLimite == False):
                self.derecha = 6*100
                
            j = self.xInicio/100
            elLimite = False
            
            while(j > -1 and elLimite == False):
                if(self.m[i][j] != data and self.m[i][j] != '69'):
                    elLimite = True
                    self.izquierda = (j+1)*100
                j = j - 1
                
            if(elLimite == False):
                self.izquierda = 0
                
            if(data == 0 and self.derecha == 6*100):
                self.derecha = 7*100

        #Vertical (establecemos los límites posibles del coche)

        else:
            j = self.xInicio/100
            i = self.yInicio/100
            
            while(i < 6 and elLimite == False):
                if(self.m[i][j] != data and self.m[i][j] != '69'):
                    elLimite = True
                    self.down = i*100
                    
                i = i + 1
                
            if(elLimite == False):
                self.down = 6*100
                
            i = self.yInicio/100
            elLimite = False
            
            while(i > -1 and elLimite == False):
                if(self.m[i][j] != data and self.m[i][j] != '69'):
                    elLimite = True
                    self.up = (i+1)*100
                i = i - 1
                
            if(elLimite == False):
                self.up = 0  
        
        return gtk.TRUE   
    
    def evento_arrastrar(self, widget, event, data):    
        
        #Para distinguir arrastrar de mover el ratón
        
        if not self.arrastrando:       
            return gtk.FALSE

        #Volvemos a analizar el coche, según el dato en 'data'

        movCoche = self.coches[data]
        movhor = movCoche[0]
        movcol = int(movCoche[1])
        movfil = int(movCoche[2])
        movlong = int(movCoche[3])

        #Obtención del desplazamiento del coche

        dx = int(event.x_root) - self.x0
        dy = int(event.y_root) - self.y0
        
        self.Inicioxy = self.xInicio+dx
        self.Inicioyx = self.yInicio+dy
        
        finalx = (self.xInicio+movlong*100)+dx
        finaly = (self.yInicio+movlong*100)+dy
        
        #Analizamos los límites según la matriz, donde han sido colocados los coches anteriormente
        
        #Si el coche es horizontal
        
        if movhor == 'H':
            
            if dx>0:
                if finalx >= self.derecha:
                    self.fixed.move(widget, self.derecha-movlong*100, self.yInicio)
                else:
                    self.fixed.move(widget, self.Inicioxy, self.yInicio)
                    
            else:
                if self.Inicioxy <= self.izquierda:
                    self.fixed.move(widget, self.izquierda, self.yInicio)
                else:
                    self.fixed.move(widget, self.Inicioxy, self.yInicio)
        
        #Si el coche es vertical
                   
        else:
            if dy>0:
                if finaly >= self.down:
                    self.fixed.move(widget, self.xInicio, self.down-movlong*100)
                else:
                    self.fixed.move(widget, self.xInicio, self.Inicioyx)
                    
            elif dy<=0:
                if self.Inicioyx <= self.up:
                    self.fixed.move(widget, self.xInicio, self.up)
                else:
                    self.fixed.move(widget, self.xInicio, self.Inicioyx)
            
        return gtk.TRUE   
    
    def evento_soltar(self, widget, event, data):     
        
        #Para distinguir arrastrar de mover el ratón
        
        self.arrastrando = False    
        dx = int(event.x_root) - self.x0
        dy=  int(event.y_root) - self.y0
        
        #Valores para la matriz a cambiar
        
        newIniciox = int(widget.allocation.x/100)
        newInicioy = int(widget.allocation.y/100)
        
        #Último análisis del coche seleccionado
        
        movCoche = self.coches[data]
        movhor = movCoche[0]
        movcol = int(movCoche[1])
        movfil = int(movCoche[2])
        movlong = int(movCoche[3])
        
        #Observamos si el movimiento ha sido horizontal o vertical, y si se ha movido, cambiamos el valor de las posiciones de la matriz
        #donde se encontraba el coche por el número nulo o vacío (69) y colocamos en su nueva posición el valor de 'data' (número del coche)
        
        if movhor == 'H':
            if dx < 0:
                i = newInicioy
                j = 0

                while(j < 6):
                    if self.m[i][j] == data:
                        self.m[i][j] = '69'
                        
                    j = j + 1
                    
                j = newIniciox
                while (movlong != 0):
                    self.m[i][j] = data
                    j = j + 1
                    movlong = movlong - 1
                    
                j = 0
                while(j<6):
                    if(self.m[i][j] == data):
                        self.fixed.move(widget, newIniciox*100, i*100)
                    j = j + 1
                    
            elif(dx > 0):
                i = newInicioy
                j = 0
                
                while(j < 6):
                    if self.m[i][j] == data:
                        self.m[i][j] = '69'
                    j = j + 1
                        
                newIniciox = newIniciox + 1
                j = newIniciox
                
                newFinalx = newIniciox + movlong
                
                if newFinalx > self.derecha/100:
                    newIniciox = newIniciox - 1
                    j = newIniciox
                
                #Si el coche presente al final es el coche '0', es decir, el coche a salir, y su valor de columna final es mayor que 6
                #activamos la ventana de victoria
                   
                if (data == 0 and newIniciox+movlong > 6):
                    self.VentanaNewLevel(widget)
                    
                else:
                    while movlong != 0:
                        self.m[i][j] = data
                        j = j + 1
                        movlong = movlong - 1
                        
                self.fixed.move(widget, newIniciox*100, i*100)
                
        elif movhor == 'V':
            if dy < 0:
                i = 0
                j = newIniciox

                while(i < 6):
                    if self.m[i][j] == data:
                        self.m[i][j] = '69'
                        
                    i = i + 1
                    
                i = newInicioy
                while (movlong != 0):
                    self.m[i][j] = data
                    i = i + 1
                    movlong = movlong - 1
                    
                i = 0
                while(i<6):
                    if(self.m[i][j] == data):
                        self.fixed.move(widget, j*100, newInicioy*100)
                    i = i + 1
                    
            elif(dy > 0):
                i = 0
                j = newIniciox
                
                while(i < 6):
                    if self.m[i][j] == data:
                        self.m[i][j] = '69'
                    i = i + 1
                        
                newInicioy = newInicioy + 1
                i = newInicioy
                
                newFinaly = newInicioy + movlong
                
                if newFinaly > self.down/100:
                    newInicioy = newInicioy - 1
                    i = newInicioy
                    
                while movlong != 0:
                    self.m[i][j] = data
                    i = i + 1
                    movlong = movlong - 1
                        
                self.fixed.move(widget, j*100, newInicioy*100)
        
        #Se suma uno al contador de pasos y se saca por pantalla su valor, actualizado en cada momento
        
        self.cont = self.cont + 1
        self.contador_record.set_text('\nNivel: '+str(self.nivel)+'\nPasos realizados hasta el momento: ' + str(self.cont)+'\nRécord: '+ self.FEstasts[int(self.nivel)-1])        
        
        return gtk.TRUE
    
    def VentanaNewLevel(self, widget):
        
        #Comprobamos el número de pasos hechos con el número de pasos presentes en el fichero, lo guardamos y volvemos a leer el fichero de estadisticas
        
        GuardarEstadisticas(self.nivel, self.cont, self.FEstasts)
        LeerEstadisticas(self.FEstasts)
        
        #Eliminamos la ventana del juego, provocando la aparición del menú, de nuevo
        
        self.ventanaJuego.destroy()
        
        Caja = gtk.VBox()
        
        #Creación de la ventana de victoria
        
        self.ventanaFin = gtk.Window()
        self.ventanaFin.set_icon_from_file('data/UnblockMe.png')
        self.ventanaFin.set_default_size(400,150)
        self.ventanaFin.set_resizable(False)
        self.ventanaFin.set_title('Nivel completado')
        self.ventanaFin.connect("destroy", gtk.Widget.destroy)
        
        #Mensaje de victoria, junto a los pasos realizados, el récord y una imagen 'graciosa'
        
        fin = gtk.Label('\nEnhorabuena, nivel completado.\n\nPasos realizados: ' + str(self.cont + 1)+'\nRécord: '+ self.FEstasts[int(self.nivel)-1])
        fin.set_size_request(100,100)
        Caja.add(fin)
        
        imagenEnhorabuena = gtk.Image()
        imagenEnhorabuena.set_from_file("data/tanqueEn.png")
        Caja.add(imagenEnhorabuena)
        
        self.ventanaFin.add(Caja)
        self.ventanaFin.show_all()
        
    def CerrarTodo(self, widget):   #Cierra el programa python por completo
        gtk.main_quit()
        
    def volverMenu(self, event):    #Vuelve a abrir menú inicial
        self.__init__()

    def volverMenu2(self, event):   #Oculta la ventana de juego actual y vuelve a abrir el menú inicial
        self.ventanaJuego.hide()
        self.__init__()

    def reintentar(self, event):    #Oculta la ventana de juego actual y vuelve a cargar el nivel actual al que se estaba jugando
        self.ventanaJuego.hide()
        self.Adelante(self)
    
    def BorrarEst(self, event):     #Se vuelve a crear un fichero de estadísticas vacío, ocultando la ventana de inicio y volviendo a abrirla
        CrearFicheroEstadisticas()  #para observar el cambio en el número de niveles disponibles
        self.ventana.hide()
        self.__init__()

#Inicio completo
      
Juego()
gtk.main()     