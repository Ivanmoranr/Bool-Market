from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Masking, Conv1D, Flatten, MaxPooling1D
from tensorflow.keras import regularizers
import pandas as pd
from pathlib import Path

def create_data(pattern):
    DATA_PATH = Path(f"data/patterns/{pattern}")
    DATA_PATH.exists()

    if True:
        data = {filepath.stem: pd.read_csv(filepath) for filepath in DATA_PATH.glob("*.csv")}
    else:
        return None

    return data

def initialize_model_LSTM():
    model = Sequential()

    model.add(Masking(mask_value=-1, input_shape=(82,4)))
    model.add(LSTM(units=32, activation='relu'))

    model.add(Dense(units=16, activation='relu'))
    model.add(Dense(units=2, activation='linear'))

    model.compile(optimizer='adam', loss='mse', metrics=['mae'])

    return model

def initialize_model_C1D():
    model = Sequential()

    model.add(Masking(mask_value=-1, input_shape=(82,4)))
    model.add(Conv1D(32, activation='relu', kernel_size=3, kernel_regularizer=regularizers.L1L2(l1=1e-3, l2=1e-3))),
    model.add(MaxPooling1D(pool_size=2))
    model.add(Conv1D(32, activation='relu', kernel_size=3))

    model.add(Flatten())
    model.add(Dense(units=16, activation='relu'))
    model.add(Dense(units=16, activation='relu'))
    model.add(Dense(units=2, activation='linear'))

    model.compile(optimizer='adam', loss='mse', metrics=['mae'])

    return model
