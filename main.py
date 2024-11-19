from factcheck.config import en_afp_url, fr_afp_url, ar_afp_url
from factcheck.scrape_afp import scrape_afp

en_afp = scrape_afp(56, en_afp_url, "en_factcheck.txt")
print(en_afp)
print(len(en_afp))

fr_afp = scrape_afp(34, fr_afp_url, "fr_factcheck.txt")
print(fr_afp)
print(len(fr_afp))

ar_afp = scrape_afp(50, ar_afp_url, "ar_factcheck.txt")
print(ar_afp)
print(len(ar_afp))
