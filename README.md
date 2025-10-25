Bib file comprarison maker
--------------------------
Author: Nestor Espinoza (nespinoza@stsci.edu) | Last update: October 25, 2025

The `compare.py` script takes two `.bib` files (in the example, `list1.bib` and `list2.bib`), and checks which records are in one but not in the other. These are `bib` files as downloaded from ADS (`ui.adsabs.harvard.edu`). 

At the core, this script does two things:

1. Convert `bib` files to a list of strings.
2. Compare the strings by converting those lists to `sets`.

Then it prints out what elements are in one but not in the other. To use, simply run by doing `python compare.py`.

## Dependencies

The only dependency is the `bibtexparser` library. This can be easily installed via `pip install bibtexparser`.

## Acknowledgments

Some parts of this project (e.g., coding assistance) were developed with the help of [ChatGPT (OpenAI)](https://openai.com/).
