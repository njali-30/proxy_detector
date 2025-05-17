from flask import Flask, render_template, request
import mysql.connector
import numpy as np
import pandas as pd
from config import db_config

app = Flask(__name__)

def get_students():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    cursor.execute("SELECT roll_no, name FROM students ORDER BY roll_no")
    students = cursor.fetchall()
    conn.close()
    return students

@app.route('/', methods=['GET', 'POST'])
def index():
    students = get_students()
    if request.method == 'POST':
        checkin_times = []
        for roll_no, _ in students:
            time_input = request.form.get(f"time_{roll_no}")
            if time_input:
                try:
                    time = float(time_input)
                except:
                    time = None
            else:
                time = None
            checkin_times.append(time)

        df = pd.DataFrame(students, columns=['roll_no', 'name'])
        df['checkin_time'] = checkin_times
        df['status'] = df['checkin_time'].apply(lambda x: 'Absent' if x is None else 'Present')

        valid_times = df[df['checkin_time'].notnull()]['checkin_time']
        mean = valid_times.mean()
        std = valid_times.std()
        if std == 0 or pd.isna(std):
            z_scores = pd.Series([0]*len(valid_times), index=valid_times.index)
        else:
            z_scores = (valid_times - mean) / std
        z_outliers = valid_times[z_scores.abs() > 2].index

        q1 = valid_times.quantile(0.25)
        q3 = valid_times.quantile(0.75)
        iqr = q3 - q1
        iqr_outliers = valid_times[(valid_times < (q1 - 1.5 * iqr)) | (valid_times > (q3 + 1.5 * iqr))].index

        proxy_indices = z_outliers.union(iqr_outliers)
        df.loc[proxy_indices, 'status'] = 'Proxy'

        return render_template('results.html', data=df.to_dict(orient='records'))

    return render_template('index.html', students=students)

if __name__ == '__main__':
    app.run(debug=True)
