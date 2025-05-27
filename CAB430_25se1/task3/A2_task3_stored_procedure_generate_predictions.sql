USE COVID19_Survey;
GO

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
