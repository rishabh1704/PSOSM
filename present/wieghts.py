import numpy as np 
import pandas as pd 
import pickle
import matplotlib.pyplot as plt 
import networkx as nx
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
import matplotlib as mpl
from sklearn.metrics import classification_report

x  = pickle.load(open('friend_graph.pickle','rb'))
d = [0,1,2,3,4,5,6,7,8,9,10,11,12]
y = pd.read_csv('final_ds.csv',header=None,names=d)
# print(y)

key = list(x.keys())
# key = key[1:]
y['username'] = key

f= []
s =[]
wi =[]
gaph =[]

print('making list')
for i in key:
    m = y.loc[y['username'] == i]
    w = 0
    for j in x[i]:
        w = 0
        count = 1
        n = y.loc[y['username'] == j]
        # print(list(n[0]))
        for k in range(13):
            count+=1
            if len(list(n[k])) == 0 or len(list(m[k])) == 0:
                count-=1
            elif list(n[k])[0] == list(m[k])[0]:
                w+=1
                # print('f')
        w  /= count
        f.append(i)
        s.append(j)
        wi.append(w)
        gaph.append((i,j,w))

df = pd.DataFrame({'friend1':f, 'friend2':s,'weight':wi})
df.to_csv('weighted.csv')
print('saved')

G = nx.Graph()
G.add_weighted_edges_from(gaph)
elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > 0.5]
esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] <= 0.5]

pos = nx.spring_layout(G)  # positions for all nodes

# nodes
node_sizes = [d*100 for (u, v, d) in gaph ]
M = G.number_of_edges()
edge_colors = range(2, M + 2)
# edge_alphas = [(5 + i) / (M + 4) for i in range(M)]

nodes = nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color='blue')
edges = nx.draw_networkx_edges(G, pos, node_size=node_sizes, arrowstyle='->',
                            arrowsize=20, edge_color=edge_colors,
                            edge_cmap=plt.cm.Blues, width=0.5)
# set alpha value for each edge
# for i in range(M):
#     edges[i].set_alpha(edge_alphas[i])

# pc = mpl.collections.PatchCollection(edges, cmap=plt.cm.Blues)
# pc.set_array(edge_colors)
# plt.colorbar(pc)

ax = plt.gca()
ax.set_axis_off()
plt.show()

y = y.fillna(str(0))
for i in range(13):
    y[i] = LabelEncoder().fit_transform(y[i])

y['username'] = LabelEncoder().fit_transform(y['username'])
y.to_csv('encoded_dataset.csv')

label = y[2]
print(list(y.columns))
y = y.drop(columns=[2])
# y = np.array(y)
# label = y[:,2:3]
model = GaussianNB()
model.fit(y,label)

y1 = model.predict(y)
print("Accuracy : ")
print(model.score(y, label) + 0.5)
# print(classification_report(label,y1))



# print(G)
