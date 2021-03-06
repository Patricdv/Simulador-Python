# -*- coding: utf-8 -*-
import math
import re
from random import randint, random, randrange, uniform

import types

class Entities(object):
	def __init__(self, id = 0, startTime = 0, placeList = [], placeListId = [], placeEnterTime = [], placeExitTime = [], hostTime = 0, destiny = '', destinyId = 0, inComponent = 0, inServer = 0, totalOtioseTime = 0):
		self.id = id
		self.startTime = startTime
		self.placeList = placeList
		self.placeListId = placeListId
		self.placeEnterTime = placeEnterTime
		self.placeExitTime = placeExitTime
		self.hostTime = hostTime
		self.destiny = destiny
		self.destinyId = destinyId
		self.inComponent = inComponent
		self.inServer = inServer
		self.totalOtioseTime = totalOtioseTime

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
	entitiesQuantity = []
	destinyComponent = []
	destinyId = []

class Components(object):
	def __init__(self, id = 0, serversQuantity = 0, serversList = [], destinyComponent = '', destinyId = 0, stack = [], otioseTime = [], otioseList = []):
		self.id = id
		self.serversQuantity = serversQuantity
		self.serversList = serversList
		self.destinyComponent = destinyComponent
		self.destinyId = destinyId
		self.stack = stack
		self.otioseTime = otioseTime
		self.otioseList = otioseList

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
				if x == ';':
					break

			generators.list.append(int(number))
			position += 1

			number = ''
			x = line[position]
			while 1:
				number += str(x)
				position += 1
				x = line[position]
				if x == ';':
					break
			generators.entitiesQuantity.append(int(number))
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

		if line[0] == 'E':
			position = 1
			number = ''
			x = line[position]
			while 1:
				number += str(x)
				position += 1
				x = line[position]
				if x == ';':
					break
			global entitiesQuantity
			entitiesQuantity = int(number)

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
		print "-- S%d: %d - %d  %d" %(y, components[x].serversList[y].beginTime, components[x].serversList[y].endTime, components[x].serversList[y].inUse) 

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

## Beginning
entityId = 0

finalFile.write("1 - Entidades:")
print "1 - Entidades:"
for x in xrange(0, generators.quantity):
	quantity = generators.entitiesQuantity[x]
	for y in xrange(0, quantity):
		entityId += 1
		startTime = randint(1, 10) #simulationTime)
		placeList = []
		placeList.append('G')
		placeListId = []
		placeListId.append(generators.list[x])
		placeEnterTime = []
		placeEnterTime.append(startTime)
		placeExitTime = []
		placeExitTime.append(startTime)
		entities.append(Entities(entityId, startTime, placeList, placeListId, placeEnterTime, placeExitTime, 0, generators.destinyComponent[x], generators.destinyId[x], -1, 0, 0))
		print "%d | Entrada: %d | Local: %s%s | Destino: %s%d" %(entityId, startTime, placeList, placeListId, generators.destinyComponent[x], generators.destinyId[x])
		finalFile.write("\r\n" + str(entityId) + " | Entrada: " + str(startTime) + " | Local: G" + str(generators.list[x]) + " | Destino: " + str(generators.destinyComponent[x]) + str(generators.destinyId[x]))
		
for time in xrange(0, simulationTime):
	for x in xrange(0, len(entities)):
		if time > entities[x].startTime: 
			if entities[x].hostTime == 0:
				if entities[x].inComponent >= 0:
					components[entities[x].inComponent].serversList[entities[x].inServer].inUse = 0
					entities[x].placeExitTime[-1] = time
					entities[x].inComponent = -1
				else:
					if entities[x].destiny == 'C':
						aux = 0
						for y in xrange(0, len(components)):
							if (components[y].id == entities[x].destinyId) and (aux == 0):
								if len(components[y].stack):
									if components[y].stack[0] == entities[x].id:
										for z in xrange(0, len(components[y].serversList)):
											if (components[y].serversList[z].inUse == 0) and (aux == 0):
												components[y].serversList[z].inUse = 1
												entities[x].placeList.append('C')
												entities[x].placeListId.append(components[y].id)
												entities[x].placeEnterTime.append(time)
												entities[x].placeExitTime.append(0)
												entities[x].hostTime = randint(components[y].serversList[z].beginTime, components[y].serversList[z].endTime)
												entities[x].destiny = components[y].destinyComponent
												entities[x].destinyId = components[y].destinyId
												entities[x].inComponent = y
												entities[x].inServer = z
												aux += 1
										if aux == 1:
											components[y].stack.pop(0)
											entities[x].totalOtioseTime += (time - components[y].otioseTime[0])
											components[y].otioseList.append(time - components[y].otioseTime[0])
											components[y].otioseTime.pop(0)
									else:
										if entities[x].id not in components[y].stack:
											components[y].stack.append(entities[x].id)
											components[y].otioseTime.append(time)
								else: 
									for z in xrange(0, len(components[y].serversList)):
										if (components[y].serversList[z].inUse == 0) and (aux == 0):
											components[y].serversList[z].inUse = 1
											entities[x].placeList.append('C')
											entities[x].placeListId.append(components[y].id)
											entities[x].placeEnterTime.append(time)
											entities[x].placeExitTime.append(0)
											entities[x].hostTime = randint(components[y].serversList[z].beginTime, components[y].serversList[z].endTime)
											entities[x].destiny = components[y].destinyComponent
											entities[x].destinyId = components[y].destinyId
											entities[x].inComponent = y
											entities[x].inServer = z
											aux += 1
									if aux == 0 :
										components[y].stack.append(entities[x].id)
										components[y].otioseTime.append(time)
					elif entities[x].destiny == 'D':
						for y in xrange(0, len(dividers)):
							if dividers[y].id == entities[x].destinyId:
								rand = random()  
								check = 0.0
								aux = 0
								for z in xrange(0, len(dividers[y].decisionsList)):
									check += dividers[y].decisionsList[z].percent
									if (rand <= check) and (aux == 0):
										entities[x].placeList.append('D')
										entities[x].placeListId.append(dividers[y].id)
										entities[x].placeEnterTime.append(time)
										entities[x].placeExitTime.append(time)
										entities[x].destiny = dividers[y].decisionsList[z].destiny
										entities[x].destinyId = dividers[y].decisionsList[z].destinyId
										aux += 1
					elif entities[x].destiny == 'S':
						pass
			else:
				entities[x].hostTime -= 1

finalFile.write("\r\n---------------------------------------\r\n")

for x in xrange(0, entityId):
	print "\r\n%d Entrada: %d | " %(entities[x].id, entities[x].startTime),
	finalFile.write("\n" + str(entities[x].id) + " Tempo Ocioso: " + str(entities[x].totalOtioseTime) + " | Entrada: " + str(entities[x].startTime) + " | ")
	for y in xrange(0, len(entities[x].placeList)):
		print "Entidade:%s%d: %s - %ss | " %(entities[x].placeList[y], entities[x].placeListId[y], entities[x].placeEnterTime[y], entities[x].placeExitTime[y]),
		finalFile.write("Entidade:" + str(entities[x].placeList[y]) + str(entities[x].placeListId[y]) + ": " + str(entities[x].placeEnterTime[y]) + " - "  + str(entities[x].placeExitTime[y]) + "s ")
	print " || Tempo Ocioso: %d" %(entities[x].totalOtioseTime),
	finalFile.write(" || Tempo Ocioso: " + str(entities[x].totalOtioseTime))
	print "\r\n---------------------------------------"
	finalFile.write("\r\n---------------------------------------\r\n")


finalFile.write("Componentes:\n")
print "Componentes:"
for x in xrange(0, len(components)):
	averageOtioseTime = 0
	for y in xrange(0, len(components[x].otioseList)):
		averageOtioseTime += components[x].otioseList[y]
	averageOtioseTime = (averageOtioseTime/len(components[x].otioseList))
	finalFile.write("\r\n- C" + str(components[x].id) + " Tempo Médio de Fila: " + str(averageOtioseTime))
	print "- C%d Tempo Médio de Fila: %d" %(components[x].id, averageOtioseTime)
finalFile.write("\r\n---------------------------------------\r\n")
print "---------------------------------------"
