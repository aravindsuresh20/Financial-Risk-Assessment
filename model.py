import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load the dataset
df = pd.read_csv('financial_risk_assessment.csv')

# Select relevant columns
df = df[['Income', 'Loan Amount', 'Debt-to-Income Ratio']]

# Drop rows with missing values
df.dropna(inplace=True)

# Create the target variable 'Will Repay'
df['Will Repay'] = (df['Debt-to-Income Ratio'] < 0.4).astype(int)

# Split the data into features and target
X = df[['Income', 'Loan Amount', 'Debt-to-Income Ratio']]
y = df['Will Repay']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Classifier
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Save the trained model
with open('model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

# Save the label encoders (empty in this case since all inputs are numeric)
label_encoders = {}
with open('label_encoders.pkl', 'wb') as encoder_file:
    pickle.dump(label_encoders, encoder_file)

print("Model and label encoders have been saved successfully.")
