from flask import Flask, redirect, url_for, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, RadioField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange

app = Flask(__name__)
app.config['SECRET_KEY'] = "Banana73"

personList = [] # stores every form entry [personDetails class]locally so long as the server doesn't shutdown, can be stored long term by writing into a csv
#piledCacheCategories = [] # for the usage of sending the categories of each patient before nuking them from personList
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
    q11 = RadioField('Q11: Did you consume fruit 1 or more times a day?', validators=[DataRequired()], choices=[('0', 'No'), ('1', 'Yes')])
    q12 = RadioField('Q12: Do you consume Alcohol heavily (Adults)? For Men: More than 14 Drinks per week. For Women: More than 7 Drinks per week', validators=[DataRequired()], choices=[('0', 'No'), ('1', 'Yes')])
    q13 = RadioField('Q13: Do you have difficulties walking or climbing up the stairs?', validators=[DataRequired()], choices=[('0', 'No'), ('1', 'Yes')])
    q14 = RadioField('Q14: What is your sex?', validators=[DataRequired()], choices=[('0', 'Female'), ('1', 'Male')])
    q15 = RadioField('Q15: What is your age group?', validators=[DataRequired()], choices=[('1', '18-24'), ('2', '25-29'), ('3', '30-34'), ('4', '35-39'), ('5', '40-44'), ('6', '45-49'), ('7', '50-54'), ('8', '55-59'), ('9', '60-64'), ('10', '65-69'), ('11', '70-74'), ('12', '75-79'), ('13', '80+'), ])
    
    submit = SubmitField('Secretly Tell Us!')

# remember to implement AES for data encryption when sending gRPC over the network


# Usage; personList = popBasedOnIndexes(personList, doctorsRepliesOfPatients)
def popBasedOnIndexes(personList, indexesToPop):
    newList = [personList[i] for i in range(len(personList)) if i not in indexesToPop]
    return newList


class personDetails():
    def __init__(self, dictionary):
        self.information = dictionary
    
    def getDetails(self):
        return self.information

@app.route("/")
def homePage():
    return render_template("index.html")

@app.route("/trainModel")
def trainModel():
    # Check if the model name hash matches with the local database hash model through an API
    # if not, then claim the new model through the API again
    # train the model iteratively locally and store the model's training weights and bias' in the database
    return redirect(url_for("homePage"))
@app.route("/sendModel")
def sendModel():
    # Check if the model name hash matches with the local database hash model through an API
    # If no, then prompt user to claim a new model and train it first
    # If yes, then query from the local/cloud database and then send the model over to the server through the API
    return redirect(url_for("homePage"))

@app.route('/doctors', methods=['GET', 'POST'])
def doctors():
    global personList
    # global piledCacheCategories
    if request.method == 'POST':
        # Create an empty list to store the selected indexes
        selected_indexes = []

        dataList = request.form

        # slice the dictionary to not include the last POST request key which is for 'submit'
        for indexKey, value in list(dataList.items())[:-1]: 
            if dataList[indexKey] != None:
                # converts the string that is passed back and then is typecasted into an integer and -1 for the 0th indexing start
                selected_indexes.append((int(indexKey)-1)) 

        # to retrieve the 0,1,2 from each radio button, just add get the value from each key that iterates through
        # remove those indexes that the doctor actually categorises
        personList = popBasedOnIndexes(personList, selected_indexes)

        # SEND THE CATEGORIZING INFORMATION HERE

    return render_template('doctors.html', personList=personList)

@app.route("/questions", methods=["POST", "GET"])
def prediction():
    form = userForm()
    if form.validate_on_submit():
        patientDetails = {}
        patientDetails['HighBP'] = request.form['q1']
        patientDetails['HighChol'] = request.form['q2']
        patientDetails['CholCheck'] = request.form['q3']
        patientDetails['BMI'] = request.form['q4']
        patientDetails['Smoker'] = request.form['q5']
        patientDetails['Stroke'] = request.form['q6']
        patientDetails['HeartDiseaseorAttack'] = request.form['q7']
        patientDetails['PhysActivity'] = request.form['q8']
        patientDetails['Fruits'] = request.form['q9']
        patientDetails['Veggies'] = request.form['q10']
        patientDetails['HvyAlcoholConsump'] = request.form['q11']
        patientDetails['PhysHlth'] = request.form['q12']
        patientDetails['DiffWalk'] = request.form['q13']
        patientDetails['Sex'] = request.form['q14']
        patientDetails['Age'] = request.form['q15']

        # All the values in the keys being inserted into the dictionary are currently Strings, calling this function to convert them into float values, if not needed, then remove
        convertStrsToFloats(patientDetails)

        # Instantiate the new person
        newPerson = personDetails(patientDetails)

        # Add him/her into the local list of personLists for the doctors to use, for every person that their data is cleared up, they are cleared off the list
        personList.append(newPerson)

        print("New patient added!\n")
        print(f"Number of patients currently in list is: {len(personList)}")

        return redirect(url_for("homePage"))
    
    # else condition for get request
    return render_template('questions.html', form=form)

if __name__ == "__main__":
    app.run(debug=True, port=8080)