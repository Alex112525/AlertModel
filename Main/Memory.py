# developed by Carlos Johnnatan Sandoval Arrayga
# email: carlos.sandoval@cinvestav.mx

class Memoria:

    def __init__(self, frecuenciaVector, amplitudVector, tempVector):
        self.__fvector = frecuenciaVector
        self.__avector = amplitudVector
        self.__tvector = tempVector

        # calculo los resultados de la memoria1(memoria de promedios sin perdidad de memoria)
        self.__m1f = []
        self.__m1a = []
        self.__m1t = []
        for i in range(len(self.__fvector)):
            if i == 0:
                self.__m1f.append(self.__fvector[i])
                self.__m1a.append(self.__avector[i])
                self.__m1t.append(self.__tvector[i])
                continue
            self.__m1f.append((self.__m1f[i - 1] * i + self.__fvector[i]) / float(i + 1))
            self.__m1a.append((self.__m1a[i - 1] * i + self.__avector[i]) / float(i + 1))
            self.__m1t.append((self.__m1t[i - 1] * i + self.__tvector[i]) / float(i + 1))

        # calculo los resultados de la memoria2(memoria con perdida de la memoria logaritmica)
        self.__m2f = []
        self.__m2a = []
        self.__m2t = []

        for i in range(len(self.__fvector)):
            if i == 0:
                self.__m2f.append(self.__fvector[i])
                self.__m2a.append(self.__avector[i])
                self.__m2t.append(self.__tvector[i])
                continue
            self.__m2f.append((self.__m2f[i - 1] + self.__fvector[i]) / 2.0)
            self.__m2a.append((self.__m2a[i - 1] + self.__avector[i]) / 2.0)
            self.__m2t.append((self.__m2t[i - 1] + self.__tvector[i]) / 2.0)

    # normalizo los datos usando z-score

    def promedio(self, tiempo=None, tipo=None):
        resp = float('NaN')

        if (tiempo == None):
            resp = [self.__m1f, self.__m1a, self.__m1t]
        elif (tiempo <= 0 and tipo == None):
            resp = [0, 0, 0]
        elif (tiempo <= 0 and tipo != None):
            resp = 0
        elif (tipo == None):
            tiempo = tiempo - 1
            resp = [self.__m1f[tiempo], self.__m1a[tiempo], self.__m1t[tiempo]]
        elif (tipo == "frecuencia"):
            tiempo = tiempo - 1
            resp = self.__m1f[tiempo]
        elif (tipo == 'amplitud'):
            tiempo = tiempo - 1
            resp = self.__m1a[tiempo]
        elif (tipo == 'tiempo'):
            tiempo = tiempo - 1
            resp = self.__m1t[tiempo]

        return (resp)

    def perdidaMemoria(self, tiempo=None, tipo=None):
        resp = float('NaN')

        if (tiempo == None):
            resp = [self.__m2f, self.__m2a, self.__m2t]
        elif (tiempo <= 0 and tipo == None):
            resp = [0, 0, 0]
        elif (tiempo <= 0 and tipo != None):
            resp = 0
        elif (tipo == None):
            resp = [self.__m2f[tiempo], self.__m2a[tiempo], self.__m2t[tiempo]]
        elif (tipo == "frecuencia"):
            resp = self.__m2f[tiempo]
        elif (tipo == 'amplitud'):
            resp = self.__m2a[tiempo]
        elif (tipo == 'tiempo'):
            resp = self.__m2t[tiempo]
        return (resp)


# pruebas de unidad del llenado de la informacion
'''
sonido1 = [1,2,3,4,5]
sonido2 = [6,7,8,9,10]
sonido3 = [11,12,13,14,15]
memoria = Memoria(sonido1,sonido2,sonido3)
#print(memoria.fvector)
#print(memoria.avector)
#print(memoria.tvector)
'''

# pruebas de unidad memoria 1
'''
print('promedio inicial')
print(memoria.promedio(0))
print(memoria.promedio(1))
print(memoria.promedio(2))
print(memoria.promedio(3))
print(memoria.promedio(4))
print('promedio')
print(memoria.promedio())
print(memoria.promedio(0))
print(memoria.promedio(-1))
print(memoria.promedio(0,'frecuencia'))
print(memoria.promedio(4))
print(memoria.promedio(4,'frecuencia'))
print(memoria.promedio(4,'amplitud'))
print(memoria.promedio(4,'tiempo'))
'''

# pruebas de unidad de memoria 2
'''
print('perdida de memoria')
print(memoria.perdidaMemoria())
print(memoria.perdidaMemoria(0))
print(memoria.perdidaMemoria(-1))
print(memoria.perdidaMemoria(0,'tiempo'))

print(memoria.perdidaMemoria(2))
print(memoria.perdidaMemoria(2, 'frecuencia'))
print(memoria.perdidaMemoria(2, 'amplitud'))
print(memoria.perdidaMemoria(2, 'tiempo'))
'''

