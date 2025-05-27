USE COVID19_Survey;
GO

/* Execution Scripts to create the training and test dataset*/

DROP TABLE IF EXISTS dbo.Training_Data;
GO

SELECT
    fs.Survey_ID, fs.Date,
    fs.Covid19_positive,
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
    fs.Covid19_positive,
    p.Gender, p.Age, p.Height, p.Weight, p.Bmi, p.BloodType, p.Insurance, p.Race,
    r.Smoking, r.Contact_count, r.House_count, r.Public_transport_count, r.Working,
    r.Covid19_symptoms, r.Covid19_contact, r.Asthma, r.Kidney_disease, r.Liver_disease,
    r.Compromised_immune, r.Heart_disease, r.Lung_disease, r.Diabetes, r.Hiv_positive,
    r.Hypertension, r.Other_chronic, r.Nursing_home, r.Health_worker
INTO dbo.Testing_Data
FROM dbo.Fact_survey AS fs
JOIN dbo.Participant AS p ON fs.Participant = p.Participant_ID
JOIN dbo.Response AS r ON fs.Response = r.Response_ID
WHERE (fs.Date BETWEEN '2020-04-01' AND '2020-04-30')
GO


/* Scripts to create "create model" stored procedures*/

DROP PROCEDURE IF EXISTS create_python_model_dt;
GO

--a stored procedure to to train and generate a python classification model using decision tree algorithm, with a training_data supplied via an input param
CREATE PROCEDURE create_python_model_dt (@training_data_input NVARCHAR(max), @trained_model varbinary(max) OUTPUT)
AS
BEGIN
	EXECUTE sp_execute_external_script @language = N'Python'
	, @script = N'
# import packages and libraries
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle

# split target and input attributes from dataset
y = training_data["Covid19_positive"]
X = training_data.drop(columns=["Covid19_positive"])

# train model
model_py = DecisionTreeClassifier()
model_py.fit(X, y)

print("Training Accuracy:", model_py.score(X, y))

# convert model to binary
binary_model = pickle.dumps(model_py)
trained_model_py = binary_model
'
	, @input_data_1 = @training_data_input
	, @input_data_1_name = N'training_data'
	, @params = N'@trained_model_py varbinary(max) OUTPUT'
	, @trained_model_py = @trained_model OUTPUT;
END
GO

DROP PROCEDURE IF EXISTS create_python_model_nb;
GO

--a stored procedure to to train and generate a python classification model using Naive Bayes algorithm, with a training_data supplied via an input param
CREATE PROCEDURE create_python_model_nb (@training_data_input NVARCHAR(max), @trained_model varbinary(max) OUTPUT)
AS
BEGIN
	EXECUTE sp_execute_external_script @language = N'Python'
	, @script = N'
# import packages and libraries
import pandas as pd
from sklearn.naive_bayes import GaussianNB
import pickle

# split target and input attributes from dataset
y = training_data["Covid19_positive"]
X = training_data.drop(columns=["Covid19_positive"])

# train model
model_py = GaussianNB()
model_py.fit(X, y)

print("Training Accuracy:", model_py.score(X, y))

# convert model to binary
binary_model = pickle.dumps(model_py)
trained_model_py = binary_model
'
	, @input_data_1 = @training_data_input
	, @input_data_1_name = N'training_data'
	, @params = N'@trained_model_py varbinary(max) OUTPUT'
	, @trained_model_py = @trained_model OUTPUT;
END
GO


/* Script to create "predict model" stored procedure*/

DROP PROCEDURE IF EXISTS predict_covid19_positive;
GO

-- A stored procedure to generate Covid19_positive predictions
CREATE PROCEDURE predict_covid19_positive (@testing_data_input NVARCHAR(max), @model VARCHAR(100))
AS
BEGIN
	-- use @model input param to select model from COVID19_ML_models table
	DECLARE @input_model VARBINARY(max) = (SELECT model FROM COVID19_ML_models
	WHERE model_name = @model);
	EXECUTE sp_execute_external_script @language = N'Python'
	, @script = N'
# import packages and libraries
import pandas as pd
import pickle

# convert model from binary
classifier = pickle.loads(model_py)

# split target and input attributes from dataset
y_test = test_data["Covid19_positive"]
X_test = test_data.drop(columns=["Covid19_positive", "Survey_ID"], errors="ignore")

# predict using input attributes
covid19_positive_pred = classifier.predict(X_test)

# Performance evaluation
print("\n", model_name)
print("\n Metrics.Accuracy=", metrics.accuracy_score(y_test, covid19_positive_pred))
print("\n Metrics.precision_score=", metrics.precision_score(y_test, covid19_positive_pred, average = "weighted"))
print("\n Metrics.recall_score=", metrics.recall_score(y_test, covid19_positive_pred, average = "weighted"))
print("\n Metrics.f1 score=", metrics.f1_score(y_test, covid19_positive_pred, average = "weighted"))

# add prediction to the input dataset
test_data["PredictedPositive"] = covid19_positive_pred

# select columns for the output dataset
OutputDataSet = test_data[["Survey_ID","PredictedPositive","Covid19_positive"]]
	'
	, @input_data_1 = @testing_data_input, @input_data_1_name = N'test_data'
	, @params = N'@model_py varbinary(max), @model_name VARCHAR(100)'
	, @model_py = @input_model, @model_name = @model
	WITH RESULT SETS((
	"Survey_ID" INT, "Predicted" INT, "Actual" INT
	));
END
GO

/* Execution scripts to use stored procedures to generate DT/GaussianNB models for each feature set*/

DECLARE @new_model_name_dt_2 varchar(50);
SET @new_model_name_dt_2 = 'Decision Tree (2 Features)';
DECLARE @new_model_name_nb_2 varchar(50);
SET @new_model_name_nb_2 = 'GauusianNB (2 Features)';

DECLARE @training_data_query_2 nvarchar(max);
SET @training_data_query_2 = 'SELECT Covid19_positive,
Covid19_symptoms, Covid19_contact
FROM COVID19_Survey.dbo.Training_Data';

DECLARE @model_dt_2 varbinary(max);
EXECUTE create_python_model_dt @training_data_query_2, @model_dt_2 OUTPUT;
DECLARE @model_nb_2 varbinary(max);
EXECUTE create_python_model_nb @training_data_query_2, @model_nb_2 OUTPUT;

DELETE COVID19_ML_models WHERE model_name IN (@new_model_name_dt_2, @new_model_name_nb_2);
INSERT INTO COVID19_ML_models (model_name, model)
values(@new_model_name_dt_2, @model_dt_2), (@new_model_name_nb_2, @model_nb_2);
GO

DECLARE @new_model_name_dt_11 varchar(50);
SET @new_model_name_dt_11 = 'Decision Tree (11 Features)';
DECLARE @new_model_name_nb_11 varchar(50);
SET @new_model_name_nb_11 = 'GauusianNB (11 Features)';

DECLARE @training_data_query_11 nvarchar(max);
SET @training_data_query_11 = 'SELECT Covid19_positive,
Covid19_symptoms, Covid19_contact, Bmi, House_count,
Weight, Contact_count, Kidney_disease, Height,
Compromised_immune, Nursing_home, Diabetes
FROM COVID19_Survey.dbo.Training_Data';

DECLARE @model_dt_11 varbinary(max);
EXECUTE create_python_model_dt @training_data_query_11, @model_dt_11 OUTPUT;
DECLARE @model_nb_11 varbinary(max);
EXECUTE create_python_model_nb @training_data_query_11, @model_nb_11 OUTPUT;

DELETE COVID19_ML_models WHERE model_name IN (@new_model_name_dt_11, @new_model_name_nb_11);
INSERT INTO COVID19_ML_models (model_name, model)
values(@new_model_name_dt_11, @model_dt_11), (@new_model_name_nb_11, @model_nb_11);
GO


/* Execution scripts to use stored procedure to generate predictions and evaluation metrics models for each model*/

DECLARE @model_dt_2 varchar(50);
SET @model_dt_2 = 'Decision Tree (2 Features)';
DECLARE @model_nb_2 varchar(50);
SET @model_nb_2 = 'GauusianNB (2 Features)';

DECLARE @test_data_query_2 nvarchar(max);
SET @test_data_query_2 = 'SELECT Survey_ID, Covid19_positive,
Covid19_symptoms, Covid19_contact
FROM COVID19_Survey.dbo.Testing_Data';

EXECUTE predict_covid19_positive @test_data_query_2, @model_nb_2;
EXECUTE predict_covid19_positive @test_data_query_2, @model_dt_2;
GO

DECLARE @model_dt_11 varchar(50);
SET @model_dt_11 = 'Decision Tree (11 Features)';
DECLARE @model_nb_11 varchar(50);
SET @model_nb_11 = 'GauusianNB (11 Features)';

DECLARE @test_data_query_11 nvarchar(max);
SET @test_data_query_11 = 'SELECT Survey_ID, Covid19_positive,
Covid19_symptoms, Covid19_contact, Bmi, House_count,
Weight, Contact_count, Kidney_disease, Height,
Compromised_immune, Nursing_home, Diabetes
FROM COVID19_Survey.dbo.Testing_Data';


EXECUTE predict_covid19_positive @test_data_query_11, @model_nb_11;
EXECUTE predict_covid19_positive @test_data_query_11, @model_dt_11;
GO