# Over the Fence

**Big ideas in mathematics, one neighbourly conversation at a time.**

An illustrated book by Guhan Purushothaman: 121 pages, seven university-level mathematical themes, and 68 custom illustrations. The source combines dialogue, everyday analogies and original programmatic SVG figures.

[Read the book (PDF)](Over-the-Fence.pdf)

## Topics

1. Fourier series
2. Vector spaces
3. Metrics
4. Eigenvalues and eigenvectors
5. Groups
6. Bayes’ theorem
7. Regression to the mean

## Source and publishing workflow

`content/` contains the chapter source. `figs*.py` and `svgkit.py` generate the illustrations. `build.py` assembles the HTML, uses headless Google Chrome to print a PDF, maps table-of-contents page markers with Ghostscript, and renders the final book.

The checked-in PDF is the existing completed book, preserved byte-for-byte. The publishing source and completed artifact are packaged together for review.

To rebuild on macOS with Python 3, Google Chrome and Ghostscript installed:

```sh
python3 build.py
```

The script currently uses the standard macOS Chrome application path. Adjust `CHROME` for another platform. Generated intermediates are excluded from Git.

## Published essays

The author’s [WordPress archive](https://guhanpurushothaman.wordpress.com/) includes earlier mathematical explainers and other essays. The website itself is hosted by WordPress; this repository contains the book’s source rather than the WordPress engine.

Copyright Guhan Purushothaman. Text and illustrations are shared for reading and portfolio review; all rights reserved.
