import pandas as pd
import re

# Load the CSV file into a DataFrame
df = pd.read_csv('/Users/admin/Documents/Data/Dicao_Shop/Dicao_Shop_CLeaned_Sentiment.csv')

# Define a function to clean and extract the sentiment
def clean_sentiment(row):
    review = row['review']
    sentiment = row['sentiment']
    
    # If the review is None, set sentiment to None
    if pd.isna(review):
        return None
    
    # Define the regex pattern to match the sentiment format
    if pd.isna(sentiment) or not isinstance(sentiment, str):
        return None
    pattern = r"{\s*'positive'\s*:\s*\d{1,3}%\s*,\s*'negative'\s*:\s*\d{1,3}%\s*}"
    
    # Try to find the sentiment pattern in the text
    match = re.search(pattern, sentiment, re.DOTALL)
    
    if match:
        # If a match is found, return the cleaned sentiment
        return match.group(0).replace('\n', '').replace('\r', '').replace(' ', '')
    else:
        # If no valid format is found, return None
        return None

# Apply the cleaning function to the sentiment column
df['sentiment'] = df.apply(clean_sentiment, axis=1)

# Save the cleaned DataFrame back to a CSV file
df.to_csv('/Users/admin/Documents/Data/Dicao_Shop/Dicao_Shop_CLeaned_Sentiment.csv', index=False)
