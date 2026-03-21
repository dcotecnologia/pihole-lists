# Script para extrair linhas que mencionam 'microsoft' de todos os arquivos em 'lists/' e salvar em 'microsoft.txt'.
import os

LISTS_DIR = "lists"
LIST_DESTINATION = "microsoft.txt"
OUTPUT_FILE = os.path.join(LISTS_DIR, LIST_DESTINATION)
KEYWORDS = ["microsoft", "bing", "windows", "edge", "azure", "office", "365", "xbox"]


def main():
    lines_found = set()
    for fname in os.listdir(LISTS_DIR):
        fpath = os.path.join(LISTS_DIR, fname)
        if not os.path.isfile(fpath):
            continue
        if fname == LIST_DESTINATION:
            continue
        with open(fpath, encoding="utf-8", errors="ignore") as f:
            for line in f:
                if any(keyword in line.lower() for keyword in KEYWORDS):
                    lines_found.add(line.rstrip())
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for line in sorted(lines_found):
            out.write(line + "\n")
    print(f"{len(lines_found)} lines containing '{', '.join(KEYWORDS)}' were saved in {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
