# 🏦 Credit Risk Engine

A Personal Credit Risk Scoring Engine built with Python, Machine Learning, and Flask.

---

## 📌 Overview

The Credit Risk Engine is a web-based application that predicts the credit risk of an individual based on their financial and personal data. It uses a trained Machine Learning model to classify whether a person is a **high** or **low** credit risk, helping in smarter lending decisions.

---

## 🚀 Features

- 🔍 Predicts credit risk based on user input
- 🤖 Machine Learning model trained on real credit data
- 🌐 Clean and interactive web interface built with Flask
- 📊 Instant risk scoring results
- 📁 Organized project structure with modular code

---

## 🛠️ Tech Stack

| Technology | Usage |
|------------|-------|
| Python | Core programming language |
| Flask | Web framework |
| Scikit-learn | Machine Learning model |
| Pandas | Data processing |
| HTML/CSS | Frontend templates |

---

## 📂 Project Structure

```
Credit-Risk-Engine/
├── model/
│   ├── credit_data.csv       # Dataset used for training
│   ├── risk_model.pkl        # Trained ML model
│   ├── train_model.py        # Model training script
│   └── test_model.py         # Model testing script
├── templates/
│   ├── welcome.html          # Landing page
│   ├── input.html            # User input form
│   └── result.html           # Risk result display
├── ttf/                      # Font files
├── .gitignore
├── app.py                    # Main Flask application
└── requirements.txt          # Project dependencies
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/rishi8639/Credit-Risk-Engine.git
cd Credit-Risk-Engine
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # On Windows
source venv/bin/activate   # On Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python app.py
```

### 5. Open in browser
```
http://127.0.0.1:5000
```

---

## 🎯 How It Works

1. User visits the welcome page
2. Fills in their financial details in the input form
3. The Flask app passes the data to the trained ML model
4. The model predicts the credit risk score
5. The result is displayed on the result page

---

## 📸 Screenshots

> _Add screenshots of your app here_

---

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Rishi Kumar Reddy**  
GitHub: [@rishi8639](https://github.com/rishi8639)
