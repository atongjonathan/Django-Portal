import pandas as pd
import os
import json


def combine_data():
    with open(os.path.join(os.path.dirname(__file__), "static/portal/db", "ARK JUNIOR KITENGELA_Cust_ Ledg_ Entry.csv")) as file:
        normal = pd.read_csv(file)
    with open(os.path.join(os.path.dirname(__file__), "static/portal/db", "ARK JUNIOR KITENGELA_Detailed Cust_ Ledg_ Entry.csv")) as file:
        detailed = pd.read_csv(file)
    renamed_detailed = detailed.rename(
        columns={'Cust_ Ledger Entry No_': 'Entry No_'})
    combined_df = pd.merge(renamed_detailed, normal, on='Entry No_')
    return combined_df


def get_statements(id):
    combined = combine_data()
    student = combined.loc[combined["Customer No__x"] == id]
    student_2023 = student[student['Posting Date_x'].str.contains("2023")]
    student_2023.drop(columns=["Posting Date_y", "Customer No__y",
                      "Customer No__x", "Amount", "Entry No_"], inplace=True)
    student_2023.rename(columns={'Posting Date_x': 'date', 'Description': 'particular',
                        'Debit Amount': 'debit', 'Credit Amount': 'credit'}, inplace=True)
    return student_2023.to_dict()


print(json.dumps(get_statements("STU-0246"), indent=4))
