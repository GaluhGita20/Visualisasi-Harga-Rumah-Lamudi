from flask import Flask, jsonify, render_template, request
import pandas as pd
import numpy as np
import json
import pickle
from src.linear_regression import mainprog

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
    my_dict = {key: value for key, value in zip(grouped_dict['luas_bangunan'], grouped_dict['harga'])}
    datas = datas[datas['harga'] == 1000000000000000000000000000]
    return render_template('form.html',values=datas)


#Predict Data
@app.route('/predict', methods=['POST'])
def predict():
    values = request.values

    # X_new = {'kamar_tidur': [int(values['kamar_tidur'])], 'kamar_mandi': [int(values['kamar_mandi'])], 'jmlh_lantai': [int(values['jmlh_lantai'])], 'luas_bangunan': [int(values['luas_bangunan'])], 'luas_tanah': [int(values['luas_tanah'])]}
   
    predict, val = mainprog(values['kabupaten'], int(values['kamar_tidur']), int(values['kamar_mandi']), int(values['jmlh_lantai']), int(values['luas_bangunan']), int(values['luas_tanah'])) 
    # locale.setlocale(locale.LC_ALL, 'id_ID')
  
    # hasil1 = pd.DataFrame([[values['kabupaten'],values['luas_tanah'],values['luas_bangunan'],values['kamar_tidur'],values['kamar_mandi'],values['jmlh_lantai'],predict]], columns =[['Kabupaten','Luas Tanah','Luas Bangunan','Kamar Tidur','Kamar Mandi','Jumlah Lantai','Hasil Prediksi Harga']])
    # hasil = pd.concat([hasil,hasil1]).reset_index(drop=True)
    if values !=None:
        query = "INSERT INTO prediksi (kabupaten , kamar_tidur , kamar_mandi , jumlah_lantai ,luas_bangunan , luas_tanah ,harga) VALUES(%s,%s,%s,%s,%s,%s,%s)"
        values = (values['kabupaten'], int(values['kamar_tidur']), int(values['kamar_mandi']), int(values['jmlh_lantai']), int(values['luas_bangunan']), int(values['luas_tanah']), int(predict))
        mycursor = mydb.cursor()
        mycursor.execute(query,values)
        mydb.commit()

    # formatted_price = locale.currency(predict, grouping=True)
    return render_template('form.html', prediction_text='Hasil Prediksi Harga Rumah : Rp. {} '.format(int(predict)), values=val)

@app.route('/heatmap')
def heatmap():
    return render_template('heatmap.html')

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
    query = "SELECT * FROM prediksi ORDER BY harga ASC"
    mycursor = mydb.cursor()
    mycursor.execute(query)
    datas = mycursor.fetchall()
    return render_template('laporan.html',values = datas)

if __name__ == '__main__':
    app.run(debug=True)
                   