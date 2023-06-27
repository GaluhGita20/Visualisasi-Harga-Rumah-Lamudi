import pandas as pd
import statsmodels.formula.api as smf
from sklearn.metrics import mean_squared_error
import numpy as np
import pickle

paths= 'D:/Web Data Viz/Visualisasi-Harga-Rumah-Lamudi/model/'
file_path_dataset = 'D:/Web Data Viz/Visualisasi-Harga-Rumah-Lamudi/static/data/data harga rumah clean baru.csv'
# Predict Data
def predict_linear_regression(data):
    with open(paths+'model_linear_regression.pkl', 'rb') as file:
        model = pickle.load(file)
    predictions = model.predict(data)
    return predictions

# Main Program
def mainprog(kabupaten, kamar_tidur, kamar_mandi, jmlh_lantai, luas_bangunan, luas_tanah):
    file_path = 'D:/Web Data Viz/Visualisasi-Harga-Rumah-Lamudi/static/data/Normalisasi Data Rumah.csv'
    data = pd.read_csv(file_path)
    #model = linear_regression(data, kabupaten)
    
    #Encoding Kabupaten Data
    #kabupaten = label_encode(kabupaten)

    #Scaling Data
    kamar_tidur = scl_trans_kamar_tidur(kamar_tidur)
    kamar_mandi = scl_trans_kamar_mandi(kamar_mandi)  
    luas_tanah = scl_trans_luas_tanah(luas_tanah)  
    luas_bangunan = scl_trans_luas_bangunan(luas_bangunan)
    jmlh_lantai = scl_trans_jumlah_lantai(jmlh_lantai)

    # Membuat data baru untuk prediksi
    new_data = pd.DataFrame({
        'kamar_tidur': [kamar_tidur],
        'kamar_mandi': [kamar_mandi],
        'jmlh_lantai': [jmlh_lantai],
        'luas_bangunan': [luas_bangunan],
        'luas_tanah': [luas_tanah],
        'kabupaten':[kabupaten]
    })

    # Menggunakan model regresi linear untuk melakukan prediksi
    predictions = predict_linear_regression(new_data)
    filtered_data = data[data['kabupaten'] == kabupaten]
    filter_data_min = filtered_data[(filtered_data['harga'] <= predictions[0][0])]
    filter_data_min = filter_data_min.sort_values('harga', ascending=False).head(5)
    filter_data_max = filtered_data[(filtered_data['harga'] >= predictions[0][0])]
    filter_data_max = filter_data_max.sort_values('harga',ascending=True).head(5)
    df_concat = pd.concat([filter_data_min,filter_data_max],axis=0)

    #Inverse Scaling Rekomendasi Data
    df_concat['kabupaten'] = df_concat['kabupaten'].apply(lambda x : label_decode_kab(x))
    df_concat['parkir_motor'] = df_concat['parkir_motor'].apply(lambda x : scl_inv_parkir_motor(x))
    df_concat['jmlh_lantai'] = df_concat['jmlh_lantai'].apply(lambda x : scl_inv_jumlah_lantai(x))
    df_concat['kamar_tidur'] = df_concat['kamar_tidur'].apply(lambda x : scl_inv_kamar_tidur(x))
    df_concat['kamar_mandi'] = df_concat['kamar_mandi'].apply(lambda x : scl_inv_kamar_mandi(x))
    df_concat['luas_tanah'] = df_concat['luas_tanah'].apply(lambda x : scl_inv_luas_tanah(x))
    df_concat['luas_bangunan'] = df_concat['luas_bangunan'].apply(lambda x : scl_inv_luas_bangunan(x))
    df_concat['harga'] = df_concat['harga'].apply(lambda x : scl_inv_harga(x))

    #inverse Scaling Prediksi
    #{:,.0f}
    predict = scl_inv_harga(predictions[0][0])
    
    #filtered_data = filtered_data[(filtered_data['harga'] >= predictions.min()) | (filtered_data['harga'] <= predictions.max())].head(10)
    #filtered_data = filtered_data[(filtered_data['harga'].between(predictions - 10000000, predictions + 10000000, inclusive=True))].head(5)
    return predict,df_concat

# predict di semua kabupaten dengan parameter yang sama
def mecprog(kamar_tidur, kamar_mandi, jmlh_lantai, luas_bangunan, luas_tanah):
    file_path = 'D:/Web Data Viz/Visualisasi-Harga-Rumah-Lamudi/static/data/Normalisasi Data Rumah.csv'
    data = pd.read_csv(file_path)
    #model = linear_regression(data, kabupaten)
    
    #Encoding Kabupaten Data
    #kabupaten = label_encode(kabupaten)

    #Scaling Data
    hasil =[]
    kab =[]
    kamar_tidur = scl_trans_kamar_tidur(kamar_tidur)
    kamar_mandi = scl_trans_kamar_mandi(kamar_mandi)  
    luas_tanah = scl_trans_luas_tanah(luas_tanah)  
    luas_bangunan = scl_trans_luas_bangunan(luas_bangunan)
    jmlh_lantai = scl_trans_jumlah_lantai(jmlh_lantai)
    for x in range(0,8):
    # Membuat data baru untuk prediksi
        new_data = pd.DataFrame({
            'kamar_tidur': [kamar_tidur],
            'kamar_mandi': [kamar_mandi],
            'jmlh_lantai': [jmlh_lantai],
            'luas_bangunan': [luas_bangunan],
            'luas_tanah': [luas_tanah],
            'kabupaten':[x]
        })
        predictions = predict_linear_regression(new_data)
        predict = scl_inv_harga(predictions[0][0])
        kabupaten = label_decode_kab(x)
        hasil.append(int(predict))
        kab.append(kabupaten.upper())

    df = pd.DataFrame({"kabupaten":kab, "hasil_prediksi":hasil})
    #df["hasil prediksi"].sort_values(ascending=True)
    df_sorted = df.sort_values(by="hasil_prediksi" , ascending=True)
    json_d = df_sorted.to_json(orient="records")
    return json_d
    #return df.sort_values(by="Hasil Prediksi" , ascending=True)

#Training Model gak dipakai
def linear_regression(data, kabupaten):
    house_data = data[data['kabupaten'] == kabupaten]
    y = house_data['harga']
    x = house_data[['kamar_tidur', 'kamar_mandi', 'jmlh_lantai', 'luas_bangunan', 'luas_tanah']]
    model = smf.ols(formula=f'{y.name} ~ {x.columns.str.cat(sep=" + ")}', data=house_data).fit()
    return model

# Inverse Scaling Data
def scl_inv_luas_tanah(data):
    with open(paths+'skala_luas_tanah.pkl', 'rb') as file:
        sclTh = pickle.load(file)
    data=sclTh.inverse_transform(np.array(data).reshape(-1,1))
    return int(np.ceil(data))

def scl_inv_luas_bangunan(data):
    with open(paths+'skala_luas_bangunan.pkl', 'rb') as file:
        sclBg = pickle.load(file)
    data=sclBg.inverse_transform(np.array(data).reshape(-1,1))
    return int(np.ceil(data))

def scl_inv_kamar_mandi(data):
    with open(paths+'skala_kamar_mandi.pkl', 'rb') as file:
        sclKm = pickle.load(file)
    data=sclKm.inverse_transform(np.array(data).reshape(-1,1))
    return int(np.ceil(data))

def scl_inv_kamar_tidur(data):
    with open(paths+'skala_kamar_tidur.pkl', 'rb') as file:
        sclKt = pickle.load(file)
    data=sclKt.inverse_transform(np.array(data).reshape(-1,1))
    return int(np.ceil(data))

def scl_inv_jumlah_lantai(data):
    with open(paths+'skala_jmlh_lantai.pkl', 'rb') as file:
        sclLt = pickle.load(file)
    data=sclLt.inverse_transform(np.array(data).reshape(-1,1))
    return int(np.ceil(data))

def scl_inv_parkir_motor(data):
    with open(paths+'skala_parkir_motor.pkl', 'rb') as file:
        sclMtr = pickle.load(file)
    data=sclMtr.inverse_transform(np.array(data).reshape(-1,1))
    return int(np.ceil(data))

def scl_inv_harga(data):
    with open(paths+'skala_harga.pkl', 'rb') as file:
        sclHarga = pickle.load(file)
    val = sclHarga.inverse_transform(np.array(data).reshape(-1,1))
    return val[0][0]

# Scaling Transform
def scl_trans_luas_tanah(data):
    with open(paths+'skala_luas_tanah.pkl', 'rb') as file:
        sclTh = pickle.load(file)
    data=sclTh.transform(np.array(data).reshape(-1,1))
    return data

def scl_trans_luas_bangunan(data):
    with open(paths+'skala_luas_bangunan.pkl', 'rb') as file:
        sclBg = pickle.load(file)
    data=sclBg.transform(np.array(data).reshape(-1,1))
    return data

def scl_trans_kamar_mandi(data):
    with open(paths+'skala_kamar_mandi.pkl', 'rb') as file:
        sclKm = pickle.load(file)
    data=sclKm.transform(np.array(data).reshape(-1,1))
    return data

def scl_trans_kamar_tidur(data):
    with open(paths+'skala_kamar_tidur.pkl', 'rb') as file:
        sclKt = pickle.load(file)
    data=sclKt.transform(np.array(data).reshape(-1,1))
    return data

def scl_trans_jumlah_lantai(data):
    with open(paths+'skala_jmlh_lantai.pkl', 'rb') as file:
        sclLt = pickle.load(file)
    data=sclLt.transform(np.array(data).reshape(-1,1))
    return data

def label_decode_kab(kab):
    if kab ==0:
        kab='bangli'
    elif kab ==1:
        kab='jembrana'
    elif kab ==2:
        kab='karangasem'
    elif kab ==3:
        kab='buleleng'
    elif kab ==4:
        kab='gianyar'
    elif kab ==5:
        kab='tabanan'
    elif kab ==6:
        kab='badung'
    elif kab ==7:
        kab='denpasar'
    return kab

# df1= pd.read_csv(file_path_dataset)
# df1 = df1.groupby("kabupaten")["harga"].mean()
# data = pd.DataFrame({"kabupaten":df1.index, "harga":df1.values})
# for x in range(0,9):
#     print(df1.index[x].upper())

# data = data.sort_values(by="harga",ascending=True)
# print(data)

# def kabupaten(data):
#     kabupa

#testing 
# lt = int(input("masukakan luas tanah "))
# lb = int(input("masukan luas bangunan "))
# kmt = int(input("masukan kamar tidur "))
# kmd = int(input("masukakan kamar mandi "))
# lt1 = int(input("masukan jumlah lantai "))

# hasil = mecprog(kmt, kmd , lt1 , lb , lt)
# print(f"hasil prediksi harga rumah di semua kab yaitu {hasil}")


