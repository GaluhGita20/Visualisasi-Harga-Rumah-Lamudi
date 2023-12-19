from flask import Flask, jsonify, render_template, redirect,make_response,url_for, request
import pandas as pd
import numpy as np
import json
import pickle
from src.linear_regression import mainprog
from src.linear_regression import mecprog
from src.linear_regression import label_decode_kab

import locale
import pymysql

with open('model/model.pkl', 'rb') as file:
    model = pickle.load(file)
app = Flask(__name__)

mydb = pymysql.connect(
    host ='localhost',
    user='root',
    passwd='',
    database='rumah'
)

#Reading data

file_path_dataset = 'static/data/data harga rumah clean baru.csv'
file_path_heatmap = 'static/data/heatmap_data.csv'
data_df = pd.read_csv(file_path_dataset)
data_heatmap = pd.read_csv(file_path_heatmap)

@app.route('/')
def index():
    datas =  data_df.groupby('luas_bangunan')['harga'].mean().reset_index()
    grouped_dict =  datas.to_dict(orient='list')
    #my_dict = {key: value for key, value in zip(grouped_dict['luas_bangunan'], grouped_dict['harga'])}
    datas = datas[datas['harga'] == 1000000000000000000000000000]
    d = data_df.groupby("kabupaten")["harga"].mean()
    kabs=[]
    harga =[]
    for x in range(0,8):
        kabs.append(d.index[x].upper())
        harga.append(int(d.values[x]))

    d1 = pd.DataFrame({"kabupaten":kabs, "hasil_prediksi":harga})
    d1 = d1.sort_values(by="hasil_prediksi",ascending=True)
    d1 = d1.to_json(orient="records")
    d1= json.loads(d1)

    # Mengubah objek Python menjadi JSON tanpa escape
    jsd = json.dumps(d1)
    return render_template('form.html',values=[datas,jsd,datas])


#Predict Data
@app.route('/predict', methods=['POST'])
def predict():
    values = request.values
    kabs = label_decode_kab(int(values['kabupaten']))

    # predict di 1 kabupaten
    d = mecprog(int(values['kamar_tidur']), int(values['kamar_mandi']), int(values['jmlh_lantai']), int(values['luas_bangunan']), int(values['luas_tanah'])) 
    js= json.loads(d)

    # Mengubah objek Python menjadi JSON tanpa escape
    jsd = json.dumps(js)

    predict, val = mainprog(int(values['kabupaten']), int(values['kamar_tidur']), int(values['kamar_mandi']), int(values['jmlh_lantai']), int(values['luas_bangunan']), int(values['luas_tanah'])) 
    #dimatikan sementara
    df1 = pd.DataFrame([[kabs , int(values['luas_tanah']) , int(values['luas_bangunan']), int(values['kamar_tidur']), int(values['kamar_mandi']),int(values['jmlh_lantai'])]],columns=[["kabupaten","luas_tanah","luas_bangunan","kamar_mandi","kamar_tidur","jumlah_lantai"]])

    if values !=None:
        query = "INSERT INTO prediksi (kabupaten , kamar_tidur , kamar_mandi , jumlah_lantai ,luas_bangunan , luas_tanah ,harga) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        values = (kabs, int(values['kamar_tidur']), int(values['kamar_mandi']), int(values['jmlh_lantai']), int(values['luas_bangunan']), int(values['luas_tanah']), int(predict))
        mycursor = mydb.cursor()
        mycursor.execute(query,values)
        mydb.commit()

    # predict di semua kabupaten

    #parameter input
    #pd.DataFrame({"kabupaten":kabs, "luas_tanah":int(values['luas_tanah']),"luas_bangunan":int(values['luas_bangunan']), "kamar_mandi":int(values['kamar_mandi']),"kamar_tidur":int(values['kamar_tidur']),"jmlh_lantai":int(values['jmlh_lantai'])})
    # return df1
    return render_template('form.html',prediction_text='Hasil Prediksi Harga Rumah : Rp. {:,.0f} '.format(int(predict)),values=[val,jsd,df1])
    #return jsd

@app.route('/heatmap')
def heatmap():
    d = data_df.groupby("kabupaten")["harga"].mean()
    kabs=[]
    harga =[]
    for x in range(0,8):
        kabs.append(d.index[x].upper())
        harga.append(int(d.values[x]))

    d1 = pd.DataFrame({"kabupaten":kabs, "hasil_prediksi":harga})
    d1 = d1.sort_values(by="hasil_prediksi",ascending=True)
    d1 = d1.to_json(orient="records")
    d1= json.loads(d1)

    # Mengubah objek Python menjadi JSON tanpa escape
    jsd = json.dumps(d1)
    return render_template('heatmap.html', values=[jsd])


@app.route('/get_heatmap_data')
def get_heatmap_data():
    # Convert DataFrame to dictionary
    data_dict = [
        { 'group': 'A', 'variable': 'v1', 'value': 30 },
        { 'group': 'A', 'variable': 'v2', 'value': 95 },
    ]
    return jsonify(data_dict)

@app.route('/scatter')
def scatter():
    return render_template('scatter.html')

@app.route('/get_scatterplot_dataLB')
def get_scatterplot_dataLB():
    datas =  data_df.groupby('luas_bangunan')['harga'].mean().reset_index()
    grouped_dict =  datas.to_dict(orient='list')
    my_dict = {key: value for key, value in zip(grouped_dict['luas_bangunan'], grouped_dict['harga'])}
    return jsonify(my_dict)

@app.route('/get_scatterplot_dataLT')
def get_scatterplot_dataLT():
    datas =  data_df.groupby('luas_tanah')['harga'].mean().reset_index()
    grouped_dict =  datas.to_dict(orient='list')
    my_dict = {key: value for key, value in zip(grouped_dict['luas_tanah'], grouped_dict['harga'])}
    return jsonify(my_dict)

def calculate_frekuensi(val, total):
    """Calculates the percentage of a value over a total"""
    percent = np.round((np.divide(val, total) * total), 2)
    return percent

def data_creation(data, percent, class_labels, group=None):
    for index, item in enumerate(percent):
        data.append(item)

@app.route('/lolipop')
def lolipop():
    return render_template('lolipop.html')

@app.route('/get_lolipopchart_data')
def get_lolipopchart_data():
    contract_labels = data_df['kabupaten'].value_counts().index.to_list()
    churn_df = data_df[(data_df['kabupaten'].isin(contract_labels))]
    _ = churn_df.groupby('kabupaten').size().values
    #Getting the value counts and total
    class_percent = calculate_frekuensi(_, np.sum(_)) 

    piechart_data= []
    data_creation(piechart_data, class_percent, contract_labels)
    my_dict = {key: value for key, value in zip(contract_labels, piechart_data)}
    return jsonify(my_dict)

# hasil = pd.DataFrame([['tabanan',0,0,0,0,0,0]], columns =[['Kabupaten','Luas Tanah','Luas Bangunan','Kamar Tidur','Kamar Mandi','Jumlah Lantai','Hasil Prediksi Harga']])
# hasil = pd.concat([hasil1,hasil]).reset_index(drop=True)

@app.route('/laporan')
def laporan():
    query = "SELECT * FROM prediksi ORDER BY id_data_predict DESC"
    mycursor = mydb.cursor()
    mycursor.execute(query)
    datas = mycursor.fetchall()
    return render_template('laporan.html',values = datas)

if __name__ == '__main__':
    app.run(debug=True)
                   