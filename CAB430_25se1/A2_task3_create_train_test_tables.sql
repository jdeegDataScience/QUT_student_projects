USE COVID19_Survey;
GO

DROP TABLE IF EXISTS dbo.Training_Data;
GO

SELECT
    fs.Survey_ID, fs.Date,
    fs.Risk_infection_level,
    p.Gender, p.Age, p.Height, p.Weight, p.Bmi, p.BloodType, p.Insurance, p.Race,
    r.Smoking, r.Contact_count, r.House_count, r.Public_transport_count, r.Working,
    r.Covid19_symptoms, r.Covid19_contact, r.Asthma, r.Kidney_disease, r.Liver_disease,
    r.Compromised_immune, r.Heart_disease, r.Lung_disease, r.Diabetes, r.Hiv_positive,
    r.Hypertension, r.Other_chronic, r.Nursing_home, r.Health_worker
INTO dbo.Training_Data
FROM dbo.Fact_survey AS fs
JOIN dbo.Participant AS p ON fs.Participant = p.Participant_ID
JOIN dbo.Response AS r ON fs.Response = r.Response_ID
WHERE (fs.Date BETWEEN '2020-05-01' AND '2020-07-31')
GO

DROP TABLE IF EXISTS dbo.Testing_Data;
GO

SELECT
    fs.Survey_ID, fs.Date,
    fs.Risk_infection_level,
    p.Gender, p.Age, p.Height, p.Weight, p.Bmi, p.BloodType, p.Insurance, p.Race,
    r.Smoking, r.Contact_count, r.House_count, r.Public_transport_count, r.Working,
    r.Covid19_symptoms, r.Covid19_contact, r.Asthma, r.Kidney_disease, r.Liver_disease,
    r.Compromised_immune, r.Heart_disease, r.Lung_disease, r.Diabetes, r.Hiv_positive,
    r.Hypertension, r.Other_chronic, r.Nursing_home, r.Health_worker
INTO dbo.Testing_Data
FROM dbo.Fact_survey AS fs
JOIN dbo.Participant AS p ON fs.Participant = p.Participant_ID
JOIN dbo.Response AS r ON fs.Response = r.Response_ID
WHERE (fs.Date NOT BETWEEN '2020-05-01' AND '2020-07-31')
GO
