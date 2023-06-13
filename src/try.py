import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

def predict_linear_regression(model, data):
    predictions = model.predict(data)  
    return predictions


def mainprog(kabupaten,kamar_tidur, kamar_mandi, jmlh_lantai, luas_bangunan, luas_tanah):
    data = pd.read_csv('static/data/data harga rumah clean baru.csv')
    kabupaten = kabupaten
    model= linear_regression(data, kabupaten)

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
    predictions = predictions


    filtered_data = data[data['kabupaten'] == kabupaten]
    # filtered_data = filtered_data[(filtered_data['harga'] >= int(predictions))]
    filtered_data = filtered_data[(filtered_data['harga'] >= int(predictions.min())) | (filtered_data['harga'] <= int(predictions.max()))]
    #filtered_data = filtered_data[(filtered_data['harga'].between(int(predictions) - 20000000, int(predictions) + 20000000, inclusive=True))].head(5)
    # filtered_data = filtered_data[(filtered_data['harga'].between(int(predictions) - 20000000, int(predictions) + 20000000, inclusive=True))].head(5)

    return predictions, filtered_data

def linear_regression(data, kabupaten):
   
    house_data = data[data['kabupaten'] == kabupaten]
    y = house_data['harga']
    x = house_data[['kamar_tidur', 'kamar_mandi', 'jmlh_lantai', 'luas_bangunan', 'luas_tanah']]
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

# Membuat objek model regresi linear
    model = LinearRegression()

# Melatih model menggunakan data latih
    model.fit(X_train, y_train)

# Memprediksi harga rumah menggunakan data uji
    y_pred = model.predict(X_test)
    # mse = mean_squared_error(y_test, y_pred)

    return model


print(mainprog('buleleng', 2,1,1,36,100))

