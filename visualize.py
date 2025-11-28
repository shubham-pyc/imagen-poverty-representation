import pandas as pd
import matplotlib.pyplot as plt

# Load the data
df = pd.read_csv("south_asian_images.csv")

# Calculate the value counts
counts = df["label"].value_counts()
labels = counts.index
values = counts.values

# Calculate the total size of the dataset
total_size = len(df)

# Create the pie chart
plt.figure(figsize=(8, 6)) # Optional: Adjust the figure size
plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)

# Ensure the plot is a perfect circle
plt.axis('equal')

# Add a title with the total size included
plt.title(f"Is Image South Asian (Total Images: {total_size})")

# Display the plot
plt.show()
