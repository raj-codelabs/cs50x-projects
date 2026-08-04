# Week-3 - Voting Simulations

Two election-simulation programs in C, plus sample data files for sorting exercises.

---

## Features

- `plurality/` — Implements plurality voting. Each voter casts a single vote; the candidate with the most votes wins (ties are allowed).
- `runoff/` — Implements instant-runoff voting. Voters rank candidates; if no candidate wins a majority, the lowest-ranked candidate is eliminated and votes are redistributed until a winner emerges.
- `sort/` — Contains numeric data files in random, reversed, and sorted orders for testing sorting algorithms.

---

## Requirements

- A C compiler with the CS50 library, or `gcc`.

---

## Usage

Build and run each program from its own folder:

```bash
cd plurality
make
./plurality Alice Bob Charlie
```

---

## Project Structure

```text
Week-3/
├── plurality/
├── runoff/
└── sort/
```

---

## Notes

- Election programs read voter input from the command line.
- See the `sort/` README for details on the sorting data files.

---

## License

This project is provided for educational purposes.
