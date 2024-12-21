import os
import pandas as pd
import csv
import shutil

# Đường dẫn thư mục chứa các file CSV
document_folder = r"/Users/admin/Documents/Data/Dicao_Shop/add_comments"
# output_file = 'Wearit_Shop_comments'

# Ensure the directory for the output file exists
# output_directory = os.path.dirname(output_file)
# if not os.path.exists(output_directory):
#     os.makedirs(output_directory)S

# Load the existing CSV with ID column
df2 = pd.read_csv(r'/Users/admin/Documents/Data/Coudzy_Shop/products.csv')

def remove_newlines_in_field(value):
    if isinstance(value, str):
        return value.replace('\n', ' ').replace('\r', ' ')
    return value
dataframes = []
# Process each CSV file in the document folder
for filename in os.listdir(document_folder):
    if filename.endswith('.csv'):
        file_path = os.path.join(document_folder, filename)
        
        # Read the CSV file
        df = pd.read_csv(file_path, encoding='utf-8', quoting=csv.QUOTE_ALL)

        # Remove newlines from all fields
        df = df.applymap(remove_newlines_in_field)

        # Add a new column with the product ID based on the filename
        id_product = os.path.splitext(filename)[0].strip()
        df['ID'] = id_product
        
        # Reorder columns to place ID at the front
        df = df[['ID'] + df.columns[:-1].tolist()]

        dataframes.append(df)
        
        # Optionally move the processed file to another directory
        # shutil.move(file_path, os.path.join(mycsv_folder, filename))
combined_df = pd.concat(dataframes, ignore_index=True)
combined_df.to_csv('add_Dicao_comments.csv', index=False)

print("Hoàn thành!")
