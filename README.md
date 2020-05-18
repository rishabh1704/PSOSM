
First of all SWITCH FACEBOOK TO CLASSIC MODE else nothing will work.

There are 3 folders here.

Please install the required libraries.

1. "facebook-friend-graph" : this repo is used to generate the graph of your fb account's friend network. By default I have configured it with selenium for Firefox.
URL : "https://github.com/EliotAndres/facebook-friend-graph"

=========contents=============

facebookFOF.py -> generates friend_graph.p, unique_urls.p (graph and the url list of friends)[run this]

Facebook friend graph.ipynb -> Plots the graph. uses networkX/plotly.

Change the central URL here and give in the graph.pickle file generated using facebookFOF.py

geckodriver -> firefox selenium web driver

2. Ultimate-Facebook-Scraper : this repo is used to extract information about user profiles.
URL : "https://github.com/harismuneer/Ultimate-Facebook-Scraper"

========contents===========

bin - place your driver of choice for selenium

data - contains the output

credentials.yaml : provide your credentials

input.txt : list of accounts to be scraped

scraper/scraper.py - run this file to start scraping.

before running set up 2 factor authetication for your account. you can use google authenticator as your keystore.
The console will ask for a MFA(multi factor auth) code : use the keys from your keystore.

Write the mfa in the console, not the browser.

There will be exceptions in some sections. (We can't do anything about it, either it is private or fb is not showing it to us)

Keep an eye on the page as well as the console

(Keep a watch on the output in data folder, after a while the folders generated will be empty due to restrictions by FB)

3. present - the presentation folder from the last evaluation

=======contents=========

facebook : anonymised data

Facebook friend graph.ipynb : from the facebook-friend-graph

friend_graph.pickle : from the facebook-friend-graph

node_features.py : ML model to detect sensitive features base on data in facebook folder.[run this]

Rest of the Files : To be completed by NUNU and JAY.

