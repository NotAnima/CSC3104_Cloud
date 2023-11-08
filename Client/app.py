from flask import Flask, redirect, url_for, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange
import diabetes, schedule, time, threading, grpc, FD_pb2, FD_pb2_grpc
import pandas as pd
from os import environ
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pickle

app = Flask(__name__)
app.config['SECRET_KEY'] = "Banana73"
app.config['SQLALCHEMY_DATABASE_URI'] = environ['DATABASE_URL']
domain = environ['DOMAIN'] + ":50051"

db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    high_bp = db.Column(db.Float, nullable=False)  # Assuming 0 for No, 1 for Yes
    high_chol = db.Column(db.Float, nullable=False)  # Assuming 0 for No, 1 for Yes
    chol_check = db.Column(db.Float, nullable=False)  # Assuming 0 for No, 1 for Yes
    bmi = db.Column(db.Float, nullable=False)
    smoker = db.Column(db.Float, nullable=False)  # Assuming 0 for No, 1 for Yes
    stroke = db.Column(db.Float, nullable=False)  # Assuming 0 for No, 1 for Yes
    heart_disease_or_attack = db.Column(db.Float, nullable=False)  # Assuming 0 for No, 1 for Yes
    phys_activity = db.Column(db.Float, nullable=False)  # Assuming 0 for No, 1 for Yes
    fruits = db.Column(db.Float, nullable=False)  # Assuming 0 for No, 1 for Yes
    veggies = db.Column(db.Float, nullable=False)  # Assuming 0 for No, 1 for Yes
    hvy_alcohol_consump = db.Column(db.Float, nullable=False)  # Assuming 0 for No, 1 for Yes
    phys_hlth = db.Column(db.Float, nullable=False)  # This could be days of poor physical health
    diff_walk = db.Column(db.Float, nullable=False)  # Assuming 0 for No, 1 for Yes
    sex = db.Column(db.Float, nullable=False)  # Assuming 0 for Female, 1 for Male
    age = db.Column(db.Float, nullable=False)  # Assuming an integer representation for age groups

    # These fields are only ever updated by function calls and commits by the doctor and trainModel
    label = db.Column(db.Float, nullable=True)
    labelled = db.Column(db.Boolean, nullable=False, default=False)
    sent = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, high_bp, high_chol, chol_check, bmi, smoker, stroke, heart_disease_or_attack, phys_activity, fruits, veggies, hvy_alcohol_consump, phys_hlth, diff_walk, sex, age):
        self.high_bp = high_bp
        self.high_chol = high_chol
        self.chol_check = chol_check
        self.bmi = bmi
        self.smoker = smoker
        self.stroke = stroke
        self.heart_disease_or_attack = heart_disease_or_attack
        self.phys_activity = phys_activity
        self.fruits = fruits
        self.veggies = veggies
        self.hvy_alcohol_consump = hvy_alcohol_consump
        self.phys_hlth = phys_hlth
        self.diff_walk = diff_walk
        self.sex = sex
        self.age = age

class localmodel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.Text, nullable=False)
    picklefile = db.Column(db.LargeBinary, nullable=False)

    def __init__(self, picklefile):
        self.timestamp = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.picklefile = picklefile

class referencemodel(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    timestamp = db.Column(db.Text, nullable=False)
    picklefile = db.Column(db.LargeBinary, nullable=False)

    def __init__(self, picklefile):
        self.timestamp = str(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        self.picklefile = picklefile
        
readyToTrain = False
newModel = False
channel = grpc.insecure_channel(domain)
stub = FD_pb2_grpc.ModelServiceStub(channel)

# Check with server side if model matches up
def scheduled_task():
    global model, weights, bias

    try:
        # Load training model
        trainModel = diabetes.load_model("trainingModel.pkl")
    except:
        # If no training model ready yet, use reference model
        trainModel = diabetes.load_model("referenceModel.pkl")

    # Extract weights, bias, shape
    weights, bias, shape = diabetes.extract_weights_and_biases(trainModel)
    sent_weights = FD_pb2.sentWeights(weights=weights,bias=bias,shape=shape)
    response = stub.sendWeight(sent_weights)

    # Reconstruct the latest received model
    model = diabetes.train_base_model(response.weights, response.bias, response.shape)

    # Update the local model
    diabetes.save_model(model, "referenceModel.pkl")
    # Your background task logic goes here
    print("Scheduled task executed!")

# Schedule the task to run every 30 minutes
schedule.every(30).minutes.at(":00").do(scheduled_task)
schedule.every(30).minutes.at(":30").do(scheduled_task)

# Function used during init to get the latest model from the server
def getModel():
   # Check DB
    try:
        referenceQuery = referencemodel.query.filter_by().all()
        if len(referenceQuery) < 1:
            raise Exception
        referenceQuery = referenceQuery[-1] # get the latest entry
        referencePickle = referenceQuery.picklefile
        model = pickle.loads(referencePickle)
        return model
    except:
        try: 
                # Get by gRPC
                result = FD_pb2.startValue(number=1)
                response = stub.getModel(result)
                # Reconstruct the weights into a model
                model = diabetes.train_base_model(response.weights, response.bias, response.shape)
                # Save the model locally
                diabetes.save_model(model, "firstModel.pkl")

                with open("firstModel.pkl", "rb") as f:
                    pickleBin = f.read()
                    pickleObject = referencemodel(pickleBin)
                    db.session.add(pickleObject)
                    db.session.commit()
                return model
        except:
            # Get local model
            model = diabetes.load_model("baseModel.pkl")
            return model
   
model = getModel()

# Utility functions
def convertStrsToFloats(dictionary):
    for key, value in dictionary.items():
        dictionary[key] = float(value)


class userForm(FlaskForm):
    q1 = RadioField('Q1: Do you have high blood pressure?', validators=[DataRequired()], choices=[('0', 'Low Blood Pressure'), ('1', 'High Blood Pressure')])
    q2 = RadioField('Q2: Do you have high cholesterol?', validators=[DataRequired()], choices=[('0', 'No High Cholesterol'), ('1', 'High Cholesterol')])
    q3 = RadioField('Q3: Have you have high cholesterol in the last 5 years?', validators=[DataRequired()], choices=[('0', 'Not in the last 5 years'), ('1', 'Yes, it was within the last 5 years')])
    q4 = FloatField('Q4: What is your BMI? E.g: 23.42', validators=[DataRequired(), NumberRange(min=0.0, max=251.1)]) # 251.1 is the highest recorded BMI in the world
    q5 = RadioField('Q5: Have you smoked more than 100 cigarettes in your lifetime?', validators=[DataRequired()], choices=[('0', 'No'), ('1', 'Yes')])
    q6 = RadioField('Q6: Have you ever had a stroke before?', validators=[DataRequired()], choices=[('0', 'No'), ('1', 'Yes')])
    q7 = RadioField('Q7: Have you ever had Coronary Heart Disease or Myocordial Infarction (MI) before?', validators=[DataRequired()], choices=[('0', 'No'), ('1', 'Yes')])
    q8 = RadioField('Q8: Did you have any physical activity in the past 30 days? - Not including job', validators=[DataRequired()], choices=[('0', 'No'), ('1', 'Yes')])
    q9 = RadioField('Q9: Do you consume fruit 1 or more times a day?', validators=[DataRequired()], choices=[('0', 'No'), ('1', 'Yes')])
    q10 = RadioField('Q10: Do you introduce Vegetables 1 or more times a day in your diet?', validators=[DataRequired()], choices=[('0', 'No'), ('1', 'Yes')])
    q11 = RadioField('Q11: Do you consume Alcohol heavily (Adults)? For Men: More than 14 Drinks per week. For Women: More than 7 Drinks per week', validators=[DataRequired()], choices=[('0', 'No'), ('1', 'Yes')])
    q12 = FloatField('Q12: For the last 30 days, how many days have you not been feeling well?', validators=[DataRequired(), NumberRange(min=0.0, max=30.0)])
    q13 = RadioField('Q13: Do you have difficulties walking or climbing up the stairs?', validators=[DataRequired()], choices=[('0', 'No'), ('1', 'Yes')])
    q14 = RadioField('Q14: What is your sex?', validators=[DataRequired()], choices=[('0', 'Female'), ('1', 'Male')])
    q15 = RadioField('Q15: What is your age group?', validators=[DataRequired()], choices=[('1', '18-24'), ('2', '25-29'), ('3', '30-34'), ('4', '35-39'), ('5', '40-44'), ('6', '45-49'), ('7', '50-54'), ('8', '55-59'), ('9', '60-64'), ('10', '65-69'), ('11', '70-74'), ('12', '75-79'), ('13', '80+'), ])
    
    submit = SubmitField('Secretly Tell Us!')


# remember to implement AES for data encryption when sending gRPC over the network

@app.route("/")
def homePage():
    modelToTrain = localmodel.query.filter_by().all()
    modelToRefer = referencemodel.query.filter_by().all()
    print(len(modelToTrain))
    print(len(modelToRefer))
    #foundPatients = Patient.query.filter_by().all()
    #return render_template("index.html")
    #return render_template("test.html", personList=foundPatients)
    return render_template("modeltest.html", modelList=modelToRefer)
@app.route("/results")
def resultPage():

    prediction_result = request.args.get("prediction_result")
    return render_template("results.html",  prediction_result=prediction_result)

@app.route("/testing")
def oneTimeInsert():
    with open("baseModel.pkl", "rb") as pickleFile:
        pickleRead = pickleFile.read()
        pickleObject = referencemodel(pickleRead)
        db.session.add(pickleObject)
        db.session.commit()
    return render_template("index.html")

@app.route("/trainModel", methods=['GET', 'POST'])
def trainModel():

    # Check if at least 2 types of diabetes has been diagnosed (No diabetes, Have diabetes, Pre-diabetes)
    global readyToTrain, newModel, model
    foundPatients = Patient.query.filter_by(labelled=True, sent=False).all() # returns Patient objects
    # Diagnosis results
    result = set()
    if (not readyToTrain):
         for patient in foundPatients:
            if len(result) <= 1:
                print("System not ready yet for training")
                if patient.label != None: # should not be the case since if labelled=True, should have a label value associated with it
                    result.add(patient.label) # add the patient.label field
            else:
                print("System ready to be trained")
                readyToTrain = True
                break

    if (readyToTrain and request.method == 'POST'):
        print("Training has started")
        # Convert all the foundPatients diagnosed by the doctor into a pandas dataframe
        trainingData = pd.DataFrame(foundPatients)

        # # Send data for training
        model = diabetes.train_existing_model(model, trainingData)
        diabetes.save_model(model, "trainingModel.pkl")

        # updating the db to be such that these patient details have already been used for training and won't be used again in the future
        for patient in foundPatients:
            patient.sent = True
        db.session.commit()

        # Clean up

        readyToTrain = False
        newModel = True
        # answeredList = []
        return redirect(url_for("homePage"))

    # Check if the model name hash matches with the local database hash model through an API
    # if not, then claim the new model through the API again
    # train the model iteratively locally and store the model's training weights and bias' in the database
    return render_template("training.html", readyToTrain=readyToTrain)

@app.route('/doctors', methods=['GET', 'POST'])
def doctors():

    global model
    foundPatients = Patient.query.filter_by(labelled=False).all()

    if request.method == 'POST':
        # Create an empty list to store the selected indexes
        dataList = request.form

        # slice the array of dictionaries dataList to not include the last POST request key which is for 'submit'
        for indexKey, value in list(dataList.items())[:-1]: 
            if dataList[indexKey] != None:                
                # update those based off the form request value and mark this patient as labelled in the db
                foundPatients[(int(indexKey)-1)].label = value
                foundPatients[(int(indexKey)-1)].labelled = True
        # update the db for the atomic changes
        db.session.commit()

    # get the newly updated leftovers if any and display them onto the webpage
    foundPatients = Patient.query.filter_by(labelled=False).all()
    return render_template('doctors.html', personList=foundPatients)

@app.route("/questions", methods=["POST", "GET"])
def prediction():

    form = userForm()
    if form.validate_on_submit():
        patientDetails = {}
        patientDetails['high_bp'] = request.form['q1']
        patientDetails['high_chol'] = request.form['q2']
        patientDetails['chol_check'] = request.form['q3']
        patientDetails['bmi'] = request.form['q4']
        patientDetails['smoker'] = request.form['q5']
        patientDetails['stroke'] = request.form['q6']
        patientDetails['heart_disease_or_attack'] = request.form['q7']
        patientDetails['phys_activity'] = request.form['q8']
        patientDetails['fruits'] = request.form['q9']
        patientDetails['veggies'] = request.form['q10']
        patientDetails['hvy_alcohol_consump'] = request.form['q11']
        patientDetails['phys_hlth'] = round(float(request.form['q12'])) # Get the nearest integer by rounding
        patientDetails['diff_walk'] = request.form['q13']
        patientDetails['sex'] = request.form['q14']
        patientDetails['age'] = request.form['q15']

        # All the values in the keys being inserted into the dictionary are currently Strings, calling this function to convert them into float values, if not needed, then remove
        convertStrsToFloats(patientDetails)
        
        # create a new patient object to be stored into the db from the queried values
        newPatient = Patient(patientDetails['high_bp'], patientDetails['high_chol'], patientDetails['chol_check'], patientDetails['bmi'], patientDetails['smoker'], patientDetails['stroke'], patientDetails['heart_disease_or_attack'], patientDetails['phys_activity'], patientDetails['fruits'], patientDetails['veggies'], patientDetails['hvy_alcohol_consump'], patientDetails['phys_hlth'], patientDetails['diff_walk'], patientDetails['sex'], patientDetails['age'])
        
        # Add this new patient into the database
        db.session.add(newPatient)
        db.session.commit()

        # Transform data to be suitable for the model to predict
        predict = []
        for value in patientDetails.values():
            predict.append(value)

        referenceQuery = referencemodel.query.filter_by().all()
        referenceQuery = referenceQuery[-1] # get the latest entry
        referencePickle = referenceQuery.picklefile
        model = pickle.loads(referencePickle)

        scaled_features = diabetes.reshape_data(predict)
        prediction_result = diabetes.make_prediction(model,scaled_features)

        return redirect(url_for("resultPage", prediction_result=prediction_result))

    # else condition for get request
    return render_template('questions.html', form=form)

# Create a threaded schedule task
def run_scheduled_task():
    while True:
        schedule.run_pending()  # Check and run scheduled tasks
        time.sleep(1) 

# run the app here
if __name__ == "__main__":
    # Create a thread for the background task
    task_thread = threading.Thread(target=run_scheduled_task)
    task_thread.daemon = True  # Set as daemon to allow clean exit

    # Start the background task thread
    task_thread.start()

    # Run Flask on the main thread
    app.run(debug=True)
