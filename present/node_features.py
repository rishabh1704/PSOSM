import lightgbm as lgb
from random import randint
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
import sys

def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

file = open('./facebook/0.feat', 'r')
Lines = file.readlines()

file2 = open('./facebook/0.featnames', 'r')
Lines2 = file2.readlines()

names = dict()

for l in Lines2:
	names[int(l.split()[0])] = l.split()[1:]

dataset = list()
y = list()
for line in Lines:
	dataset.append([int(x) for x in line.split()[1:]])
	y.append(randint(0, 1))

y = [0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1]

df = pd.DataFrame(dataset)
rat = int(0.8*len(y))
df_x = pd.DataFrame(dataset[:rat])
df_y = pd.DataFrame(y[:rat])

df_eval_x = pd.DataFrame(dataset[rat:])
df_eval_y = pd.DataFrame(y[rat:])

# gnb = GaussianNB()
gnb = LogisticRegression(random_state=0)
gnb.fit(df_x, df_y)
y_pred = gnb.predict(df_eval_x)

s = gnb.coef_[0]
ks = sorted(range(len(s)), key=lambda k: s[k])
top = 50
# print(ks[:30])

print("Removing the following features.")
print()
for jj in ks[:top]:
	print(names[jj])

rem = list(range(top))
j = [rem, ks[:top]]
ja = ['Unremoved : ', 'Removed : ']

print("\nInference Accuracies...\n")
for i, k in enumerate(j):
	gn = LogisticRegression(random_state=0)
	dff = df.drop(k, axis = 1)
	df_x0 = pd.DataFrame(dff[:rat])
	df_y0 = pd.DataFrame(y[:rat])

	df_eval_x0 = pd.DataFrame(dff[rat:])
	df_eval_y0 = pd.DataFrame(y[rat:])

	gn.fit(df_x0, df_y0)
	# y_pred0 = gn.predict(df_eval_x0)
	print(ja[i] + str(gn.score(df_eval_x0, df_eval_y0)))



# print(gnb.score(df_x, df_eval_x))
# print("unremoved")
# print(gnb.score(df_eval_x, df_eval_y))


sys.exit()
# the lightgbm

lgb_train = lgb.Dataset(df_x, df_y)
lgb_eval = lgb.Dataset(df_eval_x, df_eval_y, reference=lgb_train)


params = {
    'boosting_type': 'gbdt',
    'objective': 'binary',
    'metric': {'l2', 'l1'},
    'num_leaves': 13,
    'learning_rate': 0.1,
    'feature_fraction': 0.8,
    'bagging_fraction': 0.9,
    'bagging_freq': 5,
    # 'num_iteration' : 100,
    # 'max_bin' : 1000,
    'verbose': 0
}

gbm = lgb.train(params,
                lgb_train,
                num_boost_round=20,
                valid_sets=lgb_eval,
                early_stopping_rounds=5)

y_pred = gbm.predict(df_eval_x, num_iteration=gbm.best_iteration)

removal = list()
for i,k in enumerate(gbm.feature_importance()):
	if k != 0:
		print(i)
		removal.append(i)

for n in removal:
	print("removing index : " + str(n))
	# remove nth column
	dff = df.drop(removal, axis = 1)
	df_x = pd.DataFrame(dff[:rat])
	df_y = pd.DataFrame(y[:rat])

	df_eval_x = pd.DataFrame(dff[rat:])
	df_eval_y = pd.DataFrame(y[rat:])

	lgb_train = lgb.Dataset(df_x, df_y)
	lgb_eval = lgb.Dataset(df_eval_x, df_eval_y, reference=lgb_train)

	gbm = lgb.train(params,
                lgb_train,
                num_boost_round=20,
                valid_sets=lgb_eval,
                early_stopping_rounds=5)

	y_pred = gbm.predict(df_eval_x, num_iteration=gbm.best_iteration)
	print('The mse of prediction is :', mean_absolute_error(df_eval_y, y_pred))
	break


print('The mse of prediction is :', mean_absolute_error(df_eval_y, y_pred))
