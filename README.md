# CSC3104_Cloud

All code contents are referred within the [git repository](https://github.com/NotAnima/CSC3104_Cloud)
Branch: Integration
# Client Setup
1. Directory location: Client
2. `kubectl apply -f  .`

>[!info]
All clients will establish a connection with the server on the public domain (dereknan.click) which is running an instance of the server below. As such, deployment of the server is not required but if you still wish to deploy your own server, you may do so.

# Server Setup
If you choose to setup your own server, you will need to edit the `flask-deployment.yml` file
1. Change the value of the `DOMAIN` environment variable to wherever your destination is.

These instructions are to set up the federated server as shown in the system design in our article. We have already set up the client such that it will automatically connect to the server we have created. If you still wish to deploy the server, the instructions are as follows:

1. Directory location: Server
2. YAML file used: `server-deployment.yaml`
3. `kubectl apply -f server-deployment.yaml`
  
---
# Test Result of model
If you wish to test the accuracy of your model, we have created a script to run showing the accuracy of the model. Instructions to do so are as follows:

Before running the test.py file, retrieve the model file from the client through the command. 
1. Get name of pod with `kubectl get pods`
2. Extract model out from system with `kubectl exec -it (name of pod) -- cat /app/model.pkl > (destination on host system)`
3. Install all dependencies for python using `pip install -r ./requirements.txt`

For demonstration purposes, a `baseModel.pkl` has also been provided within the TestResults directory.

Once the model from the server has been retrieved
1. Directory location: TestResults
2. Required Files: diabetes.py, diabetes_15_columns.csv, test.py baseMode.pkl
3. Simply run test.py `python test.py`

## Dataset Used
> [Dataset Used](https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset/data?select=diabetes_binary_5050split_health_indicators_BRFSS2015.csv)

This dataset is a labelled dataset from the Behavioral Risk Factor Surveillance System (BRFSS). The BRFSS is a health-related telephone survey that has been conducted anually by the CDC. 

### Dataset Legend
1. Diabetes_012 - Whether person has diabetes, prediabetes or no diabetes.
    - 0: No diabetes
    - 1: Prediabetes
    - 2: Diabetes
2. HighBP - Whether the person has high blood pressure or not.
    - 0: Low blood pressure
    - 1: High blood pressure
3. HighChol - Whether the person has high cholestrol or not 
    - 0: No high cholestrol
    - 1: High cholestrol
4. CholCheck - Whether the person has high cholestrol or not in 5 years
    - 0: No high cholestrol
    - 1: High cholestrol
5. BMI - Person's Body Mass Index 
6. Smoker - Whether the person has smoked at least 100 cigarettes in their entire life
    - 0: No 
    - 1: Yes
7. Stroke - Whether the person has ever had a stroke 
    - 0: No 
    - 1: Yes
8. HeartDisease - Whether the person has coronary heart disease (CHD) or myocardial infarction (MI) 
    - 0: No 
    - 1: Yes
9. PhysActiv - Whether person has physical activity in past 30 days - not including job 
    - 0: No 
    - 1: Yes
10. Fruits - Whether the person consumes fruit 1 or more times per day
    - 0: No 
    - 1: Yes
11. Veggies - Whether the person consumes vegetables 1 or more times per day
    - 0: No 
    - 1: Yes
12. HvyAlcoholConsump - Whether the person is a Heavy drinker (adult men having more than 14 drinks per week and adult women having more than 7 drinks per week)
    - 0: No 
    - 1: Yes
13. AnyHealthcare - Whether the person has any kind of health care coverage, including health insurance, prepaid plans such as HMO, etc.
    - 0: No 
    - 1: Yes
14. NoDocbcCost - Whether the person had a time in the past 12 months where they needed to see a doctor but could not because of cost? 
    - 0: No 
    - 1: Yes
15. GenHlth - Person's general your health
    - 1 = excellent 
    - 2 = very good 
    - 3 = good 
    - 4 = fair 
    - 5 = poor
16. MentHlth -  How many days in the past 30 days was the person's mental health not good. Scale 1-30 days, includes stress, depression, and problems with emotions
17. PhysHlth - How many days in the past 30 days was the person's physical health not good. scale 1-30 days, includes physical illness and injury, 
18. DiffWalk - Whether the person has serious difficulty walking or climbing stairs
    - 0: No 
    - 1: Yes
19. Sex - Person's sex
    - 0: Female
    - 1: Male
20. Age - 13-level age category
    - 1: 18-24
    - 2: 25-29
    - 3: 30-34
    - 4: 35-39
    - 5: 40-44
    - 6: 45-49
    - 7: 50-54
    - 8: 55-59
    - 9: 60-64
    - 10: 65-69
    - 11: 70-74
    - 12: 75-79
    - 13: 80 or older 
21. Education - Education level on a scale of 1-6
    - 1: Never attended school or only kindergarten  
    - 2: Grades 1 through 8 (Elementary)
    - 3: Grades 9 through 11 (Some high school) 
    - 4: Grade 12 or GED (High school graduate) 
    - 5: College 1 year to 3 years (Some college or technical school) 
    - 6: College 4 years or more (College graduate)
22. Income - Income scale (INCOME2 see codebook) scale 1-8 
    - 1: Less than $10,000
    - 2: $10,000 to less than $15,000
    - 3: $15,000 to less than $20,000
    - 4: $20,000 to less than $25,000
    - 5: $25,000 to less than $35,000
    - 6: $35,000 to less than $50,000
    - 7: $50,000 to less than $75,000
    - 8: $75,000 or more

## Points to do

- Web Application
- Curate training data sets and probably sort it
- Establish centralised docker container node and respective nodes
- Test out prototyping for federated learning

### Additional features(?)
- No idea at the moment

## Required Questions

### HighBP - Whether the person has high blood pressure or not.
- 0: Low blood pressure
- 1: High blood pressure
### HighChol - Whether the person has high cholestrol or not
- 0: No high cholestrol
- 1: High cholestrol
### CholCheck - Whether the person has high cholestrol or not
- 0: No high cholestrol
- 1: High cholestrol
### BMI - Person's Body Mass Index
### Smoker - Whether the person has smoked at least 100 cigarettes in their entire life
- 0: No
- 1: Yes
### Stroke - Whether the person has ever had a stroke
- 0: No
- 1: Yes
### HeartDisease - Whether the person has coronary heart disease (CHD) or myocardial infarction (MI)
- 0: No
- 1: Yes
### PhysActiv - Whether person has physical activity in past 30 days - not including job
- 0: No
- 1: Yes
### Fruits - Whether the person consumes fruit 1 or more times per day
- 0: No
- 1: Yes
### Veggies - Whether the person consumes fruit 1 or more times per day
- 0: No
- 1: Yes
### HvyAlcoholConsump - Whether the person is a Heavy drinker (adult men having more than 14 drinks per week and adult women having more than 7 drinks per week)
- 0: No
- 1: Yes
### DiffWalk - Whether the person has serious difficulty walking or climbing stairs
- 0: No
- 1: Yes
### Sex
- 0: Female
- 1: Male
### Age - 13-level age category (AGEG5YR see codebook)
- 1: 18-24
- 9: 60-64
- 13: 80 or older
- 2-8 will just be within bins (refer to darren's message on Telegram)
