import pandas as pd
import os

# df = pd.read_csv('/Users/admin/Documents/Data/8YO_STUDIO_Shop/8yo_studio_product.csv')
df = []
df1 = pd.read_csv('Dicao_comments.csv')
df2 = pd.read_csv('add_Dicao_comments.csv')

df.append(df1)
df.append(df2)

combined_df = pd.concat(df, ignore_index=True)
combined_df.to_csv('Dicao_comments2.csv', index=False)