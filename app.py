from flask import Flask, render_template, request, send_file, redirect, url_for, session
import pickle, io, os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

app = Flask(__name__)
app.secret_key = "creditrisksecretkey"

# -------- FONT --------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
font_path = os.path.join(BASE_DIR, "ttf", "DejaVuSans.ttf")

# Only register font if the file exists (optional for PDF generation)
if os.path.exists(font_path):
    pdfmetrics.registerFont(TTFont('DejaVu', font_path))
    FONT_AVAILABLE = True
else:
    FONT_AVAILABLE = False

model = pickle.load(open("model/risk_model.pkl", "rb"))
latest_report = {}

# ---------- SAFE FLOAT ----------
def to_float(val, default=0.0):
    try:
        if val is None or str(val).strip() == "":
            return default
        return float(val)
    except:
        return default


# ---------------- HOME ----------------
@app.route("/")
def home():
    return render_template("welcome.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    # login just redirects – no blocking
    if username == "analyst" and password == "1234":
        return redirect("/input")
    else:
        return render_template("welcome.html", error="Invalid credentials")


# ---------------- INPUT PAGE ----------------
@app.route("/input")
def input_page():
    return render_template("input.html")


# ---------------- RESULT ----------------
@app.route("/result", methods=["POST"])
def result():
    # ----- FORM DATA -----
    name = request.form.get("name")
    phone = request.form.get("phone")
    employment = request.form.get("employment")
    purpose = request.form.get("loan_purpose")

    loan = to_float(request.form.get("loan"))
    debt = to_float(request.form.get("debt"))
    tenure = to_float(request.form.get("tenure"), 1)

    if employment == "student":
        income = to_float(request.form.get("parent_income"))
    else:
        income = to_float(request.form.get("income"))

    collateral_type = request.form.get("property_type","none")
    collateral_value = to_float(request.form.get("property_value"))

    # ----- RATIOS -----
    dti = debt/income if income>0 else 1
    ltv = loan/collateral_value if collateral_value>0 else 0

    # ----- MODEL -----
    features=[[income,debt,loan,collateral_value,dti]]
    risk=model.predict_proba(features)[0][1]
    decision="Approved" if risk<0.75 else "Rejected"

    # ----- INTEREST -----
    interest_map={"education":0.10,"home":0.085,"personal":0.14,"business":0.16,"medical":0.12,"luxury":0.18}
    rate=interest_map.get(purpose,0.12)

    monthly_rate=rate/12
    months=tenure*12

    emi=loan*monthly_rate*(1+monthly_rate)**months/((1+monthly_rate)**months-1) if months>0 else 0
    total_payment=emi*months
    total_interest=total_payment-loan

    monthly_income=income/12 if income>0 else 0
    monthly_capacity=monthly_income*0.40

    eligible_amount=(monthly_capacity*((1+monthly_rate)**months-1)/(monthly_rate*(1+monthly_rate)**months)) if monthly_capacity>0 else 0

    # ----- EXPLANATION -----
    if decision=="Approved":
        explanation="Your income stability and repayment capacity satisfy lending policy."
        recommendation="NA"
    else:
        explanation="Loan risk too high based on financial ratios."
        recommendation="Reduce debt or increase collateral."

    global latest_report
    latest_report={
        "Applicant Name":name,
        "Phone Number":phone,
        "Decision":decision,
        "Risk Probability":f"{round(risk*100,2)} %",
        "Eligible Loan Amount":f"₹ {round(eligible_amount,2)}",
        "Loan Purpose":purpose,
        "Interest Rate":f"{round(rate*100,2)} %",
        "Tenure":f"{tenure} years",
        "Monthly EMI":f"₹ {round(emi,2)}",
        "Monthly Capacity":f"₹ {round(monthly_capacity,2)}",
        "Total Payable":f"₹ {round(total_payment,2)}",
        "Total Interest":f"₹ {round(total_interest,2)}",
        "DTI":f"{round(dti*100,2)} %",
        "LTV":f"{round(ltv*100,2)} %",
        "Explanation":explanation,
        "Recommendation":recommendation,
        "Income":f"₹ {income}",
        "Debt":f"₹ {debt}",
        "Collateral Type":collateral_type,
        "Collateral Value":f"₹ {collateral_value}"
    }

    return render_template("result.html", **{
        "applicant_name":name,
        "phone_number":phone,
        "final_decision":decision,
        "risk_probability":round(risk*100,2),
        "eligible_loan_amount":round(eligible_amount,2),
        "loan_purpose":purpose,
        "interest_percent":round(rate*100,2),
        "repayment_tenure":tenure,
        "monthly_emi":round(emi,2),
        "monthly_capacity":round(monthly_capacity,2),
        "total_payable":round(total_payment,2),
        "interest_paid":round(total_interest,2),
        "dti_ratio":round(dti*100,2),
        "ltv_ratio":round(ltv*100,2),
        "decision_explanation":explanation,
        "recommendations":recommendation,
        "income":income,
        "debt":debt,
        "loan_requested":loan,
        "employment":employment,
        "collateral_type":collateral_type,
        "collateral_value":collateral_value
    })


# ---------------- DOWNLOAD PDF ----------------
@app.route("/download")
def download():

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()
    
    if FONT_AVAILABLE:
        styles['Normal'].fontName = 'DejaVu'
        styles['Title'].fontName = 'DejaVu'

    elements = []
    elements.append(Paragraph("AI Credit Decision Report", styles['Title']))
    elements.append(Spacer(1,20))

    table_data=[[str(k),str(v)] for k,v in latest_report.items()]
    table = Table(table_data)
    
    if FONT_AVAILABLE:
        table.setStyle([('FONTNAME',(0,0),(-1,-1),'DejaVu')])

    elements.append(table)

    doc.build(elements)
    buffer.seek(0)

    return send_file(buffer,as_attachment=True,download_name="Credit_Report.pdf",mimetype="application/pdf")

if __name__ == "__main__":
    app.run(debug=True)