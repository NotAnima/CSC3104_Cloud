# CSC3104_Cloud

## Dataset Used
> https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset/data?select=diabetes_binary_5050split_health_indicators_BRFSS2015.csv

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
4. CholCheck - Whether the person has high cholestrol or not 
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
11. Veggies - Whether the person consumes fruit 1 or more times per day
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
16. MentHlth
    - 0: No 
    - 1: Yes
17. PhysHlth
    - 0: No 
    - 1: Yes
18. DiffWalk - Whether the person has serious difficulty walking or climbing stairs
    - 0: No 
    - 1: Yes
19. Sex
    - 0: Female
    - 1: Male
20. Age - 13-level age category (AGEG5YR see codebook)
    - 1: 18-24
    - 9: 60-64
    - 13: 80 or older 
21. Education - Education level (EDUCA see codebook) scale 1-6
    - 1: Never attended school or only kindergarten  
    - 2: Grades 1 through 8
22. Income - Income scale (INCOME2 see codebook) scale 1-8 
    - 1: less than $10,000
    - 5: less than $35,000
    - 8: $75,000 or more

## Points to do

- Web Application
- Curate training data sets and probably sort it
- Establish centralised docker container node and respective nodes
- Test out prototyping for federated learning

### Additional features(?)
- No idea at the moment
