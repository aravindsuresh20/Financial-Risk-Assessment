from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load model and encoders
model = pickle.load(open('model.pkl', 'rb'))
label_encoders = pickle.load(open('label_encoders.pkl', 'rb'))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get user input
        income = float(request.form['income'])
        loan_amount = float(request.form['loan_amount'])
        dti_ratio = float(request.form['dti_ratio'])

        # Match feature names used during training
        input_df = pd.DataFrame([{
            'Income': income,
            'Loan Amount': loan_amount,
            'Debt-to-Income Ratio': dti_ratio
        }])

        # Predict
        prediction = model.predict(input_df)[0]
        result = "✅ Yes, likely to repay the loan." if prediction == 1 else "❌ No, unlikely to repay the loan."

        return render_template('results.html', prediction=result)

    except Exception as e:
        return render_template('results.html', prediction=f"Prediction failed: {str(e)}")

def save_eda():
    try:
        df = pd.read_csv('financial_risk_assessment.csv')

        eda_results = []

        summary_stats = df.describe(include='all')
        eda_results.append("Summary Statistics:\n")
        eda_results.append(summary_stats.to_string())
        eda_results.append("\n\n")

        missing_values = df.isnull().sum()
        eda_results.append("Missing Values:\n")
        eda_results.append(missing_values.to_string())
        eda_results.append("\n\n")

        eda_results.append("Basic Insights:\n")
        eda_results.append(f"Total number of rows: {df.shape[0]}")
        eda_results.append(f"\nTotal number of columns: {df.shape[1]}")
        eda_results.append(f"\nColumns with missing values: {missing_values[missing_values > 0].index.tolist()}")
        eda_results.append(f"\nColumns with no missing values: {missing_values[missing_values == 0].index.tolist()}")
        eda_results.append("\n\n")

        with open('eda_results.txt', 'w') as f:
            f.write("\n".join(eda_results))

    except Exception as e:
        print(f"EDA failed: {str(e)}")

if __name__ == '__main__':
    save_eda()  # Automatically save EDA when app starts
    app.run(debug=True)
