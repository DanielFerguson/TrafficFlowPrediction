"""
Train the NN model.
"""
import sys
import warnings
import argparse
import os
import numpy as np
import pandas as pd
from data.data2 import process_data
from model import model
from keras.models import Model
from keras.callbacks import EarlyStopping
warnings.filterwarnings("ignore")


def train_model(model, X_train, y_train, name, config):
    """train
    train a single model.

    # Arguments
        model: Model, NN model to train.
        X_train: ndarray(number, lags), Input data for train.
        y_train: ndarray(number, ), result data for train.
        name: String, name of model.
        config: Dict, parameter for train.
    """

    model.compile(loss="mse", optimizer="rmsprop", metrics=['mape'])
    # early = EarlyStopping(monitor='val_loss', patience=30, verbose=0, mode='auto')
    hist = model.fit(
        X_train, y_train,
        batch_size=config["batch"],
        epochs=config["epochs"],
        validation_split=0.05)

    model.save('model/' + name + '.h5') # saving the model
    df = pd.DataFrame.from_dict(hist.history)
    df.to_csv('model/' + name + ' loss.csv', encoding='utf-8', index=False) # storing loss values


def train_seas(models, X_train, y_train, name, config):
    """train
    train the SAEs model.

    # Arguments
        models: List, list of SAE model.
        X_train: ndarray(number, lags), Input data for train.
        y_train: ndarray(number, ), result data for train.
        name: String, name of model.
        config: Dict, parameter for train.
    """

    temp = X_train
    # early = EarlyStopping(monitor='val_loss', patience=30, verbose=0, mode='auto')

    for i in range(len(models) - 1):
        if i > 0:
            p = models[i - 1]
            hidden_layer_model = Model(input=p.input,
                                       output=p.get_layer('hidden').output)
            temp = hidden_layer_model.predict(temp)

        m = models[i]
        m.compile(loss="mse", optimizer="rmsprop", metrics=['mape'])

        m.fit(temp, y_train, batch_size=config["batch"],
              epochs=config["epochs"],
              validation_split=0.05)

        models[i] = m

    saes = models[-1]
    for i in range(len(models) - 1):
        weights = models[i].get_layer('hidden').get_weights()
        saes.get_layer('hidden%d' % (i + 1)).set_weights(weights)

    train_model(saes, X_train, y_train, name, config)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="lstm", help="Model to train.")
    parser.add_argument("--lag", default="12", help="specify number of lags")
    parser.add_argument(
        "--file_name", default="970_1_data.csv", help="Csv file name")
    args = parser.parse_args()

    lag = int(args.lag)
    config = {"batch": 256, "epochs": 600} # training config
    file = args.file_name
    model_name = os.path.splitext(file)[0]
    X_train, y_train, _, _, _ = process_data(file, lag)

    if args.model == 'lstm':
        m = model.get_lstm([[3, lag], 64, 64, 1]) # changing the input to 3, lags for rain data model
        train_model(m, X_train, y_train, "{}_lstm".format(model_name), config)
    if args.model == 'gru':
        m = model.get_gru([[3, lag], 64, 64, 1])
        train_model(m, X_train, y_train, "{}_gru".format(model_name), config) # changing the input to 3, lags for rain data model


if __name__ == '__main__':
    main(sys.argv)
