import seriallib
import constants
import time

class InputManager:
	def __init__(self, configCSVPath):
		self.mappingDict = {button: [] for button in constants.validButtonValues}
		f = open(configCSVPath, "r")
		f.readline()
		keyMappingDict = {}
		for line in f.readlines():
			seperatedLine = line.strip().replace(" ", "").split(",")
			if len(seperatedLine) == 1:
				continue
			
			button = seperatedLine[0].upper()
			if not button in constants.validButtonValues:
				print(f"Invalid Button Name ({button})")
				continue
			
			keys = seperatedLine[1:]
			keyMappingDict[button] = keys
			for key in keys:
				if key.lower() in constants.nameKeyValDict:
					self.mappingDict[button].append(constants.nameKeyValDict[key])
				else:
					print(f"Received incorrect key value ({key}). Please refer to keys.txt for list of valid keys")
		print(keyMappingDict)

	def processInputs(self, payload: seriallib.Payload,  keysDown: list, mouseDiff: tuple) -> seriallib.Payload:
		dPadDir = [0, 0]
		for button, mappedKeys in self.mappingDict.items():
			if "mx" in mappedKeys or "my" in mappedKeys:
				if button in ["-LX","+LX"]:
					payload.setLeftX(128 + mouseDiff[0])
				elif button in ["-LY","+LY"]:
					payload.setLeftY(128 + mouseDiff[1])
				elif button in ["-RX","+RX"]:
					payload.setRightX(128 + mouseDiff[0])
				elif button in ["-RY","+RY"]:
					payload.setRightY(128 + mouseDiff[1])

			keysDown2 = [x+96 for x in keysDown if x != 306 and isinstance(x, int)] # If you hold ctrl + a key you get a different char value. A value that differs by 96
			'''try:
				keysDown2 = [x for x in keysDown[keysDown.index(306)+1:] if isinstance(x, int)]
				if len(keysDown2) > 0:
					for i in range(len(keysDown2)):
						keysDown2[i] += 96
			except ValueError: pass'''
			newKeysDown = []
			for key in keysDown:
				if str(key).isdigit() == False:
					try:
						newKeysDown.append(self.mappingDict[key][0])
					except KeyError:
						newKeysDown.append(key)
				else:
					newKeysDown.append(key)

			if any(key in newKeysDown for key in mappedKeys) or any(key in keysDown2 for key in mappedKeys):
				if button in constants.validButtonValues[12:]:
					payload.applyButtons(1 << (constants.validButtonValues.index(button) - 12))

				elif button == "-LX":
					payload.setLeftX(0)
				elif button == "+LX":
					payload.setLeftX(255)

				elif button == "-LY":
					payload.setLeftY(0)
				elif button == "+LY":
					payload.setLeftY(255)

				elif button == "-RX":
					payload.setRightX(0)
				elif button == "+RX":
					payload.setRightX(255)

				elif button == "-RY":
					payload.setRightX(0)
				elif button == "+RY":
					payload.setRightX(255)

				elif button == "DLEFT":
					dPadDir[0] += -1
				elif button == "DRIGHT":
					dPadDir[0] += 1
				elif button == "DUP":
					dPadDir[1] += -1
				elif button == "DDOWN":
					dPadDir[1] += 1

		payload.setHatFromVector(dPadDir[0], dPadDir[1])
		return payload
