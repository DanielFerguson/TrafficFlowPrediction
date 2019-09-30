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
    df = pd.read_csv("/Users/ditlswin/Documents/rkaul/traffic_flow_predi/TrafficFlowPrediction-master/data/{}".format(file), encoding='utf-8',header=None).fillna(0)

    df2 = pd.read_csv("/Users/ditlswin/Documents/rkaul/traffic_flow_predi/TrafficFlowPrediction-master/data/rain_weekend.csv", encoding='utf-8').fillna(0)
   
    weekend = list(df2['weekend'])
    rainfall_data = list(df2['rain_mm'])
  
    weekend = list([item]*96 for item in weekend)
    weekend = np.array(weekend)  
    weekend = weekend.ravel()
    
  
    rainfall_data = list([item]*96 for item in rainfall_data)
    rainfall_data = np.array(rainfall_data)  
    rainfall_data = rainfall_data.ravel()


    
#   read all the vehicle/15min in one array   
    flow = np.array(df.iloc[:,3:])
    flow = flow.ravel()


    
#     normalize all the values  
    scaler = MinMaxScaler(feature_range=(0, 1)).fit(flow.reshape(-1, 1))
    normalized_flow = scaler.transform(flow.reshape(-1, 1)).reshape(1, -1)[0]
    
#     append all data together
    normalized_flow = np.vstack([normalized_flow, rainfall_data,weekend])


#     splitting the file into train and test dataset
    split = int(normalized_flow.shape[1] * 0.8)
    
    flow1 = normalized_flow[:,:split]
    flow2 = normalized_flow[:,split:]
    
    
    train, test = [], []
    for i in range(lags, flow1.shape[1]):
        train.append(flow1[:,i - lags: i + 1])
    for i in range(lags, flow2.shape[1]):
        test.append(flow2[:,i - lags: i + 1])

    train = np.array(train)
    test = np.array(test)
    np.random.shuffle(train)

    X_train = train[:, :, :-1]
    y_train = train[:, 0, -1]
    X_test = test[:, :, :-1]
    y_test = test[:, 0, -1]

    return X_train, y_train, X_test, y_test, scaler