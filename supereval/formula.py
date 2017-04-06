import math

def unpack_dict(a, b):
	for c, v in b.items():
		a[c] = v
	return a

class Formula:
	def __init__(self, nombre, computo, decimales):
		self.nombre = nombre
		self.computo = computo
		self.decimales = decimales or 2
		
	def instanciar(self, vars_instanciadas):
		self.evaluacion = round(eval(self.computo, unpack_dict(math.__dict__, vars_instanciadas)), self.decimales)
		return self.evaluacion

	def __str__(self):
		self.instanciar()
		return self.nombre + ':' + str(self.decimales) + ':' +str(self.evaluacion)
