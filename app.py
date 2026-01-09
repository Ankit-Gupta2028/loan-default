from flask import Flask, render_template, request
from model import predict_default

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    form = request.form

    user_data = {
        "Age": float(form["Age"]),
        "Income": float(form["Income"]),
        "LoanAmount": float(form["LoanAmount"]),
        "CreditScore": float(form["CreditScore"]),
        "MonthsEmployed": float(form["MonthsEmployed"]),
        "NumCreditLines": float(form["NumCreditLines"]),
        "InterestRate": float(form["InterestRate"]),
        "LoanTerm": float(form["LoanTerm"]),
        "DTIRatio": float(form["DTIRatio"]),
        "Education": form["Education"],
        "EmploymentType": form["EmploymentType"],
        "MaritalStatus": form["MaritalStatus"],
        "HasMortgage": form["HasMortgage"],
        "HasDependents": form["HasDependents"],
        "HasCoSigner": form["HasCoSigner"]
    }

    result = predict_default(user_data)

    if result == 0:
        return render_template("result.html",
                               message="✔ Loan will NOT default",
                               card_class="success")
    else:
        return render_template("result.html",
                               message="❌ Loan WILL default",
                               card_class="danger")


if __name__ == "__main__":
    app.run(debug=True)
