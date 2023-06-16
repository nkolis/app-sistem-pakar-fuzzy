import base64
from io import BytesIO
from skfuzzy import control as ctrl
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from flask import Flask, request, render_template
from flask_cors import CORS, cross_origin
import numpy as np
import matplotlib
matplotlib.use('Agg')


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


def aturan():
    budget = ctrl.Antecedent(np.arange(0, 15, 1), 'budget')
    jarak = ctrl.Antecedent(np.arange(0, 3100, 1), 'jarak')
    durasi = ctrl.Antecedent(np.arange(0, 7, 1), 'durasi')

    budget['kecil'] = fuzz.trapmf(budget.universe, [0, 0, 2, 5])
    budget['sedang'] = fuzz.trimf(budget.universe, [4, 7, 10])
    budget['besar'] = fuzz.trapmf(budget.universe, [9, 12, 15, 15])

    # budget.view()

    jarak['dekat'] = fuzz.trapmf(jarak.universe, [0, 0, 1100, 2200])
    jarak['jauh'] = fuzz.trapmf(jarak.universe, [2000, 2550, 3100, 3100])

    # jarak.view()

    durasi['sebentar'] = fuzz.trapmf(durasi.universe, [0, 0, 2, 4])
    durasi['lama'] = fuzz.trapmf(durasi.universe, [3, 5, 7, 7])

    # durasi.view()

    kondisi = ctrl.Consequent(np.arange(0, 126, 1), 'kondisi')
    kondisi['tidak memungkinkan'] = fuzz.trimf(kondisi.universe, [0, 0, 50])
    kondisi['kurang memungkinkan'] = fuzz.trimf(
        kondisi.universe, [25, 50, 125])
    kondisi['memungkinkan'] = fuzz.trimf(kondisi.universe, [50, 125, 125])

    # kondisi.view()

    rule1 = ctrl.Rule(budget['kecil'] & jarak['dekat'] &
                      durasi['sebentar'], kondisi['memungkinkan'])
    rule2 = ctrl.Rule(budget['kecil'] & jarak['dekat'] &
                      durasi['lama'], kondisi['kurang memungkinkan'])
    rule3 = ctrl.Rule(budget['kecil'] & jarak['jauh'] &
                      durasi['sebentar'], kondisi['tidak memungkinkan'])
    rule4 = ctrl.Rule(budget['kecil'] & jarak['jauh'] &
                      durasi['lama'], kondisi['tidak memungkinkan'])
    rule5 = ctrl.Rule(budget['sedang'] & jarak['dekat'] &
                      durasi['sebentar'], kondisi['memungkinkan'])
    rule6 = ctrl.Rule(budget['sedang'] & jarak['dekat'] &
                      durasi['lama'], kondisi['memungkinkan'])
    rule7 = ctrl.Rule(budget['sedang'] & jarak['jauh'] &
                      durasi['sebentar'], kondisi['kurang memungkinkan'])
    rule8 = ctrl.Rule(budget['sedang'] & jarak['jauh'] &
                      durasi['lama'], kondisi['tidak memungkinkan'])
    rule9 = ctrl.Rule(budget['besar'] & jarak['dekat'] &
                      durasi['sebentar'], kondisi['memungkinkan'])
    rule10 = ctrl.Rule(budget['besar'] & jarak['dekat'] &
                       durasi['lama'], kondisi['memungkinkan'])
    rule11 = ctrl.Rule(budget['besar'] & jarak['jauh'] &
                       durasi['sebentar'], kondisi['memungkinkan'])
    rule12 = ctrl.Rule(budget['besar'] & jarak['jauh'] &
                       durasi['lama'], kondisi['memungkinkan'])
    kondisi_ctrl = ctrl.ControlSystem(
        [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9, rule10, rule11, rule12])

    braking = ctrl.ControlSystemSimulation(kondisi_ctrl)

    return {'budget': budget, 'jarak': jarak, 'durasi': durasi, 'kondisi': kondisi, 'braking': braking}


# API


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
@cross_origin()
def analyze():

    budget_value = float(request.form.get('budget'))
    jarak_value = float(request.form.get('jarak'))
    durasi_value = float(request.form.get('durasi'))

    rule = aturan()
    braking = rule['braking']
    kondisi = rule['kondisi']

    braking.input['budget'] = budget_value
    braking.input['jarak'] = jarak_value
    braking.input['durasi'] = durasi_value
    braking.compute()

    try:

        img = BytesIO()
        kondisi.view(sim=braking)

        plt.savefig(img, format='png')
        img.seek(0)
        img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
        img.close()

        persentase_output = braking.output['kondisi']

        def hasil(persentase):
            if persentase >= 75:
                return 'Memungkinkan'
            elif persentase >= 30:
                return 'Kurang Memungkinkan'
            else:
                return 'Tidak Memungkinkan'

        return [{'persentase': f"{persentase_output:.2f}", 'hasil': hasil(persentase_output), 'path_graph': img_base64}]
    except AttributeError as e:
        return [{'error': str(e)}]


# plt.show()
if __name__ == '__main__':

    app.run(debug=True, host='0.0.0.0', port=8000)
