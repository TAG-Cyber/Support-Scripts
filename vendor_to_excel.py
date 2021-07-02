import pandas
import json

# read the csv into the dataframe
vendors_df = pandas.read_csv(r'vendors.csv')

list_of_columns = list(vendors_df.columns)

vendors_df_new = vendors_df.rename(columns={0: 'name', 1: 'website', 2: 'overview', 3: 'headquarters', 4: 'controls'}) 

writer = pandas.ExcelWriter('vendors.xlsx', engine='xlsxwriter')

vendors_df_new.to_excel(writer, sheet_name="vendors")

# read controls from json
with open('controls.json') as json_file:
    vendor_dict = json.load(json_file)

vendors_control_df = pandas.DataFrame.from_dict(vendor_dict, orient="index")

vendors_control_df.to_excel(writer, sheet_name="controls")

writer.save()

print(pandas.Index(vendors_control_df))

