# Week-7 - SQL Queries

SQL query solutions for three projects, each built around its own SQLite database.

---

## Features

- **fiftyville** — Solves a fictional theft mystery by querying crime reports, phone records, flights, and more.
- **movies** — Answers questions about movies, people, ratings, and directors.
- **songs** — Explores music attributes such as energy, valence, danceability, and tempo.

---

## Requirements

- The `sqlite3` command-line utility (installed by default on most systems, or via `sudo apt install sqlite3`).

---

## Usage

Open a database and run the queries in a `.sql` file:

```bash
cd fiftyville
sqlite3 fiftyville.db
.read log.sql
```

Repeat the same pattern for the `movies` and `songs` folders.

---

## Project Structure

```text
Week-7/
├── fiftyville/
├── movies/
└── songs/
```

---

## Notes

- Each sub-project is self-contained and requires no compilation.
- The `answers.txt` files document the expected results.

---

## License

This project is provided for educational purposes.
