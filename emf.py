#!/bin/env python3

# the reason this code uses hungarian notation is this code was moved from another codebase

import copy
import re
import pickle
import struct
import io
import lzma

class VMF:
	lBlocks = None
	hFile = None
	formatversion = "100"
	emf = False

	def __init__(self, file = None):
		if not file:
			return
		self.hFile = file
		self.lBlocks = []
		b = self.ReadBlock()
		while b:
			self.lBlocks.append(b)
			b = self.ReadBlock()
			#pprint.pprint(b)
		dVerInfo = self.GetVersionInfo()
		if dVerInfo:
			self.formatversion = dVerInfo["formatversion"]
			self.emf = self.formatversion == "100_emf"

	# Get world block
	def GetWorld(self):
		for dBlock in self.lBlocks:
			if dBlock["__classname__"] == "world":
				return dBlock
		return None

	# Solid generator
	def GetGeometries(self):
		dWorld = self.GetWorld()
		if not dWorld["__subblocks__"]:
			return []
		if len(dWorld["__subblocks__"]) == 0:
			return []
		for dSubBlock in dWorld["__subblocks__"]:
			if dSubBlock["__classname__"] == "solid":
				yield Geometry(dSubBlock)

	def GetEntities(self):
		for dBlock in self.lBlocks:
			if dBlock["__classname__"] == "entity":
				yield dBlock

	# Tile generator
	def GetTiles(self):
		if not self.emf:
			raise Exception("Incompatible formatversion: '%s', Tiles not available" % self.formatversion)
		dWorld = self.GetWorld()
		if not dWorld["__subblocks__"]:
			return []
		if len(dWorld["__subblocks__"]) == 0:
			return []
		for dSubBlock in dWorld["__subblocks__"]:
			if dSubBlock["__classname__"] == "tiles":
				for dTileBlock in dSubBlock["__subblocks__"]:
					yield Tile(dTileBlock)

	# Get versioninfo block
	def GetVersionInfo(self):
		for dBlock in self.lBlocks:
			if dBlock["__classname__"] == "versioninfo":
				return dBlock
		return None

	def ReadLine(self):
		strLine = self.hFile.readline()
		if not strLine:
			return None
		return strLine.lstrip().rstrip()

	# Reads a block and it's sub-blocks
	def ReadBlock(self, strClassName = None):
		if not self.hFile:
			return

		def FindAll(strString, cChar):
			return [i for i, cLetter in enumerate(strString) if cLetter == cChar]

		dBlock = {}
		if strClassName:
			strLine = strClassName
		else:
			strLine = self.ReadLine()
		#while strLine.startswith("//"):
		#	szLline = self.hFile.readline()
		dBlock["__classname__"] = strLine
		dBlock["__subblocks__"] = []
		strLine = self.ReadLine()
		if not strLine:
			return None
		assert strLine == "{"
		strLine = self.ReadLine()
		if not strLine:
			return None
		while strLine != "}":
			if strLine.startswith('"'):
				#kv
				arrIndices = FindAll(strLine, '"')	
				assert len(arrIndices) == 4
				strProperty = strLine[arrIndices[0] + 1:arrIndices[1]]
				strValue = strLine[arrIndices[2] + 1:arrIndices[3]]
				if strProperty == "plane": #Vector3 Array3
					lNumbers = strValue.split()
					strValue = []
					for i in range(0, 3):
						lVector = []
						lVector.append(float(lNumbers[i * 3][1:]))
						lVector.append(float(lNumbers[i * 3 + 1]))
						lVector.append(float(lNumbers[i * 3 + 2][:-1]))
						strValue.append(lVector)

				elif strProperty in ["origin", "angles"]:
					lNumbers = strValue.split()
					strValue = []
					for i in range(0, 3):
						strValue.append(float(lNumbers[i]))

				elif strProperty == "_light":
					lNumbers = strValue.split()
					strValue = []
					for i in range(0, 4):
						strValue.append(int(lNumbers[i]))

				elif strProperty == "spawnflags":
					strValue = int(strValue)

				elif strProperty in ["position", "size"]:
					lNumbers = strValue.split()
					strValue = []
					for i in range(0, 2):
						strValue.append(int(lNumbers[i]))


				dBlock[strProperty] = strValue
			elif not strLine.startswith('/'):
				dSubBlock = self.ReadBlock(strLine)
				if strLine != "editor": # discard Hammer metadata
					dBlock["__subblocks__"].append(copy.deepcopy(dSubBlock))
			strLine = self.ReadLine()
			if not strLine:
				return None
		return dBlock

class Geometry:
	sides = []
	def __init__(self, dBlock):
		assert dBlock["__classname__"] == "solid"
		for dSubBlock in dBlock["__subblocks__"]:
			if dSubBlock["__classname__"] == "side":
				side = [None, None, None]
				for i in range(0, 3):
					side[i] = dSubBlock["plane"][i]
				self.sides.append(side)


class Entity:
	properties = {}
	def __init__(self, dBlock):
		assert dBlock["__classname__"] == "entity"
		for k,v in dBlock.items():
			if k.startswith("__"):
				continue
			self.properties[k] = v

	def GetProperty(self, key):
		return self.properties[key]

class Tile:
	position = None
	size = None
	properties = {}
	def __init__(self, dBlock):
		assert dBlock["__classname__"] == "tile"
		for k,v in dBlock.items():
			if k.startswith("__"):
				continue
			if k == "position":
				self.position = dBlock[k]
			elif k == "size":
				self.size = dBlock[k]
			else:
				self.properties[k] = v

# ETM is the Easimer Tile Map format. It's really just the VMF.lBlocks list serialized and compressed with LZMA.
# ETMv1 Header
# unsigned long - magic (0xe1117001)
# unsigned long - is compressed (0 - false, 1 - true)

class ETM:

	EMF_VERSION = 0x001

	@staticmethod
	def WriteHeader(hFile, dHeader):
		if not dHeader or not hFile:
			return
		hFile.write(struct.pack("<LL", 0xe1117000 | ETM.EMF_VERSION, dHeader["compress"]))

	@staticmethod
	def ReadHeader(hFile):
		if not hFile:
			return
		nMagic = 0
		nCompressed = 0
		(nMagic, nCompressed) = struct.unpack("<LL", hFile)
		return (nMagic, nCompressed)

	@staticmethod
	def Compress(bData):
		if not bData:
			return
		return lzma.compress(bData)

	@staticmethod
	def Decompress(bData):
		if not bData:
			return
		return lzma.decompress(bData)

	@staticmethod
	def Serialize(bData):
		if not bData:
			return
		hMemFile = io.BytesIO()
		pickle.dump(bData, hMemFile)
		hMemFile.seek(0)
		ret = hMemFile.read()
		hMemFile.close()
		return ret

	@staticmethod
	def Deserialize(bData):
		if not bData:
			return
		hMemFile = io.BytesIO()
		hMemFile.write(bData)
		hMemFile.seek(0)
		ret = picke.load(hMemFile)
		hMemFile.close()
		return ret

	@staticmethod
	def Sign(bData, privkey):
		return bData


	# Verify signed tile data
	@staticmethod
	def Verify(bData, pubkey):
		return bData

	@staticmethod
	def ReadMap(path):
		with open(path, 'rb') as hFile:
			(nMagic, nCompressed) = ETM.ReadHeader(hFile)
			if nMagic != 0xe1117001:
				return False
			bData = hFile.read()
			if nCompressed == 1:
				bData = ETM.Decompress(bData)
			cMap = VMF()
			cMap.lBlocks = ETM.Deserialize(bData)
			return cMap
