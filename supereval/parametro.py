import random

class Parametro:
	def __init__(self, nombre, minimo, maximo, decimales):
		self.nombre = nombre
		self.minimo = minimo or 0
		self.maximo = maximo or 100
		self.decimales = decimales or 2

	def instanciar(self):
		numero_random = random.uniform(self.minimo, self.maximo) # cuidado que asi como esta nunca devuelve maximo
		self.evaluacion = round(numero_random, self.decimales) # truncar en vez
		return self.evaluacion

	def __str__(self):
		self.instanciar()
		return self.nombre + ':' + str(self.decimales) + ':' +str(self.evaluacion)

	def eva_xml(self, cantidad_instancias):
		parametro_xml = '''
			<dataset_definition>
				<status><text>private</text></status>
				<name><text>{}</text></name>
				<type>calculatedsimple</type>
				<distribution><text>uniform</text></distribution>
				<minimum><text>{}</text></minimum>
				<maximum><text>{}</text></maximum>
				<decimals><text>{}</text></decimals>
				<itemcount>{}</itemcount>
				<dataset_items>'''.format(self.nombre, self.minimo, self.maximo, self.decimales, cantidad_instancias)
		for numero in range(cantidad_instancias):
			parametro_xml += '''
			<dataset_item>
				<number>{}</number>
				<value>{}</value>
			</dataset_item>'''.format(numero + 1, self.instanciar())
		parametro_xml += '''
				</dataset_items>
				<number_of_items>{}</number_of_items>
			</dataset_definition>'''.format(cantidad_instancias)
		return parametro_xml