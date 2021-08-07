from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

#Obteniendo los valores del archivo CSV y borrando las columnas que no se usarán
studentsData = pd.read_csv("./students_data_full_class.csv")
studentsData = studentsData.drop(columns=['ssc_p', 'ssc_b', 'hsc_b', 'hsc_p', 'hsc_s', 'etest_p', 'mba_p'])

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/full-data")
def full_data():    
    return render_template('full_data.html', tables=[studentsData.to_html(classes='data', header=True)])

@app.route("/pie-chart")
def pie_chart():
    return render_template('graphs/pie_chart.html')
