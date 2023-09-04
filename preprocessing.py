import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
def preprocess(X, y):

    def onehotencode(y_synth):
        y_synth = np.array(y_synth)
        start = y_synth[:,0]
        end = y_synth[:,1]
        pattern = y_synth[:,2]
        mapping = {
            0: [0, 0, 0, 0, 1],
            1: [0, 0, 0, 1, 0],
            2: [0, 0, 1, 0, 0],
            3: [0, 1, 0, 0, 0],
            4: [1, 0, 0, 0, 0]
        }
        mapped_values = [list(mapping[val]) for val in pattern]
        y_s = (np.column_stack((start, end, mapped_values)))
        return y_s

    y_preprocessed = onehotencode(y)
    X_train, X_test, y_train, y_test = train_test_split(X, y_preprocessed, test_size=0.2)

    y_train_dates = y_train[:,:2]
    y_test_dates = y_test[:,:2]
    y_train_p = y_train[:,2:]
    y_test_p = y_test[:,2:]

    X_train_processed=[]
    scale={}
    for i in range(len(X_train)):
        open_scaler_i = StandardScaler()
        X_train_processed.append(open_scaler_i.fit_transform(X_train[i]))
        scale[f"open_scaler_{len(X_train[i])}"] = open_scaler_i

    X_test_processed=[]
    scale={}
    for i in range(len(X_test)):
        open_scaler_i = StandardScaler()
        X_test_processed.append(open_scaler_i.fit_transform(X_test[i]))
        scale[f"open_scaler_{len(X_test[i])}"] = open_scaler_i

    x=[]

    for i in range(len(X_train)):
        x.append(len(X_train[i]))

    xx=[]

    for i in range(len(X_test_processed)):
        xx.append(len(X_test_processed[i]))

    maxlen = max(max(x), max(xx))

    X_train_preprocessed = pad_sequences(X_train_processed, maxlen = maxlen, dtype='float32', padding='post', value=-1)
    X_test_preprocessed = pad_sequences(X_test_processed, maxlen = maxlen, dtype='float32', padding='post', value=-1)

    X_train_preprocessed = tf.convert_to_tensor(X_train_preprocessed, np.float32)
    y_train_p = tf.convert_to_tensor(y_train_p, np.int16)
    y_train_dates = tf.convert_to_tensor(y_train_dates, np.int16)

    X_test_preprocessed = tf.convert_to_tensor(X_test_preprocessed, np.float32)
    y_test_p = tf.convert_to_tensor(y_test_p, np.int16)
    y_test_dates = tf.convert_to_tensor(y_test_dates, np.int16)

    return X_train_preprocessed, y_train_p, y_train_dates, X_test_preprocessed, y_test_p, y_test_dates
