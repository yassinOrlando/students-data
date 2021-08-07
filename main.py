from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    studentsData = pd.read_csv("./students_data_full_class.csv")
    return render_template('home.html')