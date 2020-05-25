def getAttriName():
	listy = []
	in_file = "../boss_data/attributes/attributes_gulati_old.csv"  
	row_reader = csv.reader(open(in_file, "r",encoding="utf8"))
	c=0
	for row in row_reader:
		if(c==0):
			print("\t"+str(row))
		else:
			listy.append(row[-1])
		c+=1
		
	# print("\tTotal number from attributes : ",len(listy.keys()))

	return listy

def getAttri():
	listy = []
	in_file = "../boss_data/attributes/attributes_kshitij.csv"  
	row_reader = csv.reader(open(in_file, "r",encoding="utf8"))
	c=0
	for row in row_reader:
		if(c==0):
			print("\t"+str(row))
		else:
			listy.append(row)
		c+=1
		
	# print("\tTotal number from attributes : ",len(listy.keys()))

	return listy

def changes(names,listy):
	out_file = "../boss_data/attributes/attributes_kshitij_final.csv"  
	row_writer = csv.writer(open(out_file, "w",encoding="utf-8", newline=''))  
	row_writer.writerow(["",0,1,2,3,4,5,6,7,8,9,10,11,12,"username"])
	
	for row in range(len(names)):  
		new_row = [row]
		# print(names[row])
		new_row.extend(listy[row][:-1])
		new_row = new_row[:-1]
		new_row.extend([names[row]])
		print(new_row)
		row_writer.writerow(new_row)
	print("CSV File Made.")

import csv
names = getAttriName()
listy = getAttri()
changes(names,listy)