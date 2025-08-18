import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Path to the saved model and its components
MODEL_PATH = 'artifacts/model_data.joblib'

# Load the model and its components
model_data = joblib.load(MODEL_PATH)
model = model_data['model']
scaler = model_data['scaler']
features = model_data['features']
cols_to_scale = model_data['cols_to_scale']


def prepare_input(age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
                    delinquency_ratio, credit_utilization_ratio, num_open_accounts, residence_type,
                    loan_purpose, loan_type):
    # Create a dictionary with input values and dummy values for missing features
    input_data = {
        'age': age,
        'loan_tenure_months': loan_tenure_months,
        'number_of_open_accounts': num_open_accounts,
        'credit_utilization_ratio': credit_utilization_ratio,
        'loan_to_income': loan_amount / income if income > 0 else 0,
        'delinquency_ratio': delinquency_ratio,
        'avg_dpd_per_delinquency': avg_dpd_per_delinquency,
        'residence_type_Owned': 1 if residence_type == 'Owned' else 0,
        'residence_type_Rented': 1 if residence_type == 'Rented' else 0,
        'loan_purpose_Education': 1 if loan_purpose == 'Education' else 0,
        'loan_purpose_Home': 1 if loan_purpose == 'Home' else 0,
        'loan_purpose_Personal': 1 if loan_purpose == 'Personal' else 0,
        'loan_type_Unsecured': 1 if loan_type == 'Unsecured' else 0,
        # additional dummy fields just for scaling purpose
        'number_of_dependants': 1,  # Dummy value
        'years_at_current_address': 1,  # Dummy value
        'zipcode': 1,  # Dummy value
        'sanction_amount': 1,  # Dummy value
        'processing_fee': 1,  # Dummy value
        'gst': 1,  # Dummy value
        'net_disbursement': 1,  # Computed dummy value
        'principal_outstanding': 1,  # Dummy value
        'bank_balance_at_application': 1,  # Dummy value
        'number_of_closed_accounts': 1,  # Dummy value
        'enquiry_count': 1  # Dummy value
    }

    # Ensure all columns for features and cols_to_scale are present
    df = pd.DataFrame([input_data])

    # Ensure only required columns for scaling are scaled
    df[cols_to_scale] = scaler.transform(df[cols_to_scale])

    # Ensure the DataFrame contains only the features expected by the model
    df = df[features]

    return df


def predict(age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
            delinquency_ratio, credit_utilization_ratio, num_open_accounts,
            residence_type, loan_purpose, loan_type):
    # Prepare input data
    input_df = prepare_input(age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
                             delinquency_ratio, credit_utilization_ratio, num_open_accounts, residence_type,
                             loan_purpose, loan_type)

    probability, credit_score, rating = calculate_credit_score(input_df)

    return probability, credit_score, rating


def calculate_credit_score(input_df, base_score=300, scale_length=600):
    x = np.dot(input_df.values, model.coef_.T) + model.intercept_

    # Apply the logistic function to calculate the probability
    default_probability = 1 / (1 + np.exp(-x))

    non_default_probability = 1 - default_probability

    # Convert the probability to a credit score, scaled to fit within 300 to 900
    credit_score = base_score + non_default_probability.flatten() * scale_length

    # Determine the rating category based on the credit score
    def get_rating(score):
        if 300 <= score < 500:
            return 'Poor'
        elif 500 <= score < 650:
            return 'Average'
        elif 650 <= score < 750:
            return 'Good'
        elif 750 <= score <= 900:
            return 'Excellent'
        else:
            return 'Undefined'  # in case of any unexpected score

    rating = get_rating(credit_score[0])

    return default_probability.flatten()[0], int(credit_score[0]), rating


# Explainability utilities
def get_feature_contributions(input_df: pd.DataFrame) -> pd.DataFrame:
    """Return per-feature linear contributions: value * coefficient.
    Output columns: feature, value, coefficient, contribution.
    """
    coefs = model.coef_.flatten()
    vals = input_df.iloc[0].values.flatten()
    contribs = vals * coefs
    df = pd.DataFrame({
        'feature': features,
        'value': vals,
        'coefficient': coefs,
        'contribution': contribs
    })
    df = df.sort_values('contribution', ascending=False).reset_index(drop=True)
    return df


def explain_from_inputs(age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
                        delinquency_ratio, credit_utilization_ratio, num_open_accounts,
                        residence_type, loan_purpose, loan_type):
    """Return prediction plus feature contribution breakdown."""
    input_df = prepare_input(age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
                             delinquency_ratio, credit_utilization_ratio, num_open_accounts, residence_type,
                             loan_purpose, loan_type)
    probability, credit_score, rating = calculate_credit_score(input_df)
    contrib_df = get_feature_contributions(input_df)
    return probability, credit_score, rating, contrib_df


def predict_batch(raw_df: pd.DataFrame) -> pd.DataFrame:
    """Batch scoring for a DataFrame with columns matching the app's raw inputs:
    [age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
     delinquency_ratio, credit_utilization_ratio, num_open_accounts,
     residence_type, loan_purpose, loan_type]

    Returns a DataFrame with the original inputs plus: default_probability, credit_score, rating, loan_to_income.
    """
    outputs = []
    for _, row in raw_df.iterrows():
        age = int(row.get('age', 0))
        income = float(row.get('income', 0))
        loan_amount = float(row.get('loan_amount', 0))
        loan_tenure_months = int(row.get('loan_tenure_months', 0))
        avg_dpd_per_delinquency = float(row.get('avg_dpd_per_delinquency', 0))
        delinquency_ratio = float(row.get('delinquency_ratio', 0))
        credit_utilization_ratio = float(row.get('credit_utilization_ratio', 0))
        num_open_accounts = int(row.get('num_open_accounts', 0))
        residence_type = row.get('residence_type', 'Owned')
        loan_purpose = row.get('loan_purpose', 'Personal')
        loan_type = row.get('loan_type', 'Unsecured')

        inp = prepare_input(age, income, loan_amount, loan_tenure_months, avg_dpd_per_delinquency,
                            delinquency_ratio, credit_utilization_ratio, num_open_accounts, residence_type,
                            loan_purpose, loan_type)
        prob, score, rating = calculate_credit_score(inp)
        outputs.append({
            'age': age,
            'income': income,
            'loan_amount': loan_amount,
            'loan_tenure_months': loan_tenure_months,
            'avg_dpd_per_delinquency': avg_dpd_per_delinquency,
            'delinquency_ratio': delinquency_ratio,
            'credit_utilization_ratio': credit_utilization_ratio,
            'num_open_accounts': num_open_accounts,
            'residence_type': residence_type,
            'loan_purpose': loan_purpose,
            'loan_type': loan_type,
            'loan_to_income': (loan_amount / income) if income else 0,
            'default_probability': float(prob),
            'credit_score': int(score),
            'rating': rating,
        })
    return pd.DataFrame(outputs)


def batch_template() -> pd.DataFrame:
    """Return a template DataFrame for batch CSV input."""
    return pd.DataFrame([{
        'age': 28,
        'income': 1200000,
        'loan_amount': 900000,
        'loan_tenure_months': 36,
        'avg_dpd_per_delinquency': 20,
        'delinquency_ratio': 30,
        'credit_utilization_ratio': 30,
        'num_open_accounts': 2,
        'residence_type': 'Owned',
        'loan_purpose': 'Personal',
        'loan_type': 'Unsecured',
    }])