import pandas as pd
import os


def combine_data():
    with open(os.path.join(os.path.dirname(__file__), "static/portal/db", "ARK JUNIOR KITENGELA_Cust_ Ledg_ Entry.csv")) as file:
        normal = pd.read_csv(file)
    with open(os.path.join(os.path.dirname(__file__), "static/portal/db", "ARK JUNIOR KITENGELA_Detailed Cust_ Ledg_ Entry.csv")) as file:
        detailed = pd.read_csv(file)
    renamed_detailed = detailed.rename(
        columns={'Cust_ Ledger Entry No_': 'Entry No_'})
    combined_df = pd.merge(renamed_detailed, normal, on='Entry No_')
    return combined_df.drop_duplicates()


def get_statements(id, year=None):
    combined = combine_data()
    student = combined.loc[combined["Customer No__x"]
                           == id].copy()  # Make a copy of the DataFrame

    # student_2023 = student[~student['Posting Date_x'].str.contains("2023")] if year is not None else student[student['Posting Date_x'].str.contains("2023")]
    student_2023 = student
    student_2023.drop(columns=["Posting Date_y", "Customer No__y",
                               "Customer No__x", "Amount", "Entry No_"], inplace=True)
    student_2023.rename(columns={'Posting Date_x': 'date', 'Description': 'particular',
                                 'Debit Amount': 'debit', 'Credit Amount': 'credit'}, inplace=True)
    student_2023["date"] = pd.to_datetime(student_2023["date"])
    df_sorted = student_2023.sort_values(by="date")
    df_sorted['date'] = df_sorted['date'].dt.strftime('%d/%m/%y')

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


# print(get_statements("STU-0227")[1])
