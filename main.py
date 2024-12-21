import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

files = {
    "Data/8YO_Shop/8YO_Shop_Cleaned_Sentiment.csv": "8YO",
    "Data/Cloudzy_Shop/Cloudzy_Shop_Cleaned_Sentiment.csv": "Cloudzy",
    "Data/Dicao_Shop/Dicao_Shop_Cleaned_Sentiment.csv": "Dicao",
    "Data/Ulzzang_Shop/Ulzzang_Shop_Cleaned_Sentiment.csv": "Ulzzang",
    "Data/Wearit_Shop/Wearit_Shop_Cleaned_Sentiment.csv": "Wearit"
}

dataframes = []

for file, shop_id in files.items():

    df = pd.read_csv(file)

    df["shop_id"] = shop_id

    if "id" in df.columns:
        df["id"] = df["id"].apply(lambda x: f"{shop_id}_{x}")

    # Lưu DataFrame vào danh sách
    dataframes.append(df)

merged_data = pd.concat(dataframes, ignore_index=True)

merged_data.to_csv("merged_shops.csv", index=False)

df = pd.read_csv('merged_shops.csv')

# df_numeric = df.select_dtypes(include=['number'])
# data_count = df_numeric.count()
# row_means = df_numeric.mean(axis=1)
# column_means = df_numeric.mean(axis=0)
# column_medians = df_numeric.median()
# column_modes = df_numeric.mode()
# column_max = df_numeric.max()
# column_min = df_numeric.min()
# column_q1 = df_numeric.quantile(0.25)
# column_q2 = df_numeric.median()
# column_q3 = df_numeric.quantile(0.75)
# column_IQR = column_q3 - column_q1
# column_variances = df_numeric.var()
# column_std_devs = df_numeric.std()
#
# colum_skewness = df_numeric.skew()
# column_kurtosis =  df_numeric.kurtosis()
#
#
#
# def descriptive(data_count, column_min, column_max, column_medians, column_modes, column_q1, column_q2, column_q3,
#                 column_IQR, column_variances, column_std_devs, column_skewness, column_kurtosis):
#     data = {'Count': [i for i in data_count],
#             'min': [i for i in column_min],
#             'max': [i for i in column_max],
#             'median': [i for i in column_medians],
#             'mode': [i for i in column_modes.values[0]],
#             'Q1': [i for i in column_q1],
#             'Q2': [i for i in column_q2],
#             'Q3': [i for i in column_q3],
#             'IQR': [i for i in column_IQR],
#             'Variance': [i for i in column_variances],
#             'stdev': [i for i in column_std_devs],
#             'skewness': [i for i in column_skewness],
#             'kurtosis': [i for i in column_kurtosis]
#             }  # dữ liệu đang ở dạng dic
#     df1 = pd.DataFrame(data)
#     df1.index = df_numeric.keys()
#     data_complete = df1.transpose()
#
#     new_column_data = ['count', 'min', 'max', 'median', 'mode', 'Q1', 'Q2', 'Q3', 'IQR',
#                        'Variance', 'stdev', 'skewness', 'kurtosis']
#     column_name = ' '
#     data_complete.insert(loc=0, column=column_name, value=new_column_data)
#     print(data_complete)
#     data_complete.to_csv('Thong_ke_1.txt', sep='\t', index=False)
#
#
# descriptive(data_count, column_min, column_max, column_medians, column_modes, column_q1, column_q2, column_q3,
#             column_IQR, column_variances, column_std_devs, colum_skewness, column_kurtosis)
# print(
#     '---------------------------------------------------------------------------------------------------------------------------------------------')
# # Tạo bảng thống kê (dùng hàm có sẵn)
# data_complete = df_numeric.describe(include='all')
# print(data_complete)
# data_complete.to_csv('Thong_ke_2.txt', sep='\t', index=False)
#
# # Lặp qua từng cột của DataFrame và vẽ histogram cho các cột kiểu nguyên
#
# for column in df.select_dtypes(include=['int64']):
#     plt.hist(df[column], bins=10, edgecolor='k')
#     plt.title(f'Histogram of {column}')
#     plt.xlabel(column)
#     plt.ylabel('Frequency')
#     plt.show()
#
#
# # Để vẽ biểu đồ hộp, ta cần đưa dữ liệu về dạng số
# #  Chọn các cột dữ liệu số (numeric columns)
#
# df_numeric = df.select_dtypes(include=['number'])
#
# for column in df_numeric.columns:
#     plt.figure(figsize=(6, 4))  # Kích thước của biểu đồ
#     plt.boxplot(df[column])
#     plt.title(f'Box Plot of {column}')
#     plt.ylabel(column)
#     plt.grid(True)
#     plt.show()
#
# #Vẽ nhiều cột trên một đồ thị, bằng seaborn
# plt.figure(figsize=(6, 4))  # Kích thước của biểu đồ
# sns.boxplot(x="variable", y="value", data=pd.melt(df_numeric))
# plt.show()