# -*- coding: utf-8 -*-
"""Anjana Kuruwita_ML_Final_Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/12oZFA8O-RUzrECRO5yjEX94F2Fibz7en
"""

import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn
import seaborn as sns
import sklearn.tree as tree

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.metrics import accuracy_score
from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import KFold, StratifiedKFold,ShuffleSplit
from google.colab import files
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import train_test_split

import io

# Upload the first CSV file
uploaded_file_1 = files.upload()

# Upload the second CSV file
uploaded_file_2 = files.upload()

# Upload the second CSV file
uploaded_file_3 = files.upload()

# Read the first CSV file into a DataFrame
df1 = pd.read_csv(io.BytesIO(uploaded_file_1['results.csv']))

# Read the second CSV file into a DataFrame
df2 = pd.read_csv(io.BytesIO(uploaded_file_2['races.csv']))

# Read the second CSV file into a DataFrame
df3 = pd.read_csv(io.BytesIO(uploaded_file_3['circuits.csv']))

# Merge the DataFrames based on the 'id' column
merged_df = pd.merge(df1, df2, on='raceId', how='inner')

df = pd.merge(merged_df, df3, on='circuitId', how='inner')


# Display the merged DataFrame
#print(merged_df)

df.describe()

df.shape

for column_name, data_type in df.dtypes.items():
    print(f"Column '{column_name}' has data type: {data_type}")

df = df.drop(["resultId", "raceId", 'driverId', "constructorId", "number",'statusId', "statusId","circuitId"], axis=1)
df = df.drop(['lat','lng'], axis=1)
df = df.select_dtypes(exclude=['object'])
X = df.values
y = df["positionOrder"]

for column_name, data_type in df.dtypes.items():
    print(f"Column '{column_name}' has data type: {data_type}")

# Select relevant columns
selected_columns = ['grid', 'positionOrder', 'points', 'laps','year','round']
df_selected = df[selected_columns]

# Set up scatter plots for all pairs of variables with customized histograms
pd.plotting.scatter_matrix(df_selected, figsize=(12, 12), marker='o', alpha=0.6, grid=False,
                           diagonal='hist', hist_kwds={'bins': 20, 'color': 'green', 'edgecolor': 'black'})

# Show the plots
plt.show()

# Select relevant columns
selected_columns = ['grid', 'positionOrder', 'points', 'laps','year','round']
df_selected = df[selected_columns]

# Set up pair plots with Seaborn
sns.pairplot(df_selected, hue='positionOrder', palette='colorblind', markers='o')

# Show the plots
plt.show()

cor = np.corrcoef(X, rowvar=False)
plt.figure(figsize=(20, 10))
feature_names = ['grid', 'positionOrder', 'points', 'laps','year','round']
sns.heatmap(cor, annot=True, xticklabels=feature_names, yticklabels=feature_names)

plt.show()

"""PCA"""

from sklearn.decomposition import PCA
pca = PCA(0.96)
pca.fit(X)

pca.components_[0]

pca.explained_variance_ratio_

#standard scalar
scaler = StandardScaler()
X = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

pca = PCA(n_components=4)
pca.fit(X_train)
X_train = pca.transform(X_train)
X_test = pca.transform(X_test)

X_train.shape

est = LinearRegression()
est.fit(X_train, y_train)
y_pred = est.predict(X_test)

print(r2_score(y_test, y_pred))

"""Decision Trees Exploration"""

est = tree.DecisionTreeRegressor(max_depth=3)

est.fit(X_train, y_train)

y_pred = est.predict(X_test)

print("R2: ", r2_score(y_test, y_pred))

plt.figure(figsize=(20, 10))
_ = tree.plot_tree(est, feature_names=df.columns, filled=True)

plt.show()

# dtreeviz is a great visualization library for trees but it's not built into colab so you'll need to install it if you have not done so
!pip install dtreeviz

from dtreeviz import model

plt.figure(figsize=(10,10))

viz = model(est, X_train, y_train,
            feature_names=df.columns)

viz.view(fontname='monospace', scale=2)

"""MLP"""

est = MLPRegressor(hidden_layer_sizes=(4,4), activation="logistic", learning_rate_init=0.001, max_iter=1000)

est.fit(X_train, y_train)
y_pred = est.predict(X_test)
print(r2_score(y_test,y_pred))

from sklearn.model_selection import cross_val_score

cv_scores = cross_val_score(est, X_train, y_train, cv=5, scoring='r2')

print("Cross-Validation Scores:", cv_scores)
print("Mean R-squared:", np.mean(cv_scores))

"""Built In

"""

clf = DecisionTreeRegressor()
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

from sklearn.ensemble import BaggingRegressor
clf = BaggingRegressor(n_estimators=35)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print(r2_score(y_test, y_pred))

from sklearn.ensemble import RandomForestRegressor
clf = RandomForestRegressor(n_estimators=35)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print(r2_score(y_test, y_pred))

from sklearn.ensemble import AdaBoostRegressor
clf = AdaBoostRegressor(n_estimators=35)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print(r2_score(y_test, y_pred))

from sklearn.ensemble import GradientBoostingRegressor
clf = GradientBoostingRegressor(n_estimators=35)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)
print(r2_score(y_test, y_pred))

ests = [BaggingRegressor(), RandomForestRegressor(), AdaBoostRegressor(), GradientBoostingRegressor()]

for e in ests:
  e.fit(X_train, y_train)
  y_pred = e.predict(X_test)
  print(type(e), r2_score(y_test, y_pred))

"""Cross Validation"""

k = 10
y1 = np.random.randint(0, 10, size=X.shape[0])

cv1 = ShuffleSplit(n_splits = k, test_size= 0.2)
for train_index, test_index in cv1.split(X):
  print(train_index, "/", test_index)

cv2 = KFold(n_splits = k, shuffle=False)
for train_index, test_index in cv2.split(X):
  print(train_index, "/", test_index)

cv3 = StratifiedKFold(n_splits = k)
for train_index, test_index in cv3.split(X,y1):
  print(train_index, "/", test_index)

est = GradientBoostingRegressor(n_estimators=15)

# Use an appropriate scoring metric for regression, i.e 'r2'
scores1 = cross_val_score(est, X, y, scoring='r2', cv=cv1)
scores2 = cross_val_score(est, X, y, scoring='r2', cv=cv2)
scores3 = cross_val_score(est, X, y, scoring='r2', cv=cv3)

# Print the mean and standard deviation of the scores
print("Mean: ", np.mean(scores1))
print("SD: ", np.std(scores1))
print("Mean: ", np.mean(scores2))
print("SD: ", np.std(scores2))
print("Mean: ", np.mean(scores3))
print("SD: ", np.std(scores3))

gbr = GradientBoostingRegressor()

param_grid = {'n_estimators': [5, 15, 25, 35]}

grid_search = GridSearchCV(gbr, param_grid, scoring='r2', cv=cv1, n_jobs=-1)
grid_search.fit(X_train, y_train)

grid_search.cv_results_

grid_search.best_estimator_

"""As the number of estimators increases the rank increased as well"""