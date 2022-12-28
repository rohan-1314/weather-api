from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

stations = pd.read_csv('data_small_weather/stations.txt', skiprows=17)
station = stations[['STAID', 'STANAME                                 ']]


@app.route('/')
def home():
    return render_template('home.html', data=station.to_html())


@app.route('/api/v1/<station>/<date>')
def one_date_temp_data(station, date):
    filepath = 'data_small_weather/TG_STAID' + str(station).zfill(6) + '.txt'
    df = pd.read_csv(filepath, skiprows=20, parse_dates=['    DATE'])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10
    content = {
        'station': station,
        'date': date,
        'temperature': temperature
    }
    return content


@app.route('/api/v1/<station>')
def all_data(station):
    filepath = 'data_small_weather/TG_STAID' + str(station).zfill(6) + '.txt'
    df = pd.read_csv(filepath, skiprows=20, parse_dates=['    DATE'])
    result = df.to_dict(orient='records')
    return result


@app.route('/api/v1/yearly/<station>/<year>')
def data_one_year(station, year):
    filepath = 'data_small_weather/TG_STAID' + str(station).zfill(6) + '.txt'
    df = pd.read_csv(filepath, skiprows=20)
    df['    DATE'] = df['    DATE'].astype(str)
    result = df[df['    DATE'].str.startswith(str(year))].to_dict(orient='record')
    return result


if __name__ == '__main__':
    app.run(debug=True)
