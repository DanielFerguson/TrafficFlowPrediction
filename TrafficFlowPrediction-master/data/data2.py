"""
Processing the data
"""
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler,normalize

def process_data(file, lags):
    """Process data
    Reshape and split train\test data.
    # Arguments
        train: String, name of .csv train file.
        test: String, name of .csv test file.
        lags: integer, time lag.
    # Returns
        X_train: ndarray.
        y_train: ndarray.
        X_test: ndarray.
        y_test: ndarray.
        scaler: StandardScaler.
    """
    
#     read csv file
    df = pd.read_csv("data/{}".format(file), encoding='utf-8',header=None).fillna(0) # read data from csv

#   read all the vehicle/15min in one array   
    flow = np.array(df.iloc[:,3:]) # read all after third column which is traffic flow for a particular location
    flow = flow.ravel() # converting it to a 1D array

    
#     normalize all the values  
    scaler = MinMaxScaler(feature_range=(0, 1)).fit(flow.reshape(-1, 1)) # seting scaler data between 0 - 1 
    normalized_flow = scaler.transform(flow.reshape(-1, 1)).reshape(1, -1)[0] # scaling data between 0 - 1 
    

#     splitting the file into train and test dataset
    split = int(normalized_flow.shape[0] * 0.8)
    
    flow1 = normalized_flow[:split]
    flow2 = normalized_flow[split:]
    
    
    
    train, test = [], []
    for i in range(lags, len(flow1)): # creating flow with the number of lags provided for training
        train.append(flow1[i - lags: i + 1])
    for i in range(lags, len(flow2)): # creating test set
        test.append(flow2[i - lags: i + 1])

    train = np.array(train)
    test = np.array(test)
    np.random.shuffle(train)

    X_train = train[:, :-1]
    y_train = train[:, -1]
    X_test = test[:, :-1]
    y_test = test[:, -1]

    return X_train, y_train, X_test, y_test, scaler