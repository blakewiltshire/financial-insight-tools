# modules/acronyms.py
ACRONYMS = {
    "gdp": "GDP",
    "us": "US",
    "Ism": "ISM",
    "Pmi": "PMI",
    # Add more acronyms as needed
}

def format_title(s):
    words = s.replace('_', ' ').split()
    formatted_words = [ACRONYMS.get(word.lower(), word.title()) for word in words]
    return ' '.join(formatted_words)
