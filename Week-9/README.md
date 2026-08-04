# Week-9 - Flask Web Applications

Two Flask-based web applications: a birthday tracker and a stock-trading simulator.

---

## Features

- **Birthdays** — Stores and displays birthdays using a form and a SQLite database, with validation for month and day.
- **Finance** — Simulates stock trading with user registration, real-time quote lookup, buying and selling shares, and transaction history.

---

## Requirements

- Python 3.
- Packages listed in `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## Usage

From the respective application folder, run:

```bash
flask run
```

Then open the URL printed by Flask in a browser.

---

## Project Structure

```text
Week-9/
├── Birthdays/
│   ├── appy.py
│   ├── templates/
│   └── static/
└── Finance/
    ├── app.py
    ├── helpers.py
    ├── requirements.txt
    ├── templates/
    └── static/
```

---

## Notes

- The Finance app uses an external API for real-time stock quotes.
- The Birthdays app uses cache-control headers to always show the latest data.

---

## License

This project is provided for educational purposes.
