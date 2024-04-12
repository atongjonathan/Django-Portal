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
    return combined_df.drop_duplicates()


def get_child_data():
    with open(os.path.join(os.path.dirname(__file__), "static/portal/db", "ARK JUNIOR KITENGELA$Customer.csv")) as file:
        customer = pd.read_csv(file)

    customer.rename(columns={
        'No_': 'id',
        'Name': 'name',
        'Customer Posting Group': 'group',
        'E-Mail': 'email',
        'Gender': 'gender',
        'Date Of Birth': 'dob',
        'Current Programme': 'programme',
        'Current Stage': 'stage',
        'Fathers Name': 'f_name',
        'Fathers Email': 'f_email',
        'Fathers ID NO': 'f_id',
        'Fathers Nationality': 'f_nation',
        'Fathers Occupation': 'f_occupation',
        'Fathers Tel No': 'f_tel',
        'Mothers Name': 'm_name',
        'Mothers Email': 'm_email',
        'Mothers ID NO': 'm_id',
        'Mothers Nationality': 'm_nation',
        'Mothers Occupation': 'm_occupation',
        'Mothers Tel No': 'm_tel',
    }, inplace=True)
    return customer.to_dict("records")


def get_statements(id):
    try:
        combined = combine_data()
        student_2023 = combined.loc[combined["Customer No__x"]
                                    == id].copy()  # Make a copy of the DataFrame
        student_2023.drop(columns=["Posting Date_y", "Customer No__y",
                                   "Customer No__x", "Amount", "Entry No_"], inplace=True)
        student_2023.rename(columns={'Posting Date_x': 'date', 'Description': 'particular',
                                     'Debit Amount': 'debit', 'Credit Amount': 'credit'}, inplace=True)
        student_2023["date"] = pd.to_datetime(student_2023["date"])
        df_sorted = student_2023.sort_values(by="date")
        df_sorted['date'] = df_sorted['date'].dt.strftime('%d/%m/%y')
    except FileNotFoundError:
        sample_data = [
            {
                "date":"01/05/19",
                "debit":5000.0,
                "credit":0.0,
                "particular":"Enrollment Fee"
            }
        ]
        df_sorted = pd.DataFrame(sample_data)        
    return format_data(df_sorted)


def format_data(student_2023):
    bal = 0
    student_2023 = student_2023.to_dict("records")
    unbilling = []
    for row in student_2023:
        if row["debit"] < 0:
            un_data = row
            un_data["debit"] = un_data["debit"]*-1
            unbilling.append(un_data)
    student_2023 = [row for row in student_2023 if row not in unbilling]
    for row in student_2023:
        bal = bal + row["debit"] - row["credit"]
        row["debit"] = format(row["debit"], ',.2f')
        row["credit"] = format(
            row["credit"], ',.2f')
        row["bal"] = format(bal, ',.2f')
    return student_2023

# print(json.dumps( get_child_data(), indent=4))
