import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es
import numpy as np
import sys
import csv


from OpenGL.GL import *



# Archivo csv y funciones con el
v = sys.argv[1] # Esto es para llamarlo por cmd

def listaC(v):                  
    with open(v) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        c = []
        for row in csv_reader:
            for i in row:
                j = int(i)
                c.append(j)
    return c

C = listaC(v) # lista que contiene cual plataforma se dibuja (1), y cual no(0)

def rows(v):
    with open(v) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            line_count += 1
    return line_count * 3

r = rows(v) #retorna el numero de filas * 3

def listaA(r):
    rows = r
    a = []
    x = [-0.7, 0.0, 0.7]
    while not rows==0:
        a.append(x[0])
        a.append(x[1])
        a.append(x[2])
        rows -=3
    return a

listaA = listaA(r) # lista que contiene la posicion en x de las plataformas

def listaB(r):
    rows = r                  # r sale de row 
    b = []
    y = -0.2
    while not rows==0:
        b.append(y)
        b.append(y)
        b.append(y)
        rows -= 3
        y += 0.7
    return b

listaB = listaB(r) # lista qe contiene la posicion en y de las plataformas

def listaABC(c,x):
    L = []
    n = len(c)
    for i in range(n):
        if c[i] == 1:
            L.append(x[i])
    return L    

A = listaABC(C,listaA)
B = listaABC(C,listaB)
        
class Plataforma(object):

    def __init__(self, posX=0.0, posY=0.0):
        gpuPlataforma = es.toGPUShape(bs.createTextureQuad("Pastito.png",5,1), GL_REPEAT, GL_NEAREST)

        plataforma = sg.SceneGraphNode('plataforma')
        plataforma.transform = tr.scale(0.5, 0.1, 1)
        plataforma.childs += [gpuPlataforma]

        plataforma_tr = sg.SceneGraphNode('plataformaTR')
        plataforma_tr.childs += [plataforma]

        self.pos_x = posX  
        self.pos_y = posY
        self.model = plataforma_tr

    def draw(self, pipeline):
        self.model.transform = tr.translate(self.pos_x, self.pos_y, 0)
        sg.drawSceneGraphNode(self.model, pipeline, "transform")

    def posJ(self, y):
        self.pos_y += y

class PlataformaCreator(object):
    def __init__(self):
        self.plataformas = []

    def create_plataforma(self, a=A, b=B):
        n = len(a)
        for i in range(n):
            self.plataformas.append(Plataforma(A[i],B[i]))

    def draw(self, pipeline):
        for k in self.plataformas:
            k.draw(pipeline)

    def posJ(self, j):
        for k in self.plataformas:
            k.posJ(j)
 
            

class Pastito(object):
    def __init__(self):
        gpuPastito = es.toGPUShape(bs.createTextureQuad("Pastito.png",15,1), GL_REPEAT, GL_NEAREST)
        gpuPuas = es.toGPUShape(bs.createTextureQuad("PastitoPuas.png",15,1), GL_REPEAT, GL_NEAREST)
        gpuFondo = es.toGPUShape(bs.createTextureQuad("Fondo.png"), GL_REPEAT, GL_NEAREST)
        gpuNubes = es.toGPUShape(bs.createTextureQuad("Nubes.png"), GL_REPEAT, GL_NEAREST)
              
        self.y = 0.0
        self.j = -1.5
        
        self.pasto = gpuPastito
        self.puas = gpuPuas
        self.fondo = gpuFondo
        self.nubes = gpuNubes

    def draw(self, pipeline):
        nubesTransformer = np.matmul(tr.translate(0.4, 2.0 + self.y, 0), tr.uniformScale(1.0))
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, nubesTransformer)
        pipeline.drawShape(self.nubes)
        
        fondoTransformer = np.matmul(tr.translate(0, 0.15 + self.y, 0), tr.uniformScale(2.0))
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, fondoTransformer)
        pipeline.drawShape(self.fondo)
               
        pastitoTransformer = np.matmul(tr.translate(0, -0.925 + self.y, 0), tr.scale(2, 0.15, 1))
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, pastitoTransformer)
        pipeline.drawShape(self.pasto)

        puasTransformer = np.matmul(tr.translate(0, self.j + self.y, 0), tr.scale(2, 0.19, 1))
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, puasTransformer)
        pipeline.drawShape(self.puas)
        
        

        
class Bananas(object):
    def __init__(self):
        gpuBananas = es.toGPUShape(bs.createTextureQuad("Bananas.png"), GL_REPEAT, GL_NEAREST)
        self.x = 0.0 
        self.y = 0.0
        self.j = 0.0
        self.bananas = gpuBananas

    def draw(self, pipeline):
        bananasTransformer = np.matmul(tr.translate(self.x, self.y + self.j, 0), tr.uniformScale(0.2))
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, bananasTransformer)
        pipeline.drawShape(self.bananas)

class Win(object):
    def __init__(self):
        gpuYouWin = es.toGPUShape(bs.createTextureQuad("YouWin.png"), GL_REPEAT, GL_NEAREST)
        self.y = 2
        self.win = gpuYouWin

        gpuSparkle = es.toGPUShape(bs.createTextureQuad("Sparkle.png"), GL_REPEAT, GL_NEAREST)
        self.reflexT = 0
        self.reflexS = 2
        self.sparkle = gpuSparkle

    def draw(self, pipeline):
        winTransformer = np.matmul(tr.translate(0, self.y, 0), tr.uniformScale(2.0))
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, winTransformer)
        pipeline.drawShape(self.win)

        sparkleTransformer = np.matmul(tr.translate(self.reflexT, self.y, 0), tr.scale(self.reflexS, 2, 1))
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, sparkleTransformer)
        pipeline.drawShape(self.sparkle)     

    def Bajando(self,j):
        self.y -= j

class GameOver(object):
    def __init__(self):
        gpuGameOver = es.toGPUShape(bs.createTextureQuad("GameOver.png"), GL_REPEAT, GL_NEAREST)
        self.gameover = gpuGameOver

    def draw(self, pipeline):
        gameTRansformer = np.matmul(tr.translate(0, 0, 0), tr.uniformScale(2.0))
        glUniformMatrix4fv(glGetUniformLocation(pipeline.shaderProgram, "transform"), 1, GL_TRUE, gameTRansformer)
        pipeline.drawShape(self.gameover)

    


    


    

        
        

    
        
        

        

    
    
    
