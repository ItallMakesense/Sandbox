"""
Usage:
	$: python task_2.py [path to files]
"""

import sys
import os.path
import warnings
import numpy as np
import pandas as pd
from sklearn import preprocessing, metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from skimage import io, transform, color, feature, exposure


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

def histogram(nbins, posters):
    hue = []
    saturation = []
    value = []
    for poster in posters:
        pic = io.imread("/home/kirgenvall/task_2_data/posters/%s" % poster)
        hsv = color.rgb2hsv(pic)
        hue.append(exposure.histogram(hsv[:, :, 0], nbins=nbins)[0])
        saturation.append(exposure.histogram(hsv[:, :, 1], nbins=nbins)[0])
        value.append(exposure.histogram(hsv[:, :, 2], nbins=nbins)[0])
    params = np.concatenate([hue, saturation, value], axis=1)
    return pd.DataFrame(preprocessing.normalize(params))

def prepare(data):
    posters = data['Poster']
    data = data.drop(['Language', 'Country', 'Poster'], axis=1)
    data['Rating'] = data['Rating'].apply(rates_to_numbers)
    data['Rating'].fillna(0, inplace=True)
    img_features = histogram(5, posters)
    return pd.concat([data, img_features], axis=1)



if __name__ == '__main__':

    warnings.filterwarnings('ignore')

    TRAIN_NAME = 'train.csv'
    TEST_NAME = 'test.csv'
    FILE_NAME = 'kirgenvall_task_2_prediction.csv'

    folder = sys.argv[1]

    train_data = pd.read_csv(os.path.join(folder, TRAIN_NAME))
    train_data = prepare(train_data)

### Training the model
    y = train_data['Target']
    X_train = preprocessing.scale(train_data.iloc[:, 2:])
    x_train, x_test, y_train, y_test = train_test_split(X_train, y, test_size=0.2,
                                                        random_state=123)
    log_reg = LogisticRegression(multi_class='multinomial', solver='newton-cg')
    log_reg.fit(x_train, y_train)
    check_predict = log_reg.predict(x_test)
    print("Area under the ROC-curve", metrics.roc_auc_score(y_test, check_predict))

### Getting results
    test_data = pd.read_csv(os.path.join(folder, TEST_NAME))
    test_data = prepare(test_data)

    prediction = log_reg.predict_proba(preprocessing.scale(test_data.iloc[:, 1:]))
    result = pd.DataFrame({'Probability': prediction[:, 1]}) # log_reg classes are 0 and 1. 1 is a Comedy
    result = pd.concat([test_data['Id'], result], axis=1)
    result.to_csv(os.path.join(folder, FILE_NAME))
