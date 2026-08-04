# Week-5 - Data Structures

Two C programs that demonstrate data structures and memory management: a genetic inheritance simulation and a hash-table-based spell checker.

---

## Features

- **inheritance** — Simulates the inheritance of blood-type alleles across three generations using a recursive family tree.
- **speller** — Spell-checks text files using a hash-table dictionary and reports benchmark timings for loading, checking, sizing, and unloading.

---

## Requirements

- A C compiler (`gcc` or `make`).

---

## Usage

Build the programs:

```bash
gcc -o inheritance/inheritance inheritance/inheritance.c
make -C speller
```

Run the programs:

```bash
# Print a three-generation family tree with blood-type alleles
./inheritance/inheritance

# Spell-check a text file with the default dictionary
./speller/speller texts/holmes.txt

# Spell-check with a custom dictionary
./speller/speller dictionaries/small texts/holmes.txt
```

---

## Project Structure

```text
Week-5/
├── inheritance/
│   └── inheritance.c
└── speller/
    ├── speller.c
    ├── dictionary.c
    ├── dictionary.h
    ├── Makefile
    ├── texts/
    └── keys/
```

---

## License

This project is provided for educational purposes.
