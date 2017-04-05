import argparse
import unicodedata
from .ejercicio import Ejercicio
from .prueba import Prueba
import pdb
from collections import defaultdict

def remover_acentos(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn') 

def abrir_contenedor(nombre_archivo):
	# pdb.set_trace()
	archivo = open(nombre_archivo, 'r')
	return [linea for linea in archivo]

def contiene_clave(linea, especifico=['titulo',
										'problema', 
										'solucion', 
										'distractor', 
										'comentario',
										'parametro',
										'computo',
										'maximo',
										'minimo',
										'decimales',
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

def parametrizar_eval(titulo_prueba, nombres_ejercicios, numero_instancias=0, texto=False, latex=False, eva=False):
	# pdb.set_trace()
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

if __name__ == "__main__": 
	parser = argparse.ArgumentParser(description="Crea prueba a partir de los ejercicios parametrizados")
	parser.add_argument('titulo', help='Titulo de la prueba')
	parser.add_argument('ejercicios_parametrizados', nargs='+', 
						help='Lista de ejercicios parametrizados.')
	parser.add_argument('--cantidad', type=int, help='Cantidad de pruebas')
	parser.add_argument('--texto', action="store_true", help='Exportacion a texto plano')
	parser.add_argument('--pdf', action="store_true", help='Exportacion a PDF')
	parser.add_argument('--eva', action="store_true", help='Para importar a entorno EVA')
	parser.add_argument('--encabezado', help='Encabezado en formato LaTeX')
	args = parser.parse_args()
	
	parametrizar_eval(
		args.titulo, 
		args.ejercicios_parametrizados, 
		numero_instancias=args.cantidad, 
		texto=args.texto, 
		eva=args.eva, 
		latex=args.pdf)


