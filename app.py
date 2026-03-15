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

        file = request.files.get("file")

        if file and file.filename != "":
            filepath = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(filepath)

            try:

                df = pd.read_csv(filepath)

                # Make sure date column exists
                if "Invoice Date" in df.columns:

                    df["Invoice Date"] = pd.to_datetime(df["Invoice Date"])
                    df["Month"] = df["Invoice Date"].dt.strftime("%b %Y")

                if "Invoice ($)" in df.columns:
                    revenue = df["Invoice ($)"].sum()

                if "Net ($)" in df.columns:
                    net_income = df["Net ($)"].sum()

                if revenue:
                    annual_projection = revenue * 12

                if "Month" in df.columns:

                    monthly_group = df.groupby("Month").sum(numeric_only=True).reset_index()

                    monthly_labels = monthly_group["Month"].tolist()

                    if "Invoice ($)" in monthly_group.columns:
                        monthly_revenue = monthly_group["Invoice ($)"].tolist()

                    if "Net ($)" in monthly_group.columns:
                        monthly_net = monthly_group["Net ($)"].tolist()

            except Exception as e:
                print("Error reading CSV:", e)

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
    app.run()
