import sys
import io
import base64
from datetime import datetime
from flask import Flask, jsonify, request, render_template_string

# ------------------------------------------------------------------
# SYLLABUS LIBRARIES IMPORT
# ------------------------------------------------------------------
import array  # Standard Python Array Module
import numpy as np  # NumPy Matrix & Statistical Vector Library
import pandas as pd  # Pandas DataFrame & Grouping Engine

# Matplotlib setup for headless backend rendering
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Tkinter Desktop GUI integration (optional launch)
try:
    import tkinter as tk
    from tkinter import messagebox

    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

app = Flask(__name__)

# ------------------------------------------------------------------
# IN-MEMORY DATABASE (STUDENT TRANSACTIONS)
# ------------------------------------------------------------------
TRANSACTIONS = [
    {
        "id": 1,
        "date": "2026-10-27",
        "type": "Expense",
        "category": "Food",
        "desc": "Hostel Canteen Dinner & Shake",
        "amount": 180.00,
    },
    {
        "id": 2,
        "date": "2026-10-26",
        "type": "Expense",
        "category": "Books",
        "desc": "Python Data Science Textbook Photocopy",
        "amount": 350.00,
    },
    {
        "id": 3,
        "date": "2026-10-25",
        "type": "Expense",
        "category": "Transport",
        "desc": "Auto rickshaw to Campus Gate",
        "amount": 60.00,
    },
    {
        "id": 4,
        "date": "2026-10-24",
        "type": "Expense",
        "category": "Entertainment",
        "desc": "Weekend Movie Ticket with Friends",
        "amount": 280.00,
    },
    {
        "id": 5,
        "date": "2026-10-22",
        "type": "Expense",
        "category": "Hostel",
        "desc": "Electricity Bill & Wifi Share",
        "amount": 450.00,
    },
    {
        "id": 6,
        "date": "2026-10-20",
        "type": "Expense",
        "category": "Food",
        "desc": "Swiggy Snack order late night",
        "amount": 240.00,
    },
    {
        "id": 7,
        "date": "2026-10-15",
        "type": "Income",
        "category": "Income",
        "desc": "Monthly Allowance from Home",
        "amount": 10000.00,
    },
]


# ------------------------------------------------------------------
# SYLLABUS COMPUTATION FUNCTIONS (NUMPY, ARRAYS, PANDAS, MATPLOTLIB)
# ------------------------------------------------------------------
def compute_analytics_with_python():
    """Demonstrates syllabus concepts:

    1. Python Standard Array & NumPy vector operations
    2. Pandas DataFrame aggregation & category grouping
    3. Matplotlib dynamic chart image generation (Base64)
    """
    if not TRANSACTIONS:
        return {
            "balance": 0.0,
            "total_income": 0.0,
            "total_expense": 0.0,
            "daily_avg": 0.0,
            "category_summary": {},
            "matplotlib_chart_b64": "",
        }

    # 1. PANDAS DATAFRAME INTEGRATION
    df = pd.DataFrame(TRANSACTIONS)

    # Separate Incomes & Expenses using Pandas indexing
    expenses_df = df[df["type"] == "Expense"]
    incomes_df = df[df["type"] == "Income"]

    # Calculate Totals with Pandas
    total_income = (
        float(incomes_df["amount"].sum()) if not incomes_df.empty else 0.0
    )
    total_expense = (
        float(expenses_df["amount"].sum()) if not expenses_df.empty else 0.0
    )
    current_balance = total_income - total_expense

    # 2. PYTHON ARRAY & NUMPY COMPUTATION
    # Convert amounts into Python's native double array ('d' typecode)
    expense_amounts_list = (
        expenses_df["amount"].tolist() if not expenses_df.empty else [0.0]
    )
    py_arr = array.array("d", expense_amounts_list)

    # Convert native Python array directly to a NumPy vector
    np_vector = np.array(py_arr, dtype=np.float64)

    # Statistical array processing via NumPy
    mean_daily_spend = float(np.mean(np_vector)) if len(np_vector) > 0 else 0.0
    std_spend = float(np.std(np_vector)) if len(np_vector) > 0 else 0.0

    # 3. PANDAS CATEGORY GROUPING
    category_summary = {}
    if not expenses_df.empty:
        cat_grouped = expenses_df.groupby("category")["amount"].sum()
        category_summary = cat_grouped.to_dict()

    # 4. MATPLOTLIB CHART GENERATION
    img_b64 = ""
    try:
        fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
        fig.patch.set_facecolor("#FFFFFF")

        if not expenses_df.empty:
            cat_names = list(category_summary.keys())
            cat_values = list(category_summary.values())
            colors = ["#FFB800", "#3B82F6", "#8B5CF6", "#EC4899", "#10B981"]

            ax.bar(
                cat_names,
                cat_values,
                color=colors[: len(cat_names)],
                width=0.5,
                edgecolor="#0F172A",
                linewidth=0.8,
            )
            ax.set_title(
                "Expenditure Breakdown (Matplotlib Engine)",
                fontsize=10,
                fontweight="bold",
                color="#0F172A",
            )
            ax.set_ylabel("Spent (₹)", fontsize=9, color="#475569")
            ax.grid(axis="y", linestyle="--", alpha=0.5)
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            plt.tight_layout()

        # Save plot to buffer as PNG and encode as Base64 for web display
        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        img_b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
        plt.close(fig)
    except Exception as e:
        print(f"Matplotlib generation error: {e}")

    return {
        "balance": current_balance,
        "total_income": total_income,
        "total_expense": total_expense,
        "daily_avg": round(mean_daily_spend, 2),
        "std_dev": round(std_spend, 2),
        "category_summary": category_summary,
        "chart_b64": img_b64,
    }


# ------------------------------------------------------------------
# FLASK API ENDPOINTS
# ------------------------------------------------------------------
@app.route("/")
def index():
    """Renders the HTML web application."""
    with open("index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return render_template_string(html_content)


@app.route("/api/analytics", methods=["GET"])
def get_analytics():
    """Returns analytics computed via NumPy, Pandas, and Matplotlib."""
    analytics = compute_analytics_with_python()
    return jsonify(analytics)


@app.route("/api/transactions", methods=["GET", "POST"])
def manage_transactions():
    global TRANSACTIONS
    if request.method == "POST":
        data = request.json
        new_entry = {
            "id": int(datetime.now().timestamp() * 1000),
            "date": data.get(
                "date", datetime.now().strftime("%Y-%m-%d")
            ),
            "type": data.get("type", "Expense"),
            "category": data.get("category", "Other"),
            "desc": data.get("desc", ""),
            "amount": float(data.get("amount", 0.0)),
        }
        TRANSACTIONS.insert(0, new_entry)
        return jsonify(
            {
                "status": "success",
                "entry": new_entry,
                "analytics": compute_analytics_with_python(),
            }
        )

    return jsonify(TRANSACTIONS)


@app.route("/api/transactions/<int:trans_id>", methods=["DELETE"])
def delete_transaction(trans_id):
    global TRANSACTIONS
    TRANSACTIONS = [t for t in TRANSACTIONS if t["id"] != trans_id]
    return jsonify(
        {
            "status": "deleted",
            "analytics": compute_analytics_with_python(),
        }
    )


# ------------------------------------------------------------------
# TKINTER DESKTOP GUI COMPONENT (SYLLABUS REQUIREMENT)
# ------------------------------------------------------------------
def launch_tkinter_desktop_app():
    """Optional Tkinter Desktop Logger utility running alongside web server."""
    if not TKINTER_AVAILABLE:
        print(
            "Tkinter not supported in headless mode. Web interface remains active."
        )
        return

    root = tk.Tk()
    root.title("Gullak Student Desktop Assistant")
    root.geometry("380x320")
    root.configure(bg="#0F172A")

    title_label = tk.Label(
        root,
        text="Gullak Quick Expense Logger",
        font=("Arial", 12, "bold"),
        fg="#FFB800",
        bg="#0F172A",
    )
    title_label.pack(pady=12)

    lbl_desc = tk.Label(
        root,
        text="Expense Description:",
        font=("Arial", 9),
        fg="#FFFFFF",
        bg="#0F172A",
    )
    lbl_desc.pack(anchor="w", padx=30)
    entry_desc = tk.Entry(root, width=30)
    entry_desc.pack(pady=4)

    lbl_amt = tk.Label(
        root,
        text="Amount (₹):",
        font=("Arial", 9),
        fg="#FFFFFF",
        bg="#0F172A",
    )
    lbl_amt.pack(anchor="w", padx=30)
    entry_amt = tk.Entry(root, width=30)
    entry_amt.pack(pady=4)

    def submit_tk():
        desc = entry_desc.get()
        amt_str = entry_amt.get()
        if desc and amt_str:
            try:
                amt = float(amt_str)
                TRANSACTIONS.insert(
                    0,
                    {
                        "id": int(datetime.now().timestamp() * 1000),
                        "date": datetime.now().strftime("%Y-%m-%d"),
                        "type": "Expense",
                        "category": "Other",
                        "desc": desc,
                        "amount": amt,
                    },
                )
                messagebox.showinfo(
                    "Success",
                    f"Added ₹{amt} ({desc}) to Gullak Database!",
                )
                entry_desc.delete(0, tk.END)
                entry_amt.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Enter a valid number")

    btn = tk.Button(
        root,
        text="Log to Gullak Database",
        command=submit_tk,
        bg="#FFB800",
        fg="#0F172A",
        font=("Arial", 10, "bold"),
    )
    btn.pack(pady=15)

    root.mainloop()


# ------------------------------------------------------------------
# APPLICATION ENTRYPOINT
# ------------------------------------------------------------------
if __name__ == "__main__":
    print("=========================================================")
    print("  GULLAK STUDENT FINANCE WEB & PYTHON ANALYTICS SERVER   ")
    print("=========================================================")
    print("  ✓ NumPy, Arrays, Pandas, Matplotlib Engine Ready")
    print("  ✓ Server starting on: http://127.0.0.1:5000")
    print("=========================================================")

    # Run Flask application
    app.run(debug=True, port=5000)