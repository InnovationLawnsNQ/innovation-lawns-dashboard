from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():

    revenue = None
    net_income = None
    annual_projection = None
    monthly_labels = []
    monthly_revenue = []
    monthly_net = []

    if request.method == "POST":

        file = request.files["file"]

        if file:
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            df = pd.read_csv(filepath)

            df["Invoice Date"] = pd.to_datetime(df["Invoice Date"])
            df["Month"] = df["Invoice Date"].dt.strftime("%b %Y")

            revenue = df["Invoice ($)"].sum()
            net_income = df["Net ($)"].sum()
            annual_projection = revenue * 12

            monthly_group = df.groupby("Month").sum(numeric_only=True).reset_index()

            monthly_labels = monthly_group["Month"].tolist()
            monthly_revenue = monthly_group["Invoice ($)"].tolist()
            monthly_net = monthly_group["Net ($)"].tolist()

    return render_template(
        "index.html",
        revenue=revenue,
        net_income=net_income,
        annual_projection=annual_projection,
        monthly_labels=monthly_labels,
        monthly_revenue=monthly_revenue,
        monthly_net=monthly_net
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
