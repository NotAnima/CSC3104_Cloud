CREATE TABLE patient (
    id SERIAL PRIMARY KEY,
    high_bp REAL NOT NULL, -- 0 for Low Blood Pressure, 1 for High Blood Pressure
    high_chol REAL NOT NULL, -- 0 for No High Cholesterol, 1 for High Cholesterol
    chol_check REAL NOT NULL, -- 0 for Not in the last 5 years, 1 for Yes, within the last 5 years
    bmi REAL NOT NULL CHECK (bmi >= 0.0 AND bmi <= 251.1), -- BMI
    smoker REAL NOT NULL, -- 0 for No, 1 for Yes
    stroke REAL NOT NULL, -- 0 for No, 1 for Yes
    heart_disease_or_attack REAL NOT NULL, -- 0 for No, 1 for Yes
    phys_activity REAL NOT NULL, -- 0 for No, 1 for Yes
    fruits REAL NOT NULL, -- 0 for No, 1 for Yes
    veggies REAL NOT NULL, -- 0 for No, 1 for Yes
    hvy_alcohol_consump REAL NOT NULL, -- 0 for No, 1 for Yes
    phys_hlth REAL NOT NULL,
    diff_walk REAL NOT NULL, -- 0 for No, 1 for Yes
    sex REAL NOT NULL, -- 0 for Female, 1 for Male
    age REAL NOT NULL -- Age group, represented by numbers 1 through 13
);
