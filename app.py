from flask import Flask, render_template, request, redirect
import pandas as pd
import sqlite3

app = Flask(__name__)

# ===== DATABASE SETUP =====
import os

def get_db():
    db_path = os.path.join("/tmp", "clients.db")  # safer location on Render
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            address TEXT,
            service TEXT,
            frequency TEXT,
            price REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ===== MAIN ROUTE =====
@app.route("/", methods=["GET", "POST"])
def index():

    conn = get_db()

    if request.method == "POST":

        # Upload client CSV
        if "client_file" in request.files:
            file = request.files["client_file"]

            if file and file.filename != "":
                df = pd.read_csv(file)

                for _, row in df.iterrows():
                    conn.execute("""
                        INSERT INTO clients (name, phone, address, service, frequency, price)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        row.get("Name"),
                        row.get("Phone"),
                        row.get("Address"),
                        row.get("Service"),
                        row.get("Frequency"),
                        row.get("Price")
                    ))

                conn.commit()

        # Add manual client
        if "name" in request.form:
            conn.execute("""
                INSERT INTO clients (name, phone, address, service, frequency, price)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                request.form.get("name"),
                request.form.get("phone"),
                request.form.get("address"),
                request.form.get("service"),
                request.form.get("frequency"),
                request.form.get("price")
            ))

            conn.commit()

        return redirect("/")

    # Fetch clients
    clients = conn.execute("SELECT * FROM clients").fetchall()
    conn.close()

    return render_template("index.html", clients=clients)


# ===== DELETE CLIENT =====
@app.route("/delete/<int:id>")
def delete_client(id):
    conn = get_db()
    conn.execute("DELETE FROM clients WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run()
