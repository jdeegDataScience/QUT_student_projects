import pyodbc
import pandas as pd

def import_sql_db_COVID19_Survey():
    # Open a connection to SQL Server COVID19_Survey database
    conn = pyodbc.connect(
        "Driver={ODBC Driver 17 for SQL Server};"
        "Server=localhost;"
        "Database=COVID19_Survey;"
        "Trusted_Connection=yes;"
    )

    # Write query that joins Fact_survey to Participant to Response
    # and selects only the numeric & bool/bit columns plus the two targets
    # boolean/bit flags are cast as INT so that pandas sees them as numeric
    sql = """
    SELECT
      fs.Risk_infection,
      fs.Covid19_positive,

      p.Height,
      p.Weight,
      p.Bmi,

      r.Contact_count,
      r.House_count,
      r.Public_transport_count,

      CAST(r.Covid19_symptoms AS INT) AS Covid19_symptoms,
      CAST(r.Covid19_contact  AS INT) AS Covid19_contact,
      CAST(r.Asthma AS INT) AS Asthma,
      CAST(r.Kidney_disease AS INT) AS Kidney_disease,
      CAST(r.Liver_disease AS INT) AS Liver_disease,
      CAST(r.Compromised_immune AS INT) AS Compromised_immune,
      CAST(r.Heart_disease AS INT) AS Heart_disease,
      CAST(r.Lung_disease AS INT) AS Lung_disease,
      CAST(r.Diabetes AS INT) AS Diabetes,
      CAST(r.Hiv_positive AS INT) AS Hiv_positive,
      CAST(r.Hypertension AS INT) AS Hypertension,
      CAST(r.Other_chronic AS INT) AS Other_chronic,
      CAST(r.Nursing_home AS INT) AS Nursing_home,
      CAST(r.Health_worker AS INT) AS Health_worker
    FROM dbo.Fact_survey AS fs
    JOIN dbo.Participant AS p
      ON fs.Participant = p.Participant_ID
    JOIN dbo.Response AS r
      ON fs.Response = r.Response_ID
    WHERE fs.Risk_infection IS NOT NULL
      AND fs.Covid19_positive IS NOT NULL;
    """

    # Load into DataFrame
    df = pd.read_sql(sql, conn)
    conn.close()
    
    return df
