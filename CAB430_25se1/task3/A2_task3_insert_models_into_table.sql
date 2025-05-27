USE COVID19_Survey;
GO

DECLARE @new_model_name_dt_2 varchar(50);
SET @new_model_name_dt_2 = 'Decision Tree (2 Features)';
DECLARE @new_model_name_nb_2 varchar(50);
SET @new_model_name_nb_2 = 'GauusianNB (2 Features)';

DECLARE @input_data_query_2 nvarchar(max);
SET @input_data_query_2 = 'SELECT Covid19_positive,
Covid19_symptoms, Covid19_contact
FROM COVID19_Survey.dbo.Training_Data';

DECLARE @model_dt_2 varbinary(max);
EXECUTE create_python_model_dt @input_data_query_2, @model_dt_2 OUTPUT;
DECLARE @model_nb_2 varbinary(max);
EXECUTE create_python_model_nb @input_data_query_2, @model_nb_2 OUTPUT;

DELETE COVID19_ML_models WHERE model_name IN (@new_model_name_dt_2, @new_model_name_nb_2);
INSERT INTO COVID19_ML_models (model_name, model)
values(@new_model_name_dt_2, @model_dt_2), (@new_model_name_nb_2, @model_nb_2);
GO

DECLARE @new_model_name_dt_11 varchar(50);
SET @new_model_name_dt_11 = 'Decision Tree (11 Features)';
DECLARE @new_model_name_nb_11 varchar(50);
SET @new_model_name_nb_11 = 'GauusianNB (11 Features)';

DECLARE @input_data_query_11 nvarchar(max);
SET @input_data_query_11 = 'SELECT Covid19_positive,
Covid19_symptoms, Covid19_contact, Bmi, House_count,
Weight, Contact_count, Kidney_disease, Height,
Compromised_immune, Nursing_home, Diabetes
FROM COVID19_Survey.dbo.Training_Data';

DECLARE @model_dt_11 varbinary(max);
EXECUTE create_python_model_dt @input_data_query_11, @model_dt_11 OUTPUT;
DECLARE @model_nb_11 varbinary(max);
EXECUTE create_python_model_nb @input_data_query_11, @model_nb_11 OUTPUT;

DELETE COVID19_ML_models WHERE model_name IN (@new_model_name_dt_11, @new_model_name_nb_11);
INSERT INTO COVID19_ML_models (model_name, model)
values(@new_model_name_dt_11, @model_dt_11), (@new_model_name_nb_11, @model_nb_11);
GO
