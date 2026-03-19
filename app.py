from flask import Flask, render_template, request, redirect
import pandas as pd

app = Flask(__name__)

# Temporary storage (we can upgrade to database later)
clients = []

@app.route("/", methods=["GET", "POST"])
def index():
    global clients

    revenue = None
    net_income = None
    annual_projection = None

    # ===== HANDLE CSV UPLOAD =====
    if request.method == "POST":

        # Upload Hnry CSV
        if "hnry_file" in request.files:
            file = request.files["hnry_file"]

            if file and file.filename != "":
                df = pd.read_csv(file)

                revenue = df.select_dtypes(include='number').sum().sum()
                annual_projection = revenue * 12

        # Upload client list CSV
        if "client_file" in request.files:
            file = request.files["client_file"]

            if file and file.filename != "":
                df = pd.read_csv(file)

                # Convert CSV to list of dicts
                clients = df.fillna("").to_dict(orient="records")

        # Add manual client
        if "name" in request.form:
            new_client = {
                "Name": request.form.get("name"),
                "Phone": request.form.get("phone"),
                "Address": request.form.get("address"),
                "Service": request.form.get("service"),
                "Frequency": request.form.get("frequency"),
                "Price": request.form.get("price")
            }

            clients.append(new_client)

        return redirect("/")

    return render_template(
        "index.html",
        revenue=revenue,
        net_income=net_income,
        annual_projection=annual_projection,
        clients=clients
    )

if __name__ == "__main__":
    app.run()
