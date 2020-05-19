import pickle 
from flask_cors import CORS
from flask import Flask,jsonify,request

#=============================================================================================#

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True

#=============================================================================================#


@app.route('/')
def home():
	return "<h1>This is the backend for our PSOSM Project</h1>"


@app.route('/<primary_friend>')
def getMyDetails(primary_friend):

	with open("../graphs/friend_graph_"+primary_friend+".pickle", 'rb') as f:
		graph_list = pickle.load(f)
	
	try: 
		results = list(graph_list.keys())
	except Exception as E:
		results = {'Error': str(E)}

	return jsonify(results)


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