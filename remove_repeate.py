import pandas as pd

# Load the CSV file into a DataFrame
df = pd.read_csv('Dicao_Shop_Cleaned.csv')

# Assume the rating is in the fifth column (index 4), adjust if necessary
# Group by all columns except the rating column, and then take the row with the minimum rating
df = df.loc[df.groupby(["User", "ID", "date"])["rating"].idxmin()]

# Save the DataFrame back to a CSV file
df.to_csv('Dicao_Shop_Cleaned2.csv', index=False)