import pandas as pd
import re

# Load the CSV file
file_path = 'Dicao_Shop_Cleaned2.csv'
df = pd.read_csv(file_path)
comment_counts = df['User'].value_counts()
threshold = 5
account_type = {account: ('bot' if count > threshold else 'normal') for account, count in comment_counts.items()}
df['type'] = df['User'].map(account_type)

# Define the function to clean the review
def clean_review_remove_specific_text(review, username, date):
    if not isinstance(review, str):
        return review
    review = re.sub(re.escape(username), '', review)
    if isinstance(date, str):
        review = re.sub(re.escape(date), '', review)

    review = re.sub(r'phản hồi của Người Bán.*$', '', review, flags=re.DOTALL)

    review = re.sub(r'dịch vụ để mang lại cho khách hàng.*hữu ích\?báo cáo', '', review)
    
    review = re.sub(r'hữu ích.*', '', review)

    # Remove everything after "phản hồi của Người Bán"
    
    # Clean up extra spaces and newlines
    review = re.sub(r'\s+', ' ', review).strip()
    
    
    # Optional: Filter out long comments
    if len(review) > 300:
        return ""
    
    return review

# Apply the function to the 'review' column
df['review'] = df.apply(lambda row: clean_review_remove_specific_text(row['review'], row['User'], row['date']), axis=1)

# Define and apply the rating extraction function
def extract_rating(raw_data):
    if raw_data == 'tất cả':
        return 5
    if isinstance(raw_data, str):
        return raw_data.strip()[0]
    elif pd.isna(raw_data):
        return 5  # Handle NaN values, or return a default rating if desired

df['rating'] = df['rating'].apply(extract_rating)

# Save the updated DataFrame to a new CSV file
output_path = 'Dicao_Shop_Cleaned_Final.csv'
df.to_csv(output_path, index=False)

print(f"File updated and saved to {output_path}")
