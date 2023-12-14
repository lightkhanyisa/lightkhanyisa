import numpy as np 

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split 
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score 


data=load_breast_cancer()
X,y=data.data,data.target

X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.2)
tree_list=[]
n_trees =10

for i in range(n_trees):
	tree=DecisionTreeClassifier(max_features='sqrt')
	subset_indices=np.random.choice(np.arange(len(X_train)),size=len(X_train)//2)
	X_train_subset=X_train[subset_indices]
	y_train_subset=y_train[subset_indices]
	tree.fit(X_train_subset,y_train_subset)
	tree_list.append(tree)

predictions=[]

for i,tree in enumerate(tree_list):
	individual_preds=tree.predict(X_test)
	individual_acc=accuracy_score(y_test,individual_preds)
	predictions.append(individual_preds)
	print(f'tree{i+1}==accuracy_score:{individual_acc}====')

##average the predictions
predictions=np.array(predictions)
ensemble_preds=np.round(np.mean(predictions,axis=0))

ensemble_acc=accuracy_score(y_test,ensemble_preds)

print(f'ensemble accuracy_score:{ensemble_acc}====')

rand_clf=RandomForestClassifier(n_estimators=100)
rand_clf.fit(X_train,y_train)

rand_preds=rand_clf.predict(X_test)
print(f'==random clf accuracy_score:{accuracy_score(y_test,rand_preds)}====')





