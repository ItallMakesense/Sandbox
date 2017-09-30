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

def histogram(nbins):
    hue = []
    saturation = []
    value = []
    for poster in data['Poster']:
        pic = io.imread("/home/kirgenvall/task_2_data/posters/%s" % poster)
        hsv = color.rgb2hsv(pic)
        hue.append(exposure.histogram(hsv[: ,: , 0], nbins=nbins)[0])
        saturation.append(exposure.histogram(hsv[: ,: , 1], nbins=nbins)[0])
        value.append(exposure.histogram(hsv[: ,: , 2], nbins=nbins)[0])
    img_feats = np.concatenate([hue, saturation, value], axis=1)
    return pd.DataFrame(preprocessing.scale(img_feats))

train_data_original = data.drop(['Language', 'Country', 'Poster'], axis=1)
predict_data = predict_data.drop(['Language', 'Country', 'Poster'], axis=1)

train_data_original['Rating'] = train_data_original['Rating'].apply(rates_to_numbers)
predict_data['Rating'] = predict_data['Rating'].apply(rates_to_numbers)

train_data_original['Rating'].fillna(0, inplace=True)
predict_data['Rating'].fillna(0, inplace=True)

train_pics = histogram(32)
print(train_data_original.shape, train_pics.shape)
train_data = pd.concat([train_data_original, train_pics], axis=1)

y = train_data['Target']
X_train = train_data.iloc[:, 2:]
X_pred = predict_data.iloc[:, 1:]

X_train = preprocessing.scale(X_train)
X_pred = preprocessing.scale(X_pred)

np.random.seed(123)
x_train, x_test, y_train, y_test = train_test_split(X_train, y, test_size=0.2)


for k in range(5, train_data.shape[1]):
    knn = KNeighborsClassifier(n_neighbors=k)
    knn.fit(x_train, y_train)
    knn_pred = knn.predict(x_test)

    # print("\nThird model\n", knn)
    # print(metrics.classification_report(y_test, knn_pred))
    print(metrics.roc_auc_score(y_test, knn_pred), 'KNeighborsClassifier')
