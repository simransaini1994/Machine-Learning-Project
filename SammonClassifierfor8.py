# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 03:18:14 2019

@author: ecs
"""
import numpy as np
from sklearn.svm import SVC
from sammon import sammon
import numpy as np
import pandas as pd
NoComp=15
data = pd.read_excel('Datasets/Gear15.xlsx')
# Dataset is now stored in a Pandas Dataframe
data = data.dropna(axis = 1, how ='all') 

#removing columns havin more than 90% zero
data=data.drop(columns=data.columns[((data==0).mean()>0.90)],axis=1)
data = data.drop_duplicates()
#print(data.info)

#saving lables in y
X_data= data.iloc[:,:-1].values
y_data=data.iloc[:,-1].values

#Normalization
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_data=sc.fit_transform(X_data)



from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2, random_state=0)
X_train, X_val, y_train, y_val   = train_test_split(X_train, y_train, test_size=0.2, random_state=1)


   # Run the Sammon projection
[X_train,E] = sammon(X_train, NoComp, maxhalves = 10, maxiter = 10)
#print(X_train.shape)
X_t = X_train.transpose()
COV = np.matmul(X_t,X_train)
from scipy import linalg as LA
e_vals, e_vecs = LA.eig(COV)
Variability=e_vals[NoComp-1]/sum(e_vals)

#print(X_train)
#print(X_test)
#print(y_test)
#print(y_train)
#COV = np.cov(X_train)
#print(COV.shape)


from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

#randomforest
classifier_randomforest=RandomForestClassifier()
param_grid_randomforest = {
    'max_depth': [100, 150,200],
    'n_estimators': [100,125,150]
}

#tuning paramter of random forest 
grid_search = GridSearchCV(estimator = classifier_randomforest, param_grid=param_grid_randomforest, cv = 10, n_jobs = -1, verbose = 2)
grid_search.fit(X_train,y_train)

optimal_classifier_randomforest=RandomForestClassifier(**grid_search.best_params_)
optimal_classifier_randomforest.fit(X_train, y_train)

Accuracy_rf = cross_val_score(optimal_classifier_randomforest, X_train, y_train, cv=10)
#print (Accuracy)
f1_score_rf=cross_val_score(optimal_classifier_randomforest, X_train, y_train, cv=10,scoring='f1_macro')
#print (f1_score)


# K-nn

from sklearn.neighbors import KNeighborsClassifier

classifier_knn=KNeighborsClassifier()
param_grid_knn = {
    'n_neighbors': [1,2,3,4,5]
}

#tuning parameter of knn
grid_search1 = GridSearchCV(estimator = classifier_knn, param_grid=param_grid_knn, cv = 10, n_jobs = -1, verbose = 2)
grid_search1.fit(X_train,y_train)

optimal_classifier_knn=KNeighborsClassifier(**grid_search1.best_params_)
optimal_classifier_knn.fit(X_train, y_train)

Accuracy_knn = cross_val_score(optimal_classifier_knn, X_train, y_train, cv=10)
#print (Accuracy)
f1_score_knn=cross_val_score(optimal_classifier_knn, X_train, y_train, cv=10,scoring='f1_macro')
#print (f1_score)



#Mlp Classifier
from sklearn.neural_network import MLPClassifier

classifier_mlp=MLPClassifier()
param_grid_mlp = {
    'activation': ['identity','relu','tanh','identity'],
    'solver':['lbfgs','sgd','adam'],
     'alpha':[1e-5]
}
grid_search2 = GridSearchCV(estimator = classifier_mlp, param_grid=param_grid_mlp, cv = 10, n_jobs = -1, verbose = 2)
#classifier_randomforest = RandomForestClassifier( max_depth=150, n_estimators=128 )
#classifier_knn= KNeighborsClassifier(n_neighbors=2 ,leaf_size=30)
grid_search2.fit(X_train,y_train)



optimal_classifier_mlp=MLPClassifier(**grid_search2.best_params_)
optimal_classifier_mlp.fit(X_train, y_train)

Accuracy_mlp = cross_val_score(optimal_classifier_mlp, X_train, y_train, cv=10)
#print (Accuracy)
f1_score_mlp=cross_val_score(optimal_classifier_mlp, X_train, y_train, cv=10,scoring='f1_macro')
#print (f1_score)


RBFClassifier = SVC(kernel='rbf')
param_grid_rbf = {
      'kernel':['rbf'],
     'gamma': [ 1e-4,0.00001],
                     'C': [1000,10000,100000]
                   
}

#tuning paramter of radial basis
grid_search3 = GridSearchCV(estimator = RBFClassifier, param_grid=param_grid_rbf, cv = 10, n_jobs = -1, verbose = 2)
grid_search3.fit(X_train,y_train)

optimal_classifier_rbf=SVC(**grid_search3.best_params_)
optimal_classifier_rbf.fit(X_train, y_train)
#y_pred3 = optimal_classifier_rbf.predict(X_test)
#cm3 = confusion_matrix(y_test, y_pred3)
#print(cn3)
#print('Accuracy using mlp ' + str(accuracy_score(y_test, y_pred3)))

Accuracy_rbf = cross_val_score(optimal_classifier_rbf, X_train, y_train, cv=10)
#print (Accuracy)
f1_score_rbf=cross_val_score(optimal_classifier_rbf, X_train, y_train, cv=10,scoring='f1_macro')

print("Variability ---", Variability)
print('Random Forest -----------')
print('optimal parameters: ',grid_search.best_params_)
best_result = grid_search.best_score_
print('Best result : ', best_result)
j=1
for i in Accuracy_rf:
  print ("Fold-"+ str(j)+" Accuracy - "+str(i))
  j=j+1

print ("mean accuracy-"+str(np.mean(Accuracy_rf)))

j=1
for i in f1_score_rf:
  print ("Fold-"+ str(j)+" F1-score- "+str(i))
  j=j+1
print ("mean f1-score-"+str(np.mean(f1_score_rf)))




print('k- Nearest  Neighbor -----------')
print('optimal parameters:',grid_search1.best_params_)
best_result1 = grid_search1.best_score_
print('Best result : ', best_result1)

j=1
for i in Accuracy_knn:
  print ("Fold-"+ str(j)+" Accuracy - "+str(i))
  j=j+1

print ("mean accuracy-"+str(np.mean(Accuracy_knn)))

j=1
for i in f1_score_knn:
  print ("Fold-"+ str(j)+" F1-score- "+str(i))
  j=j+1
print ("mean f1-score-"+str(np.mean(f1_score_knn)))




print('Multilayer Percceptron -----------')
print('optimal parameters: ', grid_search2.best_params_)
best_result2 = grid_search2.best_score_
print('Best result : ',best_result2)
j=1
for i in Accuracy_mlp:
  print ("Fold-"+ str(j)+" Accuracy - "+str(i))
  j=j+1

print ("mean accuracy-"+str(np.mean(Accuracy_mlp)))

j=1
for i in f1_score_mlp:
  print ("Fold-"+ str(j)+" F1-score- "+str(i))
  j=j+1
print ("mean f1-score-"+str(np.mean(f1_score_mlp)))


print('Radial Basis Function -----------')
print('optimal parameters: ', grid_search3.best_params_)
best_result3 = grid_search3.best_score_
print('Best result : ',best_result3)
j=1
for i in Accuracy_rbf:
  print ("Fold-"+ str(j)+" Accuracy - "+str(i))
  j=j+1

print ("mean accuracy-"+str(np.mean(Accuracy_rbf)))

j=1
for i in f1_score_rbf:
  print ("Fold-"+ str(j)+" F1-score- "+str(i))
  j=j+1
print ("mean f1-score-"+str(np.mean(f1_score_rbf)))





