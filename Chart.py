import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re  # Thư viện để xử lý regex

# Đọc dữ liệu
file_path = 'merged_shops.csv'
data = pd.read_csv(file_path)

# Xử lý thiếu dữ liệu
data = data.dropna(subset=['rating', 'sentiment'])

# Loại bỏ ký tự `%` và chuyển chuỗi thành từ điển
def process_sentiment(sentiment_str):
    # Loại bỏ ký tự `%`
    sentiment_str = re.sub(r'%', '', sentiment_str)
    # Chuyển đổi chuỗi thành từ điển
    sentiment_dict = eval(sentiment_str.replace("'", '"'))
    return sentiment_dict

data['sentiment_dict'] = data['sentiment'].apply(process_sentiment)
data['positive'] = data['sentiment_dict'].apply(lambda x: x['positive'])
data['negative'] = data['sentiment_dict'].apply(lambda x: x['negative'])

# Tính toán tổng hợp
data_grouped = data.groupby('shop_id').agg(
    total_reviews=('rating', 'count'),
    avg_rating=('rating', 'mean'),
    total_positive=('positive', 'sum'),
    total_negative=('negative', 'sum')
).reset_index()

data_grouped['positive_ratio'] = data_grouped['total_positive'] / (data_grouped['total_positive'] + data_grouped['total_negative'])
data_grouped['negative_ratio'] = data_grouped['total_negative'] / (data_grouped['total_positive'] + data_grouped['total_negative'])

# Vẽ biểu đồ
plt.figure(figsize=(18, 12))

# # Biểu đồ 1: Histogram điểm đánh giá trung bình
# plt.subplot(2, 2, 1)
# sns.histplot(data_grouped['avg_rating'].dropna(), kde=True, bins=15, color='skyblue')
# plt.title("Histogram of Average Rating")
# plt.xlabel("Average Rating")
# plt.ylabel("Number of Shops")

# Biểu đồ 2: Tỷ lệ cảm xúc tích cực của top 5 cửa hàng lớn nhất (theo tổng số lượng đánh giá)
# plt.subplot(2, 2, 2)
# top_5_shops = data_grouped.nlargest(5, 'total_reviews')
# top_5_shops_ratio = top_5_shops[['shop_id', 'positive_ratio', 'negative_ratio']].set_index('shop_id')
# top_5_shops_ratio.plot(kind='bar', stacked=True, color=['green', 'red'], ax=plt.gca())
# plt.title("Sentiment rate of shops")
# plt.xlabel("Shop")
# plt.ylabel("Sentiment rate")
# plt.legend(["Positive", "Negative"])

# Biểu đồ 3: Scatter plot - Mối quan hệ giữa số lượng đánh giá và điểm trung bình
# plt.subplot(2, 2, 2)
# sns.scatterplot(data=data_grouped, x='total_reviews', y='avg_rating', color='blue')
# plt.title("Relationship between number of reviews and average score")
# plt.xlabel("Rating count")
# plt.ylabel("Average rating")
#
# # Biểu đồ 4: Top 10 cửa hàng có cảm xúc tiêu cực cao nhất
plt.subplot(2, 2, 2)
top_negative = data_grouped.nlargest(5, 'total_negative')
sns.barplot(data=top_10_negative, x='total_negative', y='shop_id', color='salmon')
plt.title("Top shop with highest negative sentiment")
plt.xlabel("Negative sentiment count")
plt.ylabel("Shop")

plt.tight_layout()
plt.show()
