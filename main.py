from flask import Flask, render_template
import pandas as pd
import base64
from io import BytesIO
from matplotlib.figure import Figure
from matplotlib import pyplot as plt

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
    title = "Gráfica de pastel"
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    ax.plot([3, 2])
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return render_template('graphs/chart.html', title=title, img_data=data)

@app.route("/hist-chart")
def hist_chart():
    title = "Histograma"

    fig = Figure()
    ax = fig.subplots()
    ax.hist(studentsData["salary"], bins=20) 

    #plt.plot(bins, studentsData["salary"], '--', color ='black')
    ax.title.set_text('Histograma de salarios')
    ax.set_xlabel('Salarios anuales')
    ax.set_ylabel('Cantidad')
    ax.grid()
    
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return render_template('graphs/chart.html', title=title, img_data=data)

@app.route("/freq-chart")
def freq_chart():
    title = "Polígono de frecuencias"

    fig = Figure()
    ax = fig.subplots()
    n, x, _ = plt.hist(studentsData["salary"], bins=20, density=True) 
    ax.plot( x[1:], n, marker='.') 

    ax.title.set_text('Frecuencia de salarios')
    ax.set_xlabel('Salarios anuales')
    ax.set_ylabel('Frecuencia (0 = baja, 1 = alta)')
    ax.grid()
    
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return render_template('graphs/chart.html', title=title, img_data=data)

@app.route("/moda-media-mediana")
def med_tend_central():
    dataMode = studentsData.mode(dropna=True)
    dataMode = dataMode.head(1)
    dataMedian = studentsData.median()
    dataMean = studentsData.mean()
    return render_template('graphs/med_tend_central.html', moda=dataMode, media=dataMean, mediana=dataMedian)
