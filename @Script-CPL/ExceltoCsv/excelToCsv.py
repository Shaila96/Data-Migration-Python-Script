import pandas as pd

def csv_from_excel (xls_filename, csv_filename):
    data_xls = pd.read_excel(xls_filename)
    data_xls = data_xls[8:]
    data_xls.to_csv(csv_filename, encoding='utf-8', index=False, header=None)


csv_from_excel("Excel\Subject01.bar.xlsx", "Csv\excel_to_csv.csv")