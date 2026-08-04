# Week-2 - Arrays and Cryptography

A set of C programs that focus on string manipulation and cryptographic techniques.

---

## Features

- `caesar.c` — Encrypts text using Caesar's cipher with a user-provided rotation key, preserving case.
- `readability.c` — Computes the Coleman-Liau reading index of a text and classifies it by grade level.
- `scrabble.c` — Computes the Scrabble score of a word using standard letter values.
- `substitution.c` — Encrypts text using a substitution cipher based on a validated 26-character key.

---

## Requirements

- A C compiler with the CS50 library, or `gcc`.

---

## Usage

Compile each program with `make` and run the resulting executable:

```bash
make caesar
./caesar 13
```

---

## How It Works

- Caesar's cipher shifts each alphabetic character by the provided key.
- Substitution maps each letter to a letter from the supplied 26-character key.
- The readability program counts letters, words, and sentences to calculate the Coleman-Liau index.

---

## License

This project is provided for educational purposes.
