import csv
import pickle 
from flask_cors import CORS
from flask import Flask,jsonify,request

#=============================================================================================#

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

#=============================================================================================#


def getData():
    listy = {}
    in_file = "../present/weighted.csv"  
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

weighted = getData()


@app.route('/')
def home():
	return "<h1>This is the backend for our PSOSM Project</h1>"


@app.route('/<primary_friend>')
def getMyDetails(primary_friend):

	with open("../graphs/friend_graph_"+primary_friend+".pickle", 'rb') as f:
		graph_list = pickle.load(f)
	
	try:
		results = list(graph_list.keys())
		# print(len(results))

	except Exception as E:
		results = {'Error': str(E)}

	return jsonify(weighted)


@app.route('/<primary_friend>/<listed_friend>')
def getFriendDetails(primary_friend,listed_friend):

	with open("../graphs/friend_graph_"+primary_friend+".pickle", 'rb') as f:
		graph_list = pickle.load(f)
	
	try: 
		results = graph_list[listed_friend]
	except Exception as E:
		results = {'Error': str(E)}

	return jsonify(results)

#=============================================================================================#

#Command to run the app
if __name__ == "__main__":
	app.run()

#=============================================================================================#