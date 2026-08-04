# Week-4 - File Processing

Three C programs that read and process files: audio, images, and raw memory-card data.

---

## Features

- **volume** — Adjusts the volume of a `.wav` audio file by scaling each 16-bit sample.
- **filter-less** — Applies image filters to 24-bit BMP files: blur (`-b`), grayscale (`-g`), reflect (`-r`), and sepia (`-s`).
- **recover** — Recovers JPEG images from a raw memory-card image by scanning 512-byte blocks.

---

## Requirements

- A C compiler (`gcc` or `make`).

---

## Usage

Build the programs:

```bash
gcc -o volume/volume volume/volume.c
make -C filter-less
gcc -o recover/recover recover/recover.c
```

Run the programs:

```bash
# Adjust the volume of an audio file
./volume/volume input.wav output.wav 1.5

# Apply a grayscale filter
./filter-less/filter -g input.bmp output.bmp

# Recover JPEGs from a memory-card image
./recover/recover card.raw
```

---

## Notes

- Recovered files are named sequentially, such as `000.jpg`, `001.jpg`, and so on.

---

## License

This project is provided for educational purposes.
