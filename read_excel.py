import pandas as pd
import openpyxl

# Read the Excel file
file_path = 'Case study for interns.xlsx'

# Load the workbook
wb = openpyxl.load_workbook(file_path)

# Print all sheet names
print("Sheet names:", wb.sheetnames)
print("\n" + "="*80 + "\n")

# Read the full sheet with all data
df = pd.read_excel(file_path, sheet_name='Rubrics', header=None)

print("Full DataFrame:")
print(df.to_string())
print("\n" + "="*80 + "\n")
