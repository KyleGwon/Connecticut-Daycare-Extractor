import csv
import sys

def main():
	"""
	Purpose: edit the csv file specified in command-line
	Parameters: None
	"""
	if __name__ == "__main__":
		# print(sys.argv)
		try:
			dataFileName = sys.argv[1]
			csvFileName = sys.argv[2]
			data = readData(dataFileName)
			writeCSV(csvFileName, data)
			print(f"Succes! Data from {dataFileName} was exported to {csvFileName}")
		except:
			print("Error: Make sure you are running the command in the following format:\n\"python3 ct_daycare_extractor.py [input file name].txt [output file name].csv\"\n(If the file names contain spaces, put the exact name in quotes \"\")")


	# dataFileName = "daycaresCT.txt"
	# csvFileName = "daycaresData.csv"
	# writeCSV("daycaresData.csv", data)


def writeCSV(fileName, data):
	"""
	Purpose:
	Parameters:
		fileName - file name derrived from the command-line
	"""
	with open(fileName, "w") as csv_file:
		writer = csv.writer(csv_file, lineterminator="\n")
		writer.writerow(["Owner's Name", "Daycare's Name", "Full Address", "Town", "Phone Number 1", "Phone Number 2", "License"])
		for i in range(len(data)):
			writer.writerow(data[i])


def readData(fileName):
	"""
	Purpose: read the raw data from d
	Parameters:
		fileName - file name derrived from the command-line 
	"""
	file = open(fileName, "r")
	data = file.readlines()
	data = cleanLines(data)
	data = parseDaycares(data)

	for i in range(len(data)):
		print(data[i])
	return data

def cleanLines(lines):
	"""
	Purpose: returns lines without trailing whitespace or empty lines
	Parameters:
		lines - raw lines of data from txt file
	"""
	newLines = []
	for i in range(len(lines)):
		if lines[i] != "\n":
			newLines.append(lines[i].rstrip())
	return newLines



def parseDaycares(data):


	newData = []
	activeCounter = 0
	for i in range(len(data)):
		if data[i] == "More Filters": #start of section
			activeCounter = 1
		
		elif data[i] == "Don't see a provider listed? Have additional questions?": #end of section
			activeCounter = 0

		elif data[i] == "Add to Compare" or data[i] == "Not accepting referrals":
			activeCounter = 1

		else:
			if activeCounter:
				if activeCounter == 1: #owner's name
					if data[i][0].isalpha():
						newData.append([data[i]]) #create a nested list in data containing the owner's name
					else:
						newData.append([""])
						activeCounter += 1
				
				if activeCounter == 2: #daycare's name
					if data[i][0].isalpha() or data[i+2][0].isnumeric():
						newData[-1].append(data[i])
					else:
						newData[-1].append("")
						activeCounter += 1

				
				if activeCounter == 3: #address
					if data[i][0].isnumeric():
						newData[-1].append(data[i])
						print(data[i])
						newData[-1].append(data[i].split(",")[-2])
					else:
						if data[i+1][0].isnumeric():
							newData[-1].append(data[i])
							newData[-1].append(data[i].split(",")[-2])
						else:
							newData[-1].append("")
							newData[-1].append("")
							activeCounter += 1
				
				if activeCounter == 4: #phone number
					#format xxx-xxx-xxxx
					temp = ""
					for j in range(len(data[i])):
						if data[i][j].isnumeric():
							temp += data[i][j]
					newData[-1].append(temp[:3]+"-"+temp[3:6]+"-"+temp[6:10])
					if len(temp) > 10:
						newData[-1].append(temp[10:13]+"-"+temp[13:16]+"-"+temp[16:20])
					else:
						newData[-1].append("")
				
				if activeCounter == 5: #license identifier
					newData[-1].append(data[i].split()[-1])

				activeCounter += 1
	return newData

main()