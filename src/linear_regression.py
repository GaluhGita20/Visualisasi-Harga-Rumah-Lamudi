import pandas as pd
import statsmodels.formula.api as smf
from sklearn.metrics import mean_squared_error


# Predict Data
def predict_linear_regression(model, data):
    predictions = model.predict(data)
    return predictions

# Main Program
def mainprog(kabupaten, kamar_tidur, kamar_mandi, jmlh_lantai, luas_bangunan, luas_tanah):
    file_path = 'D:/Web Data Viz/Visualisasi-Harga-Rumah-Lamudi/static/data/data harga rumah clean baru.csv'
    data = pd.read_csv(file_path)
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
    filter_data_min = filtered_data[(filtered_data['harga'] <= predictions.max())]
    filter_data_min = filter_data_min.sort_values('harga', ascending=False).head(5)
    filter_data_max = filtered_data[(filtered_data['harga'] >= predictions.min())]
    filter_data_max = filter_data_max.sort_values('harga',ascending=True).head(5)
    df_concat = pd.concat([filter_data_min,filter_data_max],axis=0)
    
    #filtered_data = filtered_data[(filtered_data['harga'] >= predictions.min()) | (filtered_data['harga'] <= predictions.max())].head(10)
    #filtered_data = filtered_data[(filtered_data['harga'].between(predictions - 10000000, predictions + 10000000, inclusive=True))].head(5)
    return predictions, df_concat

#Training Model
def linear_regression(data, kabupaten):
    house_data = data[data['kabupaten'] == kabupaten]
    y = house_data['harga']
    x = house_data[['kamar_tidur', 'kamar_mandi', 'jmlh_lantai', 'luas_bangunan', 'luas_tanah']]
    model = smf.ols(formula=f'{y.name} ~ {x.columns.str.cat(sep=" + ")}', data=house_data).fit()
    return model

# #testing 
# lt = int(input("masukakan luas tanah "))
# lb = int(input("masukan luas bangunan "))
# kmt = int(input("masukan kamar tidur "))
# kmd = int(input("masukakan kamar mandi "))
# lt1 = int(input("masukan jumlah lantai "))
# kab = str(input("masukan kabupaten "))

# hasil = mainprog(kab , kmt, kmd , lt1 , lb , lt)
# print(f"hasil prediksi harga rumah di kabupaten {kab} yaitu {hasil}")


