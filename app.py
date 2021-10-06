from flask import Flask, render_template, request, url_for, redirect
from flask_cors import CORS,cross_origin
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
import jsonify
import requests
import pickle
standard_to = StandardScaler()

app = Flask(__name__)

#_________________loading_Models________________________________________#
model        = pickle.load(open('pressuredrop_random_forest_regression_model.pkl', 'rb'))
model_regime = pickle.load(open('random_forest_classification_model.pkl', 'rb'))
model_bend   = pickle.load(open('bend_pressuredrop_random_forest_regression_model.pkl', 'rb'))
########################################################################
def output_result(output):

        if output == 0:
            result = "Annular"
        elif output == 1:
            result = "Dryout"
        elif output == 2:
            result = "Intermittent"
        elif output == 3:
            result = "Misty"
        elif output == 4:
            result ="Stratified-Wavy"
        elif output == 5:
            return "Slug"
        elif output == 6:
            result = "Slug-Stratified-Wavy"
        else:
            result =int(1)
        print("From function", result)
        return result


########################################################################
#------------Flask_App-------------------------------------------------

@app.route('/')
#@cross_origin()
def Home():
    title = 'RefPTH - Home'
    return render_template('index.html', title=title)

@app.route('/flowregime')
#@cross_origin()
def flowregime():
    title = 'RefPTH - Flow-Regime'
    return render_template('flowregime.html', title=title)

@app.route('/bendpressure')
#@cross_origin()
def bendpressure():
    title = 'RefPTH - Bend-Pressure-Drop'
    return render_template('bendpressure.html', title=title)



@app.route("/predict", methods=['POST'])
#@cross_origin()
def predict():
    try:
        if request.method == 'POST':
            Refrigerant=request.form['Refrigerant']
            if(Refrigerant=='R1234yf'):
                    Refrigerant=0
            elif(Refrigerant=='R1234ze(E)'):
                    Refrigerant=1
            elif(Refrigerant=='R134a'):
                    Refrigerant=2
            elif(Refrigerant=='R22'):
                    Refrigerant=3
            elif(Refrigerant=='R410a'):
                    Refrigerant=4
            else:
                    Refrigerant=5


            Pipe_Diameter     = float(request.form['Pipe_Diameter'])
            Inlet_Temperature = float(request.form['Inlet_Temperature'])
            Inlet_Pressure = float(request.form['Inlet_Pressure'])
            Vapour_Quality    = float(request.form['Vapour_Quality'])
            Mass_Flux         = float(request.form['Mass_Flux'])


            ########################################### Prediction ###############################################################
            prediction = model.predict([[Refrigerant,Pipe_Diameter,Inlet_Temperature,Inlet_Pressure, Vapour_Quality, Mass_Flux ]])
            output=round(prediction[0],2)
            ######################################################################################################################
            if output<0.0:
                return render_template('result.html',prediction_text="Error, Please enter proper bounndary conditions")
            else:
                return render_template('result.html',prediction_text="Pipe Pressure drop is : {} Pa/m".format(output))
        else:
            return render_template('index.html')
    except:
        return render_template('result.html', prediction_text="Error")



################################################################################################################################




@app.route("/predict_1", methods=['POST'])
#@cross_origin()
def predict_1():

        if request.method == 'POST':
            Refrigerant=request.form['Refrigerant']
            if(Refrigerant=='R134a'):
                    Refrigerant=0
            elif(Refrigerant=='R22'):
                    Refrigerant=1
            else:
                    Refrigerant=2

            Pipe_Diameter     = float(request.form['Pipe_Diameter'])
            Inlet_Temperature = float(request.form['Inlet_Temperature'])
            Vapour_Quality    = float(request.form['Vapour_Quality'])
            Mass_Flux         = float(request.form['Mass_Flux'])

            ########################################### Prediction ###############################################################
            print([[Refrigerant,Pipe_Diameter, Mass_Flux, Inlet_Temperature, Vapour_Quality]])
            prediction = model_regime.predict([[Refrigerant,Pipe_Diameter, Mass_Flux, Inlet_Temperature, Vapour_Quality]])

            print("Prediction:", prediction)
            output=prediction[0]
            print("output:",output)
            singleitem = next(iter(prediction))
            ######################################################################################################################
            Results = output_result(singleitem)
            print(Results)

        else:
            return render_template('index.html', prediction_text="Error")

        return render_template('result.html', prediction_text="The Flow Regime is: {}".format(Results))





################################################################################################################################
####################################################  Bend  ############################################################################


@app.route("/predict_2", methods=['POST'])
#@cross_origin()
def predict_2():
    try:
        if request.method == 'POST':
            Refrigerant=request.form['Refrigerant']
            if(Refrigerant=='R1234yf'):
                    Refrigerant=0
            elif(Refrigerant=='R134a'):
                    Refrigerant=1
            else:
                    Refrigerant=2

            Pipe_Diameter     = float(request.form['Pipe_Diameter'])
            Radius_Curvature  = float(request.form['Radius_Curvature'])
            Inlet_Temperature = float(request.form['Inlet_Temperature'])
            Inlet_Pressure    = float(request.form['Inlet_Pressure'])
            Vapour_Quality    = float(request.form['Vapour_Quality'])
            Mass_Flux         = float(request.form['Mass_Flux'])

            ########################################### Prediction ###############################################################
            prediction = model_bend.predict([[Refrigerant,Pipe_Diameter, Radius_Curvature, Mass_Flux, Inlet_Temperature, Inlet_Pressure,Vapour_Quality]])
            output=round(prediction[0],2)
            ######################################################################################################################
            if output<=0.0:
                return render_template('result.html',prediction_text="Error, Please enter proper bounndary conditions")
            else:
                return render_template('result.html',prediction_text=" Bend Pipe Pressure drop is : {} Pa/m".format(output))
        else:
            return render_template('index.html')
    except:
        return render_template('index.html', prediction_text="Error")



################################################################################################################################
if __name__=="__main__":
    app.run(debug=False)

