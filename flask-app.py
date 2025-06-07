from flask import Flask, render_template, request, jsonify
from freq import gogo
import json
import math
app = Flask(__name__)

@app.route("/show")
def hello(r,c,pwm_freq,freq_data):
    cf=1/(2*math.pi*r*c)
    return f"<ht1ml><body>{r}  {c}  {pwm_freq}    {freq_data}<br />{cf}<br /><img src=\"/static/sine_wave.png\" /></body></html>"



@app.route('/', methods=['GET'])
def index():
    return render_template('form.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        r = float(request.form['R'])
        c = float(request.form['C'])
        pwm_freq = float(request.form['PWM_FREQ'])
        freq_data = json.loads(request.form['frequency_table'])
        gogo(pwm_freq,r,c,freq_data)
        # Return received data for now (you can add calculations later)
        return hello(r,c,pwm_freq,freq_data)

    except (ValueError, json.JSONDecodeError) as e:
        return jsonify({'error': str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
