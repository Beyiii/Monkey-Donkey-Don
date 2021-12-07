
# Con este codigo el monito es capás de trepar plataformas cuyas posiciones están dado
# por un archivo csv


import glfw
import OpenGL.GL.shaders

from Plataformas import *


# Clase que almacena el control de la aplicación (control aplication)
class Controller:
    def __init__(self):
        self.x = 0.0
        self.y = -0.675
        self.j = 0.0
        self.rightOn  = False
        self.leftOn  = False
        self.upOn = False

# Controlador global como comunicación con la función de devolución de llamada (callback function)
controller = Controller()


# Función que sirve para colocar el funcionamiento de las teclas a ocupar
def on_key(window, key, scancode, action, mods):

    global controller

    if action == glfw.PRESS:
        
        if key == glfw.KEY_D:
            controller.rightOn = True

        elif key == glfw.KEY_A:
            controller.leftOn = True

        elif key == glfw.KEY_W:
            controller.upOn = True

        elif key == glfw.KEY_ESCAPE:
            sys.exit()

        else:
            print('Unknown key')

    elif (action ==glfw.RELEASE):
        if key == glfw.KEY_D:
            controller.rightOn = False

        elif key == glfw.KEY_A:
            controller.leftOn = False

# True si el monito choca con la plataforma que está arriba
def colision(x, y, j, a=A, b=B):
    n = len(A)
    for i in range(n):
        if A[i] - 0.35 <= x <= A[i] + 0.35 and B[i] + j > y >= B[i] - 0.2 + j:
            return True

        if y < B[i] - 0.2 + j:
            return False

# True si el monito está sobre una plataforma        
def enPlataforma(x, y, j, a=A, b=B):
    n = len(A)
    for i in range(n):
        if A[i] - 0.35 <= x <= A[i] + 0.35 and B[i] + 0.21 + j < y <= B[i] + 0.23 + j:
            return True


    
    
# Acá se pone las caracteristicas de la ventana, el nombre, los elementos que habrán, entre otras cosas
if __name__ == "__main__":

    # Inicializar glfw
    if not glfw.init():
        sys.exit()

    width = 650
    height = 650

    window = glfw.create_window(width, height, "Monkey Donkey Don!", None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    # Conexión de la función callback 'on_key' para manejar eventos de teclado
    glfw.set_key_callback(window, on_key)
    
    # Un programa de sombreado simple con coordenadas de posición y textura como entradas.
    pipeline = es.SimpleTextureTransformShaderProgram()
    
    # Decir a OpenGL que use nuestro progama de sombreado
    glUseProgram(pipeline.shaderProgram)

    # Configurar el color de la pantalla
    glClearColor(0.522, 0.643, 1.0, 1.0)

    # Habilitación de transparencias
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Creando shapes en la memoria de la GPU
    gpuMonitoSaltando = es.toGPUShape(bs.createTextureQuad("Saltando1.png"), GL_REPEAT, GL_NEAREST)
    gpuMonitoEstaticoUP = es.toGPUShape(bs.createTextureQuad("MonitoArriba.png"), GL_REPEAT, GL_NEAREST)
    gpuMonitoEstaticoDOWN = es.toGPUShape(bs.createTextureQuad("MonitoAbajo.png"), GL_REPEAT, GL_NEAREST)
    gpuMonitoCorrer1 = es.toGPUShape(bs.createTextureQuad("Correr1.png"), GL_REPEAT, GL_NEAREST)
    gpuMonitoCorrer2 = es.toGPUShape(bs.createTextureQuad("Correr2.png"), GL_REPEAT, GL_NEAREST)
    gpuMonitoCorrer3 = es.toGPUShape(bs.createTextureQuad("Correr3.png"), GL_REPEAT, GL_NEAREST)
    gpuMonitoCorrer4 = es.toGPUShape(bs.createTextureQuad("Correr4.png"), GL_REPEAT, GL_NEAREST)
    gpuMonitoCorrer5 = es.toGPUShape(bs.createTextureQuad("Correr5.png"), GL_REPEAT, GL_NEAREST)
    gpuMonitoCorrer6 = es.toGPUShape(bs.createTextureQuad("Correr6.png"), GL_REPEAT, GL_NEAREST)
    gpuSadMonito = es.toGPUShape(bs.createTextureQuad("SadMonito.png"), GL_REPEAT, GL_NEAREST)
    
    
    # Plataformas
    plataformas = PlataformaCreator()

    # CREAR PLATAFORMAS
    plataformas.create_plataforma()

    # PASTITO
    pasto = Pastito()

    # BANANAS
    bananas = Bananas()

    # WIN
    win = Win()

    # GAME OVER
    gameover = GameOver()

    # Booleanos
    bajada = False
    bajada2 = False
    sobrePlataforma = False
    direccion = True
    puasOn = False
    WIN = False
    perder = False
    subida = True
    
    # Variables para los sprites
    contar = 2
    p = 2

    # Variables para cuando el monito salta
    contar2 = 0
    contar3 = 0
    
    # En este ciclo se coloca lo que harán las figuras
    while not glfw.window_should_close(window):
        # Usa GLFW para verificar eventos de entrada/ esto va para todo
        glfw.poll_events()

        # Limpia la pantalla tanto en color como en profundidad
        glClear(GL_COLOR_BUFFER_BIT)

        # Dirección del monito
        if direccion == True:                
            reflex = tr.identity()

        if direccion == False:
            reflex = tr.scale(-1, 1, 1)

        # DIBUJAR PASTITO

        pasto.draw(pipeline)
        
        # Matriz del monito 
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
            tr.translate(controller.x, controller.y, 0),
            tr.uniformScale(0.35),
            reflex]))

        # Funciones booleanas
        c = colision(controller.x, controller.y, controller.j)         # False 
        plat = enPlataforma(controller.x, controller.y, controller.j)  # False


        # Para ir a la derecha
        if controller.rightOn and controller.upOn == False and perder != True:
            direccion = True 
            contar += 0.06
            
            if controller.x >= 0.880:
                controller.x

            if controller.x < 0.880:
                controller.x += 0.003

            if contar <= p:
                pipeline.drawShape(gpuMonitoCorrer1)

            if p < contar <= p * 2:
                 pipeline.drawShape(gpuMonitoCorrer2)
            
            if p * 2 < contar <= p * 3:
                pipeline.drawShape(gpuMonitoCorrer3)

            if p * 3 < contar <= p * 4:
                pipeline.drawShape(gpuMonitoCorrer4)

            if p * 4 < contar <= p * 5:
                pipeline.drawShape(gpuMonitoCorrer5)

            if p * 5 < contar <= p * 6:
                pipeline.drawShape(gpuMonitoCorrer6)

            if p * 6 < contar <= p * 7:
                pipeline.drawShape(gpuMonitoCorrer6)
                contar = 0

        # Para ir a la izquierda
        if controller.leftOn and controller.upOn == False and perder != True:
            direccion = False
            contar += 0.06

            if controller.x <= -0.880:
                controller.x

            if controller.x > -0.880 and perder != True:
                controller.x -= 0.003           

            if contar <= p:
                pipeline.drawShape(gpuMonitoCorrer1)

            if p < contar <= p * 2:
                 pipeline.drawShape(gpuMonitoCorrer2)
            
            if p * 2 < contar <= p * 3:
                pipeline.drawShape(gpuMonitoCorrer3)

            if p * 3 < contar <= p * 4:
                pipeline.drawShape(gpuMonitoCorrer4)

            if p * 4 < contar <= p * 5:
                pipeline.drawShape(gpuMonitoCorrer5)

            if p * 5 < contar <= p * 6:
                pipeline.drawShape(gpuMonitoCorrer6)

            if p * 6 < contar <= p * 7:
                pipeline.drawShape(gpuMonitoCorrer6)
                contar = 0

        # PARA SALTAR CUANDO ESTÁ EN EL PISO
        if controller.upOn == True and sobrePlataforma == False and perder != True: 
            pipeline.drawShape(gpuMonitoSaltando)
            
            if bajada == False:
                controller.y += 0.003
                controller.j -= 0.003
                pasto.y -= 0.003
                bananas.j -= 0.003
                plataformas.posJ(-0.003)
                if controller.rightOn == True:
                    direccion = True
                    if controller.x >= 0.880:
                        controller.x
                    if controller.x < 0.880:
                        controller.x += 0.005
                if controller.leftOn == True:
                    direccion = False
                    if controller.x <= -0.880:
                        controller.x
                    if controller.x > -0.880:
                        controller.x -= 0.005                    

            if bajada == True:
                controller.y -= 0.003
                pasto.y += 0.003
                controller.j += 0.003
                bananas.j += 0.003
                plataformas.posJ(0.003)
                if controller.rightOn == True:
                    direccion = True
                    if controller.x >= 0.880:
                        controller.x
                    if controller.x < 0.880:
                        controller.x += 0.005
                if controller.leftOn == True:
                    direccion = False
                    if controller.x <= -0.880:
                        controller.x
                    if controller.x > -0.880:
                        controller.x -= 0.005                    

            if controller.y >= -0.1 or c == True:
                bajada = True
                
            if bajada == True and plat == True:
               sobrePlataforma = True 
               bajada = False
               controller.upOn = False
        
                
            if controller.y == -0.675:
                sobrePlataforma = False
                bajada = False
                controller.upOn = False
        
     

        # PARA SALTAR CUANDO ESTÁ EN PLATAFORMAS
        if controller.upOn == True and sobrePlataforma == True and perder != True:
            pipeline.drawShape(gpuMonitoSaltando)
            
            
            if bajada2 == False:
                contar2 += 1 
                controller.j -= 0.006
                pasto.y -= 0.006
                bananas.j -= 0.006
                plataformas.posJ(-0.006)
                if controller.rightOn == True:
                    direccion = True
                    if controller.x >= 0.880:
                        controller.x
                    if controller.x < 0.880 and WIN != True:
                        controller.x += 0.005
                if controller.leftOn == True:
                    direccion = False
                    if controller.x <= -0.880:
                        controller.x
                    if controller.x > -0.880 and WIN != True:
                        controller.x -= 0.005              

            if bajada2 == True:
                contar2 = 0
                controller.j += 0.006
                pasto.y += 0.006
                bananas.j += 0.006
                plataformas.posJ(0.006)
                if controller.rightOn == True:
                    direccion = True
                    if controller.x >= 0.880:
                        controller.x
                    if controller.x < 0.880 and WIN != True:
                        controller.x += 0.005
                if controller.leftOn == True:
                    direccion = False
                    if controller.x <= -0.880:
                        controller.x
                    if controller.x > -0.880 and WIN != True:
                        controller.x -= 0.005 

            if contar2 == 164 or c == True:
                bajada2 = True
                
            if bajada2 == True and plat == True:
               bajada2 = False
               controller.upOn = False 
                
            if pasto.y >= -0.348 :
                bajada2 = False
                controller.upOn = False

            
    
        if plat is not True and contar2 == 0 and sobrePlataforma == True:
            if pasto.y < -0.357:
                controller.upOn = True
                bajada2 = True
            if pasto.y >= -0.357:
                sobrePlataforma = False
                controller.upOn = True 
                bajada = True                
    
        #----------------------------------------
        t = glfw.get_time()
        tiempo = int(t)

        u = "{0:.2f}".format(t)
        temp = float(u)
        a = temp - tiempo
        lel = "{0:.1f}".format(a)
        owo = float(lel)
        #--------------------------------------
        
        # Bananas moviendose
        ty = 0.03 * np.sin(5 * t)

        # Bananas en la ultima plataforma
        n = len(A)- 1
        bananas.y = B[n] + 0.2 + ty
        bananas.x = A[n]
        bananas_y = B[n] + 0.2 + bananas.j

        if bananas.x - 0.1 < controller.x < bananas.x + 0.1 and bananas_y - 0.1 < controller.y < bananas_y + 0.1 :
            WIN = True
            controller.upOn = True


        if sobrePlataforma == True:
            puasOn = True
            pasto.j = -0.905

        if puasOn == True and controller.y == -0.675:
            perder = True

    
        # Monito en su lugar        
        if controller.upOn == False and controller.rightOn == False and controller.leftOn == False and perder == False:
            if owo <= 0.5:
                pipeline.drawShape(gpuMonitoEstaticoDOWN)
                    
            else:
                pipeline.drawShape(gpuMonitoEstaticoUP)

        # DIBUJAR LAS PLATAFORMAS

        plataformas.draw(pipeline)

        # DIBUJAR BANANAS

        bananas.draw(pipeline)

        # DIBUJAR WIN
        if owo <= 0.5:
            win.reflexT = 0.05
            win.reflexS = -2

        if owo > 0.5:
            win.reflexT = 0
            win.reflexS = 2            
        if WIN == True:
            if win.y == 0.0:
                win.Bajando(0.0)

            if win.y > 0.0:
                win.Bajando(0.001)
            
            win.draw(pipeline)

        # DIBUJAR GAME OVER
        if perder == True:
            glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, tr.matmul([
                tr.translate(controller.x, controller.y, 0),
                tr.uniformScale(0.35),
                reflex]))
            
            pipeline.drawShape(gpuSadMonito)
            

            if subida == True:
                controller.y += 0.003

            if subida == False:
                controller.y -= 0.003

            if controller.y >= -0.3:
                subida = False

            if controller.y <= -1.5:
                controller.y = -1.5

            if controller.y == -1.5:
                gameover.draw(pipeline)


        

        # Una vez que se realiza el renderizado, los búferes se intercambian, mostrando solo la escena completa.
        glfw.swap_buffers(window)

    glfw.terminate()
    
    



        



        
