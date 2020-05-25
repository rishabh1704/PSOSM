import csv
import pickle 
from flask_cors import CORS
from flask import Flask,jsonify,request

#=============================================================================================#

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True
 
#=============================================================================================#

#API calls

@app.route('/')
def home():
	return "<h1>This is the backend for our PSOSM Project</h1>"


@app.route('/myfriends/<boss>')
def getBossFriends(boss):
	try:
		results = all_weight[boss][mapping[boss]]
	except Exception as E:
		results = {'Error': str(E)}
	return jsonify(results)


@app.route('/friends/<boss>/<node>')
def getNodeFriends(boss,node):
	try:
		results = all_weight[boss][node]
	except Exception as E:
		results = {'Error': str(E)}
	return jsonify(results)


@app.route('/myattri/<boss>')
def getBossAttri(boss):
	try:
		results = all_attri[boss][mapping[boss]]
		if(boss=="kundu"):
			results["sensitive"] = ['interest','religious_views','pro_skills']
		if(boss=="rishabh"):
			results["sensitive"] = ['interest','religious_views','political']
		if(boss=="kshitij"):
			results["sensitive"] = ['language','life_event','pro_skills']

		for val in results["sensitive"]:
			results[val]["sensitive"] = True

	except Exception as E:
		results = {'Error': str(E)}
	return jsonify(results)


@app.route('/attri/<boss>/<node>')
def getNodeAttri(boss,node):
	try:
		results = all_attri[boss][node]
	except Exception as E:
		results = {'Error': str(E)}
	return jsonify(results)



#=============================================================================================#

#Utitlity Functions

def getWeight(boss):
	listy = {}
	in_file = "../boss_data/weights/weighted_"+boss+".csv"  
	row_reader = csv.reader(open(in_file, "r",encoding="utf8"))
	c=0
	for row in row_reader:
		if(c==0):
			print("\t"+str(row))
		else:
			if row[1] not in listy:
				listy[row[1]] = []
			
			listy[row[1]].append([row[3],row[2]])

		c+=1
		
	for uname in listy.keys():
		cur = listy[uname]
		cur.sort(reverse=True)
		dicti = {}
		for i in range(len(cur)):
			dicti[i] = cur[i]

		listy[uname] = dicti
	
	print("\tTotal number from weights: ",len(listy.keys()))
	return listy

def getAttri(boss):
	listy = {}
	in_file = "../boss_data/attributes/attributes_"+boss+".csv"  
	row_reader = csv.reader(open(in_file, "r",encoding="utf8"))
	c=0
	for row in row_reader:
		if(c==0):
			print("\t"+str(row))
		else:
			if row[14] not in listy:
				listy[row[14]] = {}
			
			for i in range(len(row)):
				listy[row[14]][name_row[i]] = {"value":row[i],"sensitive":False}
		c+=1
		
	print("\tTotal number from attributes : ",len(listy.keys()))

	return listy

#=============================================================================================#

#Command to run the app

if __name__ == "__main__":

	all_weight = {}
	all_attri = {}
	
	name_row = ["s_no","gender","interest","political","language","life_event","rel_status","religious_views","cities","pro_skills","college","school","quotes","companies","username"]

	mapping = {}
	mapping["kundu"] = "dhruv.kundu.1"
	mapping["kshitij"] = "kshitij.gulati"
	mapping["rishabh"] = "PyRishabhSharma"

	for boss in ["kundu","kshitij","rishabh"]:
		print("\n"+boss)
		all_attri[boss] = getAttri(boss)
		all_weight[boss] = getWeight(boss)

	app.run()

#=============================================================================================#