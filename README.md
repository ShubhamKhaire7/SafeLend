# SafeLend 🛡️ — Advanced Credit Risk Assessment Platform

A modern, professional Streamlit application for comprehensive credit risk modeling with state-of-the-art UI/UX design and machine learning capabilities.

![SafeLend Banner](https://img.shields.io/badge/SafeLend-v1.0-blue?style=for-the-badge&logo=shield&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red?style=flat&logo=streamlit)
![ML](https://img.shields.io/badge/ML-Scikit--Learn-orange?style=flat&logo=scikit-learn)

## ✨ Key Features

### 🎨 Modern UI/UX Design
- **Professional Interface** with gradient backgrounds and modern card layouts
- **Responsive Design** optimized for desktop and mobile viewing
- **Interactive Components** with hover effects and smooth transitions
- **Color-Coded Risk Indicators** for intuitive risk assessment
- **Enhanced Typography** with proper visual hierarchy

### 🧠 Machine Learning Capabilities
- **Advanced Risk Modeling** using trained ML algorithms
- **Real-time Predictions** with instant risk assessment
- **Feature Importance Analysis** with explainable AI insights
- **Batch Processing** for multiple applicant scoring
- **Model Validation** with comprehensive error handling

### 📊 Comprehensive Analytics
- **Risk Probability Calculation** with visual progress indicators
- **Credit Score Generation** on standard 300-900 scale
- **Rating Classification** (Poor/Average/Good/Excellent)
- **Affordability Analysis** with DTI and EMI calculations
- **Comparative Analysis** across different risk profiles

### 🔧 Advanced Functionality
- **Quick Presets** for rapid testing (Low/Average/High Risk)
- **Export Capabilities** (JSON reports, CSV batch results, TXT summaries)
- **Interactive Explanations** with feature contribution analysis
- **Professional Documentation** with comprehensive help sections

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (for cloning)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd SafeLend
```

2. **Create virtual environment** (recommended)
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
streamlit run main.py
```

5. **Access the app**
   - Open your browser and navigate to `http://localhost:8501`
   - The app will automatically reload when you make changes

## 📁 Project Structure

```
SafeLend/
├── artifacts/
│   └── model_data.joblib           # Trained ML model + preprocessing components
├── .streamlit/
│   └── config.toml                 # Streamlit theme configuration
├── main.py                         # Main Streamlit application
├── prediction_helper.py            # ML pipeline and prediction logic
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
├── LICENSE                         # License file
└── .gitignore                      # Git ignore rules
```

## 📊 Model Information

### Input Features

#### 👤 Personal Information
- **Age**: Applicant's age in years (18-100)
- **Annual Income**: Total yearly income in INR
- **Residence Type**: Owned, Rented, or Mortgage

#### 🏦 Loan Details
- **Loan Amount**: Requested loan amount in INR
- **Loan Tenure**: Repayment period in months
- **Loan Purpose**: Education, Home, Auto, or Personal
- **Loan Type**: Secured or Unsecured

#### 💳 Credit Profile
- **Average DPD**: Average days past due per delinquency
- **Delinquency Ratio**: Percentage of late payments (0-100%)
- **Credit Utilization**: Percentage of available credit used (0-100%)
- **Open Accounts**: Number of active loan accounts (1-10)

#### 📈 Derived Metrics
- **Loan-to-Income Ratio**: Automatically calculated (Loan Amount / Annual Income)

### Model Outputs

#### 🎯 Primary Predictions
- **Default Probability**: Risk of loan default (0-100%)
- **Credit Score**: Standard credit score (300-900 scale)
- **Credit Rating**: Categorical rating (Poor/Average/Good/Excellent)

#### 📊 Risk Classification
- **Low Risk**: < 20% default probability (✅ Green)
- **Medium Risk**: 20-40% default probability (⚠️ Orange) 
- **High Risk**: > 40% default probability (🚨 Red)

## 🧠 Machine Learning Pipeline

### Model Architecture
- **Algorithm**: Trained machine learning model (loaded from joblib)
- **Preprocessing**: MinMaxScaler for numerical features
- **Feature Engineering**: One-hot encoding for categorical variables
- **Validation**: Comprehensive input validation and error handling

### Data Processing Pipeline
1. **Input Validation**: Ensures all inputs are within valid ranges
2. **Feature Preparation**: Creates model-compatible feature vector
3. **Scaling**: Applies trained scaler to numerical features
4. **Prediction**: Generates default probability using trained model
5. **Score Derivation**: Converts probability to credit score (300-900)
6. **Rating Assignment**: Maps score to categorical rating

### Model Components (artifacts/model_data.joblib)
- **Trained Model**: Core ML algorithm for risk prediction
- **Scaler**: MinMaxScaler fitted on training data
- **Feature List**: Complete list of model features
- **Scaling Columns**: Columns that require normalization

### Credit Score Calculation
```python
# Simplified scoring logic
default_prob = model.predict_proba(scaled_features)[0][1]
credit_score = 300 + (1 - default_prob) * 600
rating = assign_rating(credit_score)
```

### 🎨 Theming

The app ships with a light, minimal theme via `.streamlit/config.toml`. You can switch to dark mode from Streamlit’s settings if desired.

## 🎨 UI/UX Design

### Design System
- **Color Palette**: Professional gradients with primary colors (#667eea to #764ba2)
- **Typography**: Modern font hierarchy with proper spacing
- **Components**: Card-based layout with subtle shadows and hover effects
- **Responsive**: Mobile-friendly design with adaptive layouts

### Theme Configuration
The app uses a custom light theme defined in `.streamlit/config.toml`:
```toml
[theme]
base = "light"
primaryColor = "#667eea"
backgroundColor = "#fafbfc"
secondaryBackgroundColor = "#f8fafc"
textColor = "#1e293b"
font = "sans serif"
```

### Visual Elements
- **Gradient Headers**: Eye-catching section headers with gradients
- **Interactive Cards**: Hover effects and smooth transitions
- **Progress Indicators**: Visual risk assessment with color coding
- **Professional Footer**: Branded footer with proper disclaimers

## 🛠 Troubleshooting

### Common Issues

#### Model Loading Errors
- **Issue**: `FileNotFoundError` for model artifact
- **Solution**: Ensure `artifacts/model_data.joblib` exists in the project directory

#### Dependency Conflicts
- **Issue**: Package version conflicts during installation
- **Solution**: 
  ```bash
  python -m pip install --upgrade pip
  pip install -r requirements.txt --force-reinstall
  ```

#### Performance Issues
- **Issue**: Slow installation on Apple Silicon or older systems
- **Solution**: Pre-compiled wheels for `scikit-learn`/`numpy` may take longer to install

#### Streamlit Issues
- **Issue**: App not loading or displaying incorrectly
- **Solution**: Clear Streamlit cache with `streamlit cache clear`

### Development Tips
- Use `streamlit run main.py --server.runOnSave true` for auto-reload
- Enable developer mode in browser for debugging CSS issues
- Check browser console for JavaScript errors if UI components malfunction

## 📈 Usage Examples

### Basic Risk Assessment
1. Select a preset profile (Low/Average/High Risk) or enter custom values
2. Fill in applicant information across all sections
3. Click "Calculate Risk" to generate assessment
4. Review results in the comprehensive dashboard

### Batch Processing
1. Navigate to "Batch Scoring" tab
2. Upload CSV file with applicant data
3. Download processed results with risk scores

### Affordability Analysis
1. Go to "Affordability" tab
2. Enter income, target DTI, and loan terms
3. View maximum affordable loan amount

## 🔒 Security & Privacy
- **Local Processing**: All data processing happens locally
- **No Data Storage**: No applicant data is stored or transmitted
- **Session-Based**: Data cleared when browser session ends

## ⚖️ Legal Disclaimer

**Important**: This application is for demonstration and educational purposes only. It does not constitute financial advice, and should not be used for actual lending decisions. Always consult with qualified financial professionals for real-world credit assessments.

## 👤 Author & Contact

**Built by Shubham Khaire**

- 📧 Email: shubhamkhaire00@gmail.com
- 💼 LinkedIn: www.linkedin.com/in/shubham-khaire07
- 🐙 GitHub: https://github.com/ShubhamKhaire7

### 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to:
- Open an issue for bug reports
- Submit pull requests for improvements
- Suggest new features or enhancements

### 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**SafeLend © 2025** - Advanced Credit Risk Assessment Platform


