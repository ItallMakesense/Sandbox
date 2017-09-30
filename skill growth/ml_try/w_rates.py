import numpy as np
import pandas as pd
import random
import pickle
from sklearn import preprocessing, metrics
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from skimage import io, transform, color, feature, exposure
from scipy import stats
import warnings


warnings.filterwarnings('ignore')

def rates_to_numbers(line):
    change = 0
    if isinstance(line, str):
        if line == 'G':
            change = 0.25
        elif line == 'PG':
            change = 0.5
        elif line == 'PG-13':
            change = 1
        elif line == 'R':
            change = 0.75
        else:
            change = 0
    else:
        change = line
    return change

data = pd.read_csv("/home/kirgenvall/task_2_data/train.csv")
predict_data = pd.read_csv("/home/kirgenvall/task_2_data/test.csv")

train_data = data.drop(['Language', 'Country', 'Poster'], axis=1)

train_data['Rating'] = train_data['Rating'].apply(rates_to_numbers)
train_data['Rating'].fillna(0, inplace=True)

y = train_data['Target']
X_train = train_data.iloc[:, 2:]
X_train = preprocessing.scale(X_train)

np.random.seed(123)
x_train, x_test, y_train, y_test = train_test_split(X_train, y, test_size=0.2)



log_reg = LogisticRegression()
log_reg.fit(x_train, y_train)
log_reg_pred = log_reg.predict(x_test)

# print("\nFirst model\n", log_reg)
print(metrics.classification_report(y_test, log_reg_pred))
print(metrics.roc_auc_score(y_test, log_reg_pred), 'LogisticRegression')



gaus = GaussianNB()
gaus.fit(x_train, y_train)
gaus_pred = gaus.predict(x_test)

# print("\nSecond model\n", gaus)
print(metrics.classification_report(y_test, gaus_pred))
print(metrics.roc_auc_score(y_test, gaus_pred), 'GaussianNB')



knn = KNeighborsClassifier()
knn.fit(x_train, y_train)
knn_pred = knn.predict(x_test)

# print("\nThird model\n", knn)
print(metrics.classification_report(y_test, knn_pred))
print(metrics.roc_auc_score(y_test, knn_pred), 'KNeighborsClassifier')



trees = DecisionTreeClassifier()
trees.fit(x_train, y_train)
trees_pred = trees.predict(x_test)

# print("\nFourth model\n", trees)
print(metrics.classification_report(y_test, trees_pred))
print(metrics.roc_auc_score(y_test, trees_pred), 'DecisionTreeClassifier')



svc = SVC()
svc.fit(x_train, y_train)
svc_pred = svc.predict(x_test)

# print("\nFifth model", svc)
print(metrics.classification_report(y_test, svc_pred))
print(metrics.roc_auc_score(y_test, svc_pred), 'SVC')



r_forest = RandomForestClassifier()
r_forest.fit(x_train, y_train)
r_forest_pred = r_forest.predict(x_test)

# print("\nSixth model\n", r_forest)
print(metrics.classification_report(y_test, r_forest_pred))
print(metrics.roc_auc_score(y_test, r_forest_pred), 'RandomForestClassifier')

# 0.81615848753 LogisticRegression
# 0.680539018504 GaussianNB
# 0.794658085278 KNeighborsClassifier
# 0.754034593725 DecisionTreeClassifier
# 0.821448109413 SVC                                                      <- WIN
# 0.776082059533 RandomForestClassifier
