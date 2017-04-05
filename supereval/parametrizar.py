import unicodedata
from .ejercicio import Ejercicio
from .prueba import Prueba
from collections import defaultdict

def remover_acentos(s):
	return ''.join(c for c in unicodedata.normalize('NFD', s)
								if unicodedata.category(c) != 'Mn') 

def abrir_contenedor(nombre_archivo):
	archivo = open(nombre_archivo, 'r')
	return [linea for linea in archivo]


def contiene_clave(linea, especifico=['titulo',
										'problema', 
										'solucion', 
										'distractor', 
										'comentario',
										'parametro',
										'maximo',
										'minimo',
										'decimales',
										'computo',
										'formula']):
	if ':' not in linea:
		return False
	clave = remover_acentos(linea.split(':')[0].strip().lower())
	return clave in especifico


def clave_valor(lineas):
	linea = lineas.pop(0)
	clave = remover_acentos(linea.split(':')[0].strip().lower())
	valor = ''.join(linea.split(':')[1:]).lstrip()
	while lineas and not contiene_clave(lineas[0]):
		linea_pregunta = lineas.pop(0)
		valor += linea_pregunta
	return clave, valor.strip()


def parsear_ejercicio(nombre_ejercicio):
	ejercicio = Ejercicio()
	ejercicio.nombre = nombre_ejercicio
	lineas = abrir_contenedor(nombre_ejercicio)
	while lineas:
		if contiene_clave(lineas[0]):
			clave, valor = clave_valor(lineas)
			if clave == 'titulo': ejercicio.set_titulo(valor)
			elif clave == 'problema': ejercicio.set_problema(valor)
			elif clave == 'solucion': ejercicio.set_solucion(valor)
			elif clave == 'distractor':	ejercicio.agregar_distractor(valor)
			elif clave == 'parametro':
				nombre = valor
				minimo = None
				maximo = None
				decimales = None
				subclaves_posibles = ['maximo', 'minimo', 'decimales']
				while lineas and contiene_clave(lineas[0], subclaves_posibles):
					subclave, valor = clave_valor(lineas)
					if subclave == 'minimo':
						subclaves_posibles.remove('minimo')
						minimo = int(valor)
					elif subclave == 'maximo':
						subclaves_posibles.remove('maximo')
						maximo = int(valor)
					elif subclave == 'decimales':
						subclaves_posibles.remove('decimales')
						decimales = int(valor)
				ejercicio.agregar_parametro(nombre, minimo, maximo, decimales)
			elif clave == 'computo':
				subclaves_posibles = ['formula', 'decimales']
				nombre = valor
				formula = None
				decimales = None
				while lineas and contiene_clave(lineas[0], subclaves_posibles):
					subclave, valor = clave_valor(lineas)
					if subclave == 'formula':
						subclaves_posibles.remove('formula')
						formula = valor
					elif subclave == 'decimales':
						subclaves_posibles.remove('decimales')
						decimales = int(valor)
				if not formula: raise Exception('No se especifico formula de ' + nombre)
				ejercicio.agregar_formula(nombre, formula, decimales) # se deberia llamar agregar computo
			elif clave == 'comentario':	
				pass
			else:
				print('ADVERTENCIA: No se reconoce la clave {}.'.format(clave))
		else:
			lineas.pop(0)
	return ejercicio


def parametrizar_eval(
	titulo_prueba, 
	nombres_ejercicios, 
	numero_instancias, 
	texto=False, 
	latex=False, 
	eva=False):
	prueba = Prueba(titulo_prueba, numero_instancias)
	for nombre_ejercicio in nombres_ejercicios:
		ejercicio =  parsear_ejercicio(nombre_ejercicio)
		prueba.agregar_ejercicio(ejercicio)
	
	if texto:
		prueba.generar('texto')
		return prueba.nombre
	if latex:
		prueba.generar('latex')
		return prueba.nombre
	if eva:
		prueba.generar('eva')
		return prueba.nombre + '.xml'