import pytd
import pandas as pd


def execute_sql_and_get_csv(database_name, sql_query):
    res = perform_sql(database_name, sql_query)
    return convert_result_to_csv(res)


def perform_sql(database_name, sql_query):
    client = pytd.Client(database=database_name)
    res = client.query(sql_query)
    return res


def convert_result_to_csv(res):
    csv = pd.DataFrame(**res).to_csv(index=False)
    return csv
