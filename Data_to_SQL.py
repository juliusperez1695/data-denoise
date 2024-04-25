'''Run this script only for initial importing of CSV data into SQL database'''

from SQLServerImportSet1 import * 
from SQLServerImportSet2 import * 

def loadData(fileName):
	df = pd.read_csv(fileName, header=None)
	df.columns = ['x','y']
	print(df)
	print("\nData upload successful!\n")

	#Read csv file and import to specific db table based on user input
	import1 = SQLServerImportSet1
	import2 = SQLServerImportSet2
	
	if fileName == "Dataset1.csv":
		import1.import_csv_tosql()
	else:
		import2.import_csv_tosql()


def main():
	fileName = input("\nEnter the File Name for the data you wish to import: ")
	loadData(fileName)

main()