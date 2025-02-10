# Import Librariesimport pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import pickle
import pandas as pd

# Load dataset
data = pd.read_csv("data/programprediction.csv")

# Preprocess the data
X = data[['Land Size', 'Gender', 'Ownership Type', 'Organization Membership']]
y = data['Recommended Programs']

# One-hot encode categorical variables
categorical_features = ['Gender', 'Ownership Type', 'Organization Membership']
preprocessor = ColumnTransformer(
    transformers=[('cat', OneHotEncoder(), categorical_features)], remainder='passthrough')

# Create logistic regression pipeline
pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                            ('classifier', LogisticRegression(multi_class='multinomial', max_iter=1000))])

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
pipeline.fit(X_train, y_train)

# Evaluate the model
y_pred = pipeline.predict(X_test)
print(classification_report(y_test, y_pred))

# Save the model
with open("program_recommender_model.pkl", "wb") as model_file:
    pickle.dump(pipeline, model_file)
# python logistic_regression.py