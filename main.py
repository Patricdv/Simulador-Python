# -*- coding: utf-8 -*-
import math
import re
from random import randint
from random import randrange, uniform
import types

class Entities(object):
	def __init__(self, id = 0, startTime = 0, placeList = [], placeListId = [], placeEnterTime = [], hostTime = 0, destiny = '', destinyId = 0):
		self.id = id
		self.startTime = startTime
		self.placeList = placeList
		self.placeListId = placeListId
		self.placeEnterTime = placeEnterTime
		self.hostTime = hostTime
		self.destiny = destiny
		self.destinyId = destinyId

class Server(object):
    def __init__(self, componentId = 0, beginTime = 0, endTime = 0, inUse = 0):
        self.componentId = componentId
        self.beginTime = beginTime
        self.endTime = endTime
        self.inUse = inUse

class Decisions(object):
	def __init__(self, percent = 0.0, destiny = '', destinyId = 0):
		self.percent = percent
		self.destiny = destiny
		self.destinyId = destinyId

class Generators:
	quantity = 0
	list = []
	destinyComponent = []
	destinyId = []

class Components(object):
	def __init__(self, id = 0, serversQuantity = 0, serversList = [], destinyComponent = '', destinyId = 0):
		self.id = id
		self.serversQuantity = serversQuantity
		self.serversList = serversList
		self.destinyComponent = destinyComponent
		self.destinyId = destinyId
	
class Dividers(object):
	def __init__(self, id = 0, decisionsList = []):
		self.id = id
		self.decisionsList = decisionsList

entities = []
generators = Generators()
components = []
dividers = []
simulationTime = 0

def makeModel(model):
	for line in model:
		if line[0] == 'G':
			position = 1
			generators.quantity += 1
			
			number = ''
			x = line[position]
			while 1:
				number += str(x)
				position += 1
				x = line[position]
				if x == '-':
					break

			generators.list.append(int(number))
			position += 1
			generators.destinyComponent.append(line[position])
			position += 1

			number = ''
			x = line[position]
			while 1:
				number += str(x)
				position += 1
				x = line[position]
				if x == ';':
					break
			
			generators.destinyId.append(int(number))

		if line[0] == 'C':
			position = 1
			number = ''
			x = line[position]
			while 1:
				number += str(x)
				position += 1
				x = line[position]
				if x == ';':
					break

			componentId = int(number)

			position += 1
			number = ''
			x = line[position]
			while 1:
				number += str(x)
				position += 1
				x = line[position]
				if x == ';':
					break

			serversQuantity = int(number)

			serversList = []
			while 1:
				position += 1
				number = ''
				x = line[position]
				while 1:
					number += str(x)
					position += 1
					x = line[position]
					if x == ':':
						break

				serverId = int(number)

				position += 1
				number = ''
				x = line[position]
				while 1:
					number += str(x)
					position += 1
					x = line[position]
					if x == '-':
						break

				serverBeginTime = int(number)

				position += 1
				number = ''
				x = line[position]
				while 1:
					number += str(x)
					position += 1
					x = line[position]
					if x==',' or x == ';':
						break

				serverEndTime = int(number)
				serversList.append(Server(componentId, serverBeginTime, serverEndTime))
				
				if x == ';':
					break 

			position += 1
			componentDestiny = line[position]

			position += 1
			number = ''
			x = line[position]
			while 1:
				number += str(x)
				position += 1
				x = line[position]
				if x == ';':
					break

			componentDestinyId = int(number)
			components.append(Components(componentId, serversQuantity, serversList, componentDestiny, componentDestinyId))

		if line[0] == 'D':
			position = 1
			number = ''
			x = line[position]
			while 1:
				number += str(x)
				position += 1
				x = line[position]
				if x == ';':
					break
			dividerId = int(number)

			decisionsList = []
			while 1:
				position += 1
				number = ''
				x = line[position]
				while 1:
					number += str(x)
					position += 1
					x = line[position]
					if x == '-':
						break

				decisionPercent = float(number)

				position += 1
				destinyComponent = line[position]
				
				position += 1
				number = ''
				x = line[position]
				while 1:
					number += str(x)
					position += 1
					x = line[position]
					if x == ';' or x == ',':
						break

				destinyId = int(number)

				decisionsList.append(Decisions(decisionPercent, destinyComponent, destinyId))
				
				if x == ';':
					break 
			dividers.append(Dividers(dividerId, decisionsList))

		if line[0] == 'T':
			position = 1
			number = ''
			x = line[position]
			while 1:
				number += str(x)
				position += 1
				x = line[position]
				if x == ';':
					break
			global simulationTime
			simulationTime = int(number)

## Main
			
file = open("base", "r");
model = file.readlines();
makeModel(model)
file.close();

## File Basics:
finalFile = open("final.txt", "wb")

finalFile.write("---------------------------------------\r\n")
print "---------------------------------------"

finalFile.write("Tempo de Simulacao:" + str(simulationTime))
print "Tempo de Simulacao: %d" %(simulationTime)

finalFile.write("\r\n---------------------------------------\r\n")
print "---------------------------------------"

finalFile.write("Gerador(es):" + str(generators.quantity))
print "Gerador(es): %d" %(generators.quantity)

for x in xrange(0, generators.quantity):
	finalFile.write("\r\n- G" + str(generators.list[x]) + " Destino: " + str(generators.destinyComponent[x]) + str(generators.destinyId[x]))
	print "- G%d Destino: %s%d" %(generators.list[x], generators.destinyComponent[x], generators.destinyId[x])

finalFile.write("\r\n---------------------------------------\r\n")
print "---------------------------------------"

componentsQuantity = len(components)
finalFile.write("Componentes: " + str(componentsQuantity))
print "Componentes: %d" %(componentsQuantity)

for x in xrange(0, componentsQuantity):
	finalFile.write("\r\n- C" + str(components[x].id) + " Destino: " + str(components[x].destinyComponent) + str(components[x].destinyId))
	print "- C%d Destino: %s%d" %(components[x].id, components[x].destinyComponent, components[x].destinyId)

	for y in xrange(0, components[x].serversQuantity):
		finalFile.write("\r\n-- S" + str(y) + ":" + str(components[x].serversList[y].beginTime) + " - " + str(components[x].serversList[y].endTime))
		print "-- S%d: %d - %d" %(y, components[x].serversList[y].beginTime, components[x].serversList[y].endTime) 

finalFile.write("\r\n---------------------------------------\r\n")
print "---------------------------------------"

dividersQuantity = len(dividers)
finalFile.write("Roteadores: "+ str(dividersQuantity))
print "Roteadores: %d" %(dividersQuantity)

for x in xrange(0, dividersQuantity):
	finalFile.write("\r\n- D" + str(dividers[x].id) + ":")
	print "- D%d:" %(dividers[x].id)

	for y in xrange(0, len(dividers[x].decisionsList)):
		finalFile.write("\r\n-- " + str(dividers[x].decisionsList[y].percent) + " - " + str(dividers[x].decisionsList[y].destiny) + str(dividers[x].decisionsList[y].destinyId))
		print "-- %f - %s%d" %(dividers[x].decisionsList[y].percent, dividers[x].decisionsList[y].destiny, dividers[x].decisionsList[y].destinyId)

finalFile.write("\r\n---------------------------------------\r\n")
print "---------------------------------------"

entityQuantity = 0
## Beginning
for x in xrange(0, generators.quantity):
	quantity = randint(1, 10)
	for y in xrange(0, quantity):
		entityQuantity += 1
		startTime = randint(1, 25) #simulationTime)
		placeList = []
		placeList.append('G')
		placeListId = []
		placeListId.append(generators.list[x])
		entities.append(Entities(entityQuantity, startTime, placeList, placeListId, startTime, 0, generators.destinyComponent[x], generators.destinyId[x]))

print "Entidades:"
for time in xrange(1, simulationTime):
	for x in xrange(0, entityQuantity):
		if entities[x].startTime >= time and entities[x].hostTime == 0:
			
			print "%d | Entrada: %d | Local: %s%s | Destino: %s%d" %(entities[x].id, entities[x].startTime, entities[x].placeList[0], entities[x].placeListId[0], entities[x].destiny, entities[x].destinyId)

	#print "---------------------------------------"