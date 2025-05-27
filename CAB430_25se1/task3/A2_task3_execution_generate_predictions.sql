USE COVID19_Survey;
GO

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
