"""
Traffic Flow Prediction with Neural Networks(SAEs、LSTM、GRU).
"""
import math
import warnings
import numpy as np
import pandas as pd
from data.data2 import process_data
from keras.models import load_model
from keras.utils.vis_utils import plot_model
import sklearn.metrics as metrics
import matplotlib as mpl
import matplotlib.pyplot as plt
import argparse
import pickle
import xgboost as xgb
import os

warnings.filterwarnings("ignore")


def MAPE(y_true, y_pred):
    """Mean Absolute Percentage Error
    Calculate the mape.

    # Arguments
        y_true: List/ndarray, ture data.
        y_pred: List/ndarray, predicted data.
    # Returns
        mape: Double, result data for train.
    """

    y = [x for x in y_true if x > 0]
    y_pred = [y_pred[i] for i in range(len(y_true)) if y_true[i] > 0]

    num = len(y_pred)
    sums = 0

    for i in range(num):
        tmp = abs(y[i] - y_pred[i]) / y[i]
        sums += tmp

    mape = sums * (100 / num)

    return mape


def eva_regress(y_true, y_pred):
    """Evaluation
    evaluate the predicted resul.

    # Arguments
        y_true: List/ndarray, ture data.
        y_pred: List/ndarray, predicted data.
    """

    mape = MAPE(y_true, y_pred)
    vs = metrics.explained_variance_score(y_true, y_pred)
    mae = metrics.mean_absolute_error(y_true, y_pred)
    mse = metrics.mean_squared_error(y_true, y_pred)
    r2 = metrics.r2_score(y_true, y_pred)
    print('explained_variance_score:%f' % vs)
    print('mape:%f%%' % mape)
    print('mae:%f' % mae)
    print('mse:%f' % mse)
    print('rmse:%f' % math.sqrt(mse))
    print('r2:%f' % r2)


def plot_results(y_true, y_preds, names):
    """Plot
    Plot the true data and predicted data.

    # Arguments
        y_true: List/ndarray, ture data.
        y_pred: List/ndarray, predicted data.
        names: List, Method names.
    """
    d = '2006-10-25 19:00'
    x = pd.date_range(d, periods=384, freq='15min')

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(x, y_true, label='True Data')
    for name, y_pred in zip(names, y_preds):
        ax.plot(x, y_pred, label=name)

    plt.legend()
    plt.grid(True)
    plt.xlabel('Time of Day')
    plt.ylabel('Flow')

    date_format = mpl.dates.DateFormatter("%H:%M")
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()

    plt.show()


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--lag", default="12", help="lags")
    parser.add_argument("--model", default="970_1_data.csv", help="csv file name for the model")   
    args = parser.parse_args()
    lag = int(args.lag)
    model_name = args.model
    model_name = os.path.splitext(model_name)[0] # getting model name

    # load all the models
    lstm = load_model('model/lstm.h5')
    gru = load_model('model/gru.h5')
    saes = load_model('model/saes.h5')
    knn = pickle.load(open('model/knn.model', 'rb'))
    xgboost = xgb.Booster({'nthread': 4})  # init model
    xgboost.load_model('model/xgb.model')
    models = [lstm, gru, saes,knn,xgboost]
    names = ['LSTM', 'GRU', 'SAEs','KNN','Xgboost']

    lag = 12
    file = '970_1_data.csv'
    _, _, X_test, y_test, scaler = process_data(file, lag)
    print(y_test.shape)
    y_test = scaler.inverse_transform(y_test.reshape(-1, 1)).reshape(1, -1)[0]
    print(y_test.shape)

    y_preds = []
    for name, model in zip(names, models):
         _, _, X_test, _,_ = process_data(file, lag)
        if name == 'SAEs':
            X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1]))
        elif name == 'GRU' or name == 'LSTM':
            X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        elif name == 'Xgboost':
            X_test = xgb.DMatrix(X_test)
        # file = 'images/' + name + '.png'
        # plot_model(model, to_file=file, show_shapes=True)
        predicted = model.predict(X_test)
        predicted = scaler.inverse_transform(predicted.reshape(-1, 1)).reshape(1, -1)[0]
        y_preds.append(predicted[:384]) # append all the prediction results
        print(name)
        eva_regress(y_test, predicted)

    plot_results(y_test[: 384], y_preds, names)


if __name__ == '__main__':
    main()
