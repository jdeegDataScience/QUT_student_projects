USE COVID19_Survey;
GO

DROP PROCEDURE IF EXISTS create_python_model_dt;
GO

--a stored procedure to to train and generate a python classification model using decision tree algorithm, with a training_data supplied via an input param
CREATE PROCEDURE create_python_model_dt (@training_data_input NVARCHAR(max), @trained_model varbinary(max) OUTPUT)
AS
BEGIN
	EXECUTE sp_execute_external_script @language = N'Python'
	, @script = N'
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import pickle

y = training_data["Covid19_positive"]
X = training_data.drop(columns=["Covid19_positive"])
model_py = DecisionTreeClassifier()
model_py.fit(X, y)

print("Training Accuracy:", model_py.score(X_test, y_test))

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
import pandas as pd
from sklearn.naive_bayes import GaussianNB
import pickle

y = training_data["Covid19_positive"]
X = training_data.drop(columns=["Covid19_positive"])
model_py = GaussianNB()
model_py.fit(X, y)

print("Training Accuracy:", model_py.score(X_test, y_test))

binary_model = pickle.dumps(model_py)
trained_model_py = binary_model
'
	, @input_data_1 = @training_data_input
	, @input_data_1_name = N'training_data'
	, @params = N'@trained_model_py varbinary(max) OUTPUT'
	, @trained_model_py = @trained_model OUTPUT;
END
GO
