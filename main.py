from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/api/v1/<station>/<date>')
def weather_api(station, date):
    filepath = 'data_small_weather/TG_STAID' + str(station).zfill(6) + '.txt'
    df = pd.read_csv(filepath, skiprows=20, parse_dates=['    DATE'])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10
    content = {
        'station': station,
        'date': date,
        'temperature': temperature
    }
    return content


if __name__ == '__main__':
    app.run(debug=True)
