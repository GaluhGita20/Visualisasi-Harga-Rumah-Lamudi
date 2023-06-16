import pandas as pd
import statsmodels.formula.api as smf
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def predict_linear_regression(model, data):
    predictions = model.predict(data)
    return predictions


def mainprog(kabupaten, kamar_tidur, kamar_mandi, jmlh_lantai, luas_bangunan, luas_tanah):
    data = pd.read_csv('static/data/data harga rumah clean baru.csv')
    kabupaten = kabupaten
    model, y_pred, y_test = linear_regression(data, kabupaten)

    # Membuat data baru untuk prediksi
    new_data = pd.DataFrame({
        'kamar_tidur': [kamar_tidur],
        'kamar_mandi': [kamar_mandi],
        'jmlh_lantai': [jmlh_lantai],
        'luas_bangunan': [luas_bangunan],
        'luas_tanah': [luas_tanah]
    })

    # Menggunakan model regresi linear untuk melakukan prediksi
    predictions = predict_linear_regression(model, new_data)

    #evaluasi 
    mse, rmse, mape = calculate_metrics(y_test, y_pred)
    mse =print("MSE:", mse)
    rmse=print("RMSE:", rmse)
    mape=print("MAPE:", mape, '%')

    filtered_data = data[data['kabupaten'] == kabupaten]
    filtered_data = filtered_data[(filtered_data['harga'] >= predictions.min()) | (filtered_data['harga'] <= predictions.max())]
    #filtered_data = filtered_data[(filtered_data['harga'].between(predictions - 10000000, predictions + 10000000, inclusive=True))].head(5)
    return predictions, filtered_data, mse, rmse, mape

def linear_regression(data, kabupaten):
    house_data = data[data['kabupaten'] == kabupaten]
    y = house_data['harga']
    x = preprocessing(house_data[['kamar_tidur', 'kamar_mandi', 'jmlh_lantai', 'luas_bangunan', 'luas_tanah']])
    model = smf.ols(formula=f'{y.name} ~ {x.columns.str.cat(sep=" + ")}', data=house_data).fit()
    y_pred = model.predict(x)

    return model, y_pred, y

def preprocessing(X):    
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    variables = pd.DataFrame(X_scaled, columns=X.columns)
    return variables

def calculate_metrics(actual, predicted):
    # Menghitung Mean Squared Error (MSE)
    mse = np.mean((actual - predicted) ** 2)

    # Menghitung Root Mean Squared Error (RMSE)
    rmse = np.sqrt(mse)

    # Menghitung Mean Absolute Percentage Error (MAPE)
    mape = np.mean(np.abs((actual - predicted) / actual)) * 100

    return mse, rmse, mape



print(mainprog('buleleng', 2,1,1,36,100))
