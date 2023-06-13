import pandas as pd
import statsmodels.formula.api as smf
from sklearn.metrics import mean_squared_error

def predict_linear_regression(model, data):
    predictions = model.predict(data)
    return predictions


def mainprog(kabupaten, kamar_tidur, kamar_mandi, jmlh_lantai, luas_bangunan, luas_tanah):
    data = pd.read_csv('static/data/data harga rumah clean baru.csv')
    kabupaten = kabupaten
    model = linear_regression(data, kabupaten)

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


    filtered_data = data[data['kabupaten'] == kabupaten]
    filtered_data = filtered_data[(filtered_data['harga'] >= predictions.min()) | (filtered_data['harga'] <= predictions.max())]
    #filtered_data = filtered_data[(filtered_data['harga'].between(predictions - 10000000, predictions + 10000000, inclusive=True))].head(5)
    return predictions, filtered_data

def linear_regression(data, kabupaten):
    house_data = data[data['kabupaten'] == kabupaten]
    y = house_data['harga']
    x = house_data[['kamar_tidur', 'kamar_mandi', 'jmlh_lantai', 'luas_bangunan', 'luas_tanah']]
    model = smf.ols(formula=f'{y.name} ~ {x.columns.str.cat(sep=" + ")}', data=house_data).fit()
    return model


#print(mainprog('buleleng', 2,1,1,36,100))

