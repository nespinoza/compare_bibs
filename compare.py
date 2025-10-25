import bibtexparser
from bibtexparser.bparser import BibTexParser
from bibtexparser.customization import convert_to_unicode
import re

# For this to work, go here: https://ui.adsabs.harvard.edu/public-libraries/JAL40dT5ToGup2Omjvc3Ag
# Download or copy-paste text on BibTex to my_publications.bib

# Mapping LaTeX-style journal codes to full names
JOURNAL_NAME_MAP = {
    r'\aap': 'Astronomy & Astrophysics',
    r'\apj': 'Astrophysical Journal',
    r'\apjl': 'Astrophysical Journal Letters',
    r'\apjs': 'Astrophysical Journal Supplement Series',
    r'\mnras': 'Monthly Notices of the Royal Astronomical Society',
    r'\aj': 'Astronomical Journal',
    r'\nat': 'Nature',
    r'\araa': 'Annual Review of Astronomy and Astrophysics',
    r'\pasp': 'Publications of the Astronomical Society of the Pacific',
    r'\icarus': 'Icarus',
    r'\ssr': 'Space Science Reviews'
}
def clean_latex_commands(text):
    """Replace LaTeX-style journal codes and remove braces."""
    text = text.strip()
    text = re.sub(r'\\[a-zA-Z]+', lambda m: JOURNAL_NAME_MAP.get(m.group(0), m.group(0)), text)
    text = re.sub(r'[{}]', '', text)
    return text
def format_authors(author_field, max_authors=3):
    authors = [a.strip() for a in author_field.replace('\n', ' ').split(' and ')]
    if len(authors) > max_authors:
        return ', '.join(authors[:max_authors]) + ', et al.'
    return ', '.join(authors)
def parse_bibtex(file_path):
    with open(file_path, 'r') as bibtex_file:
        parser = BibTexParser()
        parser.customization = convert_to_unicode
        bib_database = bibtexparser.load(bibtex_file, parser=parser)
    publications = []
    for entry in bib_database.entries:
        authors = format_authors(entry.get('author', ''))
        title = clean_latex_commands(entry.get('title', 'No title'))
        journal_raw = entry.get('journal') or entry.get('booktitle') or 'No venue listed'
        journal = clean_latex_commands(journal_raw)
        volume = entry.get('volume', '')
        number = entry.get('number', '')
        pages = entry.get('pages', '')
        year = entry.get('year', 'n.d.')
        year_int = int(year) if year.isdigit() else 0
        # Build volume/issue/page string
        citation_details = []
        if volume:
            citation_details.append(f"vol. {volume}")
        if number:
            citation_details.append(f"no. {number}")
        if pages:
            citation_details.append(f"pp. {pages}")
        citation_str = ', '.join(citation_details)
        if citation_str:
            citation_str = f", {citation_str}"
        formatted_entry = {
            'year': year_int,
            'text': f"{authors}: \"\\textit{{{title}}}.\" \\textit{{{journal}}}, {year}{citation_str}"
        }
        publications.append(formatted_entry)
    # Sort in reverse chronological order
    publications.sort(key=lambda x: x['year'], reverse=True)
    return [pub['text'] for pub in publications]

if __name__ == "__main__":

    bib_file1 = "list1.bib"  
    bib_file2 = "list2.bib"
    publications1 = parse_bibtex(bib_file1)
    publications2 = parse_bibtex(bib_file2)

    # Convert to sets
    set1, set2 = set(publications1), set(publications2)

    # Find elements not in common
    diff1 = set1 - set2   # items in publications1 but not in publications2
    diff2 = set2 - set1   # items in publications2 but not in publications1

    # Union of differences = symmetric difference
    not_in_common = diff1 | diff2   # or: set1.symmetric_difference(set2)

    print('\n----------------------------------------------------------------\n')
    print('\n----------------------------------------------------------------\n')
    print("\nA total of "+str(len(diff1))+" publications in ",bib_file1, 'but not in ',bib_file2,':')
    count = 1
    for pub in diff1:

        print("\n "+str(count)+'. ',pub)
        count += 1

    print('\n----------------------------------------------------------------\n')
    print('\n----------------------------------------------------------------\n')
    print("\nA total of "+str(len(diff2))+" publications in ",bib_file2, 'but not in ',bib_file1,':')
    count = 1
    for pub in diff2:

        print("\n "+str(count)+'. ',pub)
        count +=1

    print('\n')
