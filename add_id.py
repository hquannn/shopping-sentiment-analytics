import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('/Users/admin/Documents/Data/Wearit_Shop/products.csv')

# Add an ID column (starting from 1)
df['ID'] = range(1, len(df) + 1)

# Reorder columns to make 'ID' the first column
columns = ['ID'] + [col for col in df.columns if col != 'ID']
df = df[columns]

# Save the DataFrame back to a CSV file
df.to_csv('/Users/admin/Documents/Data/Wearit_Shop/products.csv', index=False)
