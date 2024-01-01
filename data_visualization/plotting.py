import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = '/home/nmh/ds/project/data_validation/cleaned_concatenated_data.csv'
df = pd.read_csv(file_path)

# Set the style for seaborn plots
sns.set(style="whitegrid")

# Plot 1: Histogram of Prices
plt.figure(figsize=(10, 6))
sns.histplot(df['price'], bins=30, kde=True)
plt.title('Distribution of Property Prices')
plt.xlabel('Price (in Millions)')
plt.ylabel('Frequency')
plt.show()

# Plot 2: Boxplot of Areas by District
plt.figure(figsize=(14, 8))
sns.boxplot(x='district', y='area', data=df)
plt.xticks(rotation=45)
plt.title('Property Area Distribution by District')
plt.xlabel('District')
plt.ylabel('Area (in Square Meters)')
plt.show()

# Plot 3: Scatter Plot of Price vs. Area
plt.figure(figsize=(10, 6))
sns.scatterplot(x='area', y='price', data=df, hue='district', alpha=0.6)
plt.title('Property Price vs. Area by District')
plt.xlabel('Area (in Square Meters)')
plt.ylabel('Price (in Millions)')
plt.legend(title='District', bbox_to_anchor=(1.05, 1), loc=2)
plt.show()

# Plot 4: Countplot of Bedrooms
plt.figure(figsize=(10, 6))
sns.countplot(x='bedroom', data=df)
plt.title('Number of Bedrooms in Properties')
plt.xlabel('Number of Bedrooms')
plt.ylabel('Count')
plt.show()

# Plot 5: Correlation Heatmap
plt.figure(figsize=(12, 8))
correlation_matrix = df.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.show()
