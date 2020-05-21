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


@app.route('/friends/<boss>')
def getBossFriends(boss):
	try:
		results = all_weight[boss][boss]
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


@app.route('/attri/<boss>')
def getBossAttri(boss,node):
	try:
		results = all_attri[boss][boss]
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


@app.route('/netgraph/<boss>')
def getNetGraph(boss,node):
	try:
		with open("../graphs/friend_graph_"+boss+".pickle", 'rb') as f:
			graph_list = pickle.load(f)	
		
	except Exception as E:
		results = {'Error': str(E)}
	return jsonify(results)

@app.route('/frgraph/<boss>')
def getFrGraph(boss,node):
	try:
		with open("../graphs/friend_graph_"+boss+".pickle", 'rb') as f:
			graph_list = pickle.load(f)
	except Exception as E:
		results = {'Error': str(E)}
	return jsonify(results)

#=============================================================================================#

#Utitlity Functions

def getWeight(boss):
    listy = {}
    in_file = "../present/weighted_"+boss+".csv"  
    row_reader = csv.reader(open(in_file, "r",encoding="utf8"))
    c=0
    for row in row_reader:
        if(c==0):
            print(row)
        else:
            if row[1] not in listy:
            	listy[row[1]] = {}
            
            listy[row[1]][row[2]] = row[3]

        c+=1
        
    print("\nTotal number : ",len(listy.keys()))
    return listy

def getAttri(boss):
    listy = {}
    in_file = "../present/attributes_"+boss+".csv"  
    row_reader = csv.reader(open(in_file, "r",encoding="utf8"))
    c=0
    for row in row_reader:
        if(c==0):
            print(row)
        else:
            if row[1] not in listy:
            	listy[row[1]] = {}
            
            listy[row[1]][row[2]] = row[3]

        c+=1
        
    print("\nTotal number : ",len(listy.keys()))
    return listy

#=============================================================================================#

#Command to run the app

if __name__ == "__main__":

	all_weight = {}
	for boss in ["kundu","kshitij","rishabh"]:
		all_attri[boss] = getAttri(boss)
		all_weight[boss] = getWeight(boss)
		
	app.run()

#=============================================================================================#