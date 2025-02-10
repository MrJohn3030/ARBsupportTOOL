# Import Libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv("arb_data.csv")

# Preprocess Data
data['Organization Member'] = data['Organization Member'].map({'Yes': 1, 'No': 0})
data['Ownership Type'] = data['Ownership Type'].map({'Individual': 0, 'Collective': 1, 'Co-Ownership': 2})
data['Gender'] = data['Gender'].map({'Male': 0, 'Female': 1})

def categorize_land_size(size):
    if size <= 1:
        return 0  # Small
    elif 1 < size <= 5:
        return 1  # Medium
    else:
        return 2  # Large

data['Land Size Category'] = data['Land Size'].apply(categorize_land_size)

# Define features and target
X = data[['Land Size Category', 'Organization Member', 'Ownership Type', 'Gender']]
y = data['Program Outcome']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the Logistic Regression Model
model = LogisticRegression()
model.fit(X_train, y_train)

# Save the Model
joblib.dump(model, "logistic_regression_model.pkl")

# Evaluate the Model
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)
print("Classification Report:")
print(classification_report(y_test, y_pred))

# Visualize Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_pred)
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues')
plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.show()
