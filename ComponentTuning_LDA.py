# -*- coding: utf-8 -*-
"""
Created on Sun Jul 21 12:03:16 2019

@author: simran
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 21:29:52 2019

@author: simran
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
sc = StandardScaler()

data= pd.read_excel('Datasets/Gear1.xlsx')
data = data.dropna(axis = 1, how ='all') 

data=data.drop(columns=data.columns[((data==0).mean()>0.90)],axis=1)
#print(data.info)

X_data= data.iloc[:,:-1].values
y_data=data.iloc[:,-1].values


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2, random_state=0)

X_train=sc.fit_transform(X_train)
X_test= sc.transform(X_test)
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA

#
accuracy_score = []
for k in range(1,15):
    X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.2, random_state=0)

    X_train=sc.fit_transform(X_train)
    X_test= sc.transform(X_test)
    lda = LDA(n_components=k)
    X_train = lda.fit_transform(X_train, y_train)
    X_test = lda.transform(X_test)

#
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import GridSearchCV
    
    classifier_randomforest=RandomForestClassifier()    
    param_grid_randomforest = {
    'max_depth': [100, 150,200],
    'n_estimators': [100,125,150]
    }
    grid_search = GridSearchCV(estimator = classifier_randomforest, param_grid=param_grid_randomforest, cv = 2, n_jobs = -1,verbose = 2)

    grid_search.fit(X_train,y_train)
    print(grid_search.best_params_)
    best_result = grid_search.best_score_
    accuracy_score.append(str(k)+': '+str(best_result))
print(accuracy_score)
    
    
    
    
    
    







