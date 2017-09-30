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
        # if line == 'G':
        #     change = 0.25
        # elif line == 'PG':
        #     change = 0.5
        # elif line == 'PG-13':
        #     change = 1
        # elif line == 'R':
        #     change = 0.75
        # else:
        #     change = 0

        change = 1 / len(line)
    else:
        change = line
    return change

train_data = pd.read_csv("/home/kirgenvall/task_2_data/train.csv")
predict_data = pd.read_csv("/home/kirgenvall/task_2_data/test.csv")

posters = train_data['Poster']

def histogram(nbins):
    hue = []
    saturation = []
    value = []
    for poster in posters:
        pic = io.imread("/home/kirgenvall/task_2_data/posters/%s" % poster)
        hsv = color.rgb2hsv(pic)
        hue.append(exposure.histogram(hsv[: ,: , 0], nbins=nbins)[0])
        saturation.append(exposure.histogram(hsv[: ,: , 1], nbins=nbins)[0])
        value.append(exposure.histogram(hsv[: ,: , 2], nbins=nbins)[0])
    img_feats = np.concatenate([hue, saturation, value], axis=1)
    scaled = pd.DataFrame(preprocessing.normalize(img_feats))
    print(scaled)
    return scaled

train_data_original = train_data.drop(['Language', 'Country', 'Poster'], axis=1)
predict_data = predict_data.drop(['Language', 'Country', 'Poster'], axis=1)

train_data_original['Rating'] = train_data_original['Rating'].apply(rates_to_numbers)
predict_data['Rating'] = predict_data['Rating'].apply(rates_to_numbers)

train_data_original['Rating'].fillna(0, inplace=True)
predict_data['Rating'].fillna(0, inplace=True)


# for n in range(1,65):
train_pics = histogram(4)
print(train_data_original.shape, train_pics.shape)
train_data = pd.concat([train_data_original, train_pics], axis=1)

# train_data = train_data_original
y = train_data['Target']
X_train = train_data.iloc[:, 2:]
X_pred = predict_data.iloc[:, 1:]

X_train = preprocessing.normalize(X_train)
X_pred = preprocessing.normalize(X_pred)

np.random.seed(123)
x_train, x_test, y_train, y_test = train_test_split(X_train, y, test_size=0.2)



log_reg = LogisticRegression()
log_reg.fit(x_train, y_train)
log_reg_pred = log_reg.predict(x_test)

print(metrics.roc_auc_score(y_test, log_reg_pred), 'LogisticRegression')
