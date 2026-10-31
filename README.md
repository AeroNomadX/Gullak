# Gullak - Campus Cash Flow Management System

Gullak (Hindi for "piggy bank") is a Python-based cash flow manager for university students living on a fixed monthly allowance. It records allowance and expenses, validates every entry, calculates the balance and spending statistics, and shows everything on a web dashboard.

Built as an MCA academic project at Chandigarh University.

![Gullak dashboard](screenshots/dashboard.png)
_Add a screenshot of your dashboard at `screenshots/dashboard.png`._

---

## Features

- **Transaction management:** add, list and delete income (allowance) and expense entries, stored permanently in a JSON file.
- **Input validation:** rejects wrong types, zero or negative amounts, non-numeric amounts, unknown categories and invalid dates, with a clear error message.
- **Cash flow analytics:** balance, total income, total expense, daily average spend, spending variation (standard deviation) and a safe daily budget.
- **Category summary:** expenses grouped by Food, Books, Hostel, Entertainment, Transport and Other using Pandas.
- **Server-side chart:** category-wise expense chart rendered as a PNG with Matplotlib.
- **REST API:** Flask endpoints used by the web dashboard.
- **Web dashboard:** responsive UI built with HTML, Tailwind CSS and Chart.js, including a simulated investment hub for learning.
- **Optional desktop window:** a Tkinter quick-entry form that shares the same logic and data file.
- **Automated tests:** 17 unit and API tests using `unittest`.

## Tech Stack

| Area | Technology |
|---|---|
| Backend | Python 3, Flask |
| Data analysis | NumPy, Pandas, `array` module |
| Charts | Matplotlib (server side), Chart.js (browser) |
| Frontend | HTML, Tailwind CSS, JavaScript, Font Awesome |
| Desktop (optional) | Tkinter |
| Storage | JSON file |
| Testing | `unittest`, Flask test client |

## Project Structure

```
gullak/
├── app.py              # Flask web backend (REST API)
├── analytics.py        # Core logic: validation, storage, analytics, chart
├── desktop.py          # Optional Tkinter quick-entry window
├── test_gullak.py      # Unit and API tests
├── requirements.txt    # flask, numpy, pandas, matplotlib
├── transactions.json   # Created automatically on first run
└── static/
    └── index.html      # Web dashboard
```

## Getting Started

### Prerequisites

- Python 3.9 or later
- An internet connection when viewing the dashboard (Tailwind CSS, Chart.js and Font Awesome load from CDNs)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/<your-username>/gullak.git
cd gullak

# 2. (Recommended) create a virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt
```

### Run the web app

```bash
python app.py
```

Open http://127.0.0.1:5000 in your browser. Sample data is created automatically on the first run.

### Run the tests

```bash
python -m unittest -v
```

### Run the desktop quick-entry window (optional)

```bash
python desktop.py
```

## API Reference

| Endpoint | Method | Description |
|---|---|---|
| `/` | GET | Serves the dashboard |
| `/api/transactions` | GET | Lists all transactions, newest first |
| `/api/transactions` | POST | Adds a transaction (201 on success, 400 with an error message if invalid) |
| `/api/transactions/<id>` | DELETE | Deletes a transaction (404 if not found) |
| `/api/analytics` | GET | Returns balance, totals, daily average, variation, safe daily budget, category summary and a base64 chart |
| `/api/chart.png` | GET | Returns the category-wise expense chart as a PNG |

**Example request**

```bash
curl -X POST http://127.0.0.1:5000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{"type":"Expense","category":"Food","amount":120,"desc":"Canteen","date":"2026-10-30"}'
```

**Example analytics response** (chart field omitted)

```json
{
  "balance": 4250.0,
  "total_income": 10000.0,
  "total_expense": 5750.0,
  "daily_avg": 185.48,
  "daily_std": 182.93,
  "days_elapsed": 31,
  "days_left": 1,
  "safe_daily": 4250.0,
  "transaction_count": 15,
  "category_summary": {
    "Books": 850.0, "Entertainment": 1100.0, "Food": 1600.0,
    "Hostel": 1500.0, "Transport": 700.0
  }
}
```

The daily average and days left depend on the date the program is run.

## How the Analytics Work

| Indicator | Formula |
|---|---|
| Balance | Total income - total expense |
| Daily average | Total expense / days elapsed since the first transaction |
| Spending variation | Standard deviation of per-day expense totals (NumPy) |
| Safe daily budget | Balance / days left in the month, or 0 if the balance is not positive |
| Category summary | Expense amounts grouped by category (Pandas) |

## Known Limitations

- Single user with JSON file storage; there is no login.
- The dashboard's safe daily budget card currently uses a fixed number of days. The API already returns `safe_daily`, `days_left` and `days_elapsed` for the dashboard to display.
- `desktop.py` requires Tkinter, which is included with most Python installers.
- The investment hub is simulated and for learning only; it does not use real market data.

## Future Scope

- User accounts and login
- SQLite or MySQL database
- Monthly budgets with alerts
- UPI or bank statement import
- Live market data for the investment hub

## Documentation

The full case study report is in [`docs/Gullak_Case_Study.docx`](docs/Gullak_Case_Study.docx).

## Author

**Hritik Sharma**
MCA, Chandigarh University
GitHub: [@your-username](https://github.com/your-username)

## License

Created for educational purposes. Add a license of your choice (for example MIT) in a `LICENSE` file.
