import zipfile
import re
import string
from pathlib import Path

import pandas as pd
from PIL import Image
import pytesseract

# ------------ CONFIG ------------
ZIP_PATH = "unique_tables.zip"  # path to your zip with 45 PNGs
CSV_OUT = "all_schedules_summary.csv"
TXT_OUT = "all_schedules_summary.txt"
# --------------------------------

time_pattern = re.compile(r'(\d{1,2}\s*[apAP])\s*[-–]\s*(\d{1,2}\s*[apAP])')

def to_24h_simple(t: str):
    t = t.strip().lower()
    m = re.match(r'(\d{1,2})([ap])', t)
    if not m:
        return None
    num = int(m.group(1))
    ap = m.group(2)
    if ap == 'a':
        return 0 if num == 12 else num
    else:
        return 12 if num == 12 else num + 12

def parse_image_text(img: Image.Image):
    """
    Given a schedule image, OCR it and return a list of (name, start, end) rows.
    Assumes pattern:
        <time row: "9a - 5p">
        <name row: "Firstname Lastname LEVEL THREE">
    """
    # You can downscale a bit to speed up if needed, e.g. 0.7
    # w, h = img.size
    # img = img.resize((int(w*0.7), int(h*0.7)), Image.LANCZOS)

    text = pytesseract.image_to_string(img)
    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
    rows = []

    i = 0
    while i < len(lines):
        line = lines[i]
        m = time_pattern.search(line)
        if m:
            start = m.group(1).replace(" ", "").lower()
            end = m.group(2).replace(" ", "").lower()

            # look forward for the name line
            j = i + 1
            name = ""
            while j < len(lines):
                nl = lines[j].strip()
                j += 1
                if not nl:
                    continue
                # ignore obvious headers
                if any(
                    hdr in nl
                    for hdr in ["Annotations", "Job Site", "Sandwich Line", "Default"]
                ):
                    continue
                # do not treat another time as a name
                if time_pattern.search(nl):
                    continue

                tokens = nl.split()
                cut_words = {"LEVEL", "SUP", "ORIENTATION", "SUPERVISOR", "LEAD"}
                name_tokens = []
                for tok in tokens:
                    tok_clean = tok.strip(string.punctuation)
                    if tok_clean.upper() in cut_words:
                        break
                    name_tokens.append(tok)

                # require at least one alpha character
                if name_tokens and any(c.isalpha() for c in " ".join(name_tokens)):
                    name = " ".join(name_tokens)
                    break

            if name:
                rows.append((name, start, end))
                i = j
                continue

        i += 1

    return rows

def main():
    zip_path = Path(ZIP_PATH)
    if not zip_path.exists():
        raise FileNotFoundError(f"Cannot find {zip_path}")

    all_rows = []

    with zipfile.ZipFile(zip_path, "r") as z:
        for member in sorted(z.namelist()):
            with z.open(member) as f:
                img = Image.open(f).convert("RGB")
                rows = parse_image_text(img)
                # you can keep track of which schedule each row came from if desired
                for name, start, end in rows:
                    all_rows.append((member, name, start, end))

    if not all_rows:
        raise RuntimeError("No rows extracted from any image.")

    df = pd.DataFrame(all_rows, columns=["SourceImage", "Name", "Start", "End"])

    # Convert times to 24h numeric so we can sort & compare
    df["StartH"] = df["Start"].apply(to_24h_simple)
    df["EndH"] = df["End"].apply(to_24h_simple)

    # Sort by start time then name
    df_sorted = df.sort_values(["StartH", "Name"]).reset_index(drop=True)

    # Compute counts
    closers = int((df_sorted["EndH"] == 20).sum())      # 8pm
    after2 = int((df_sorted["EndH"] > 14).sum())        # > 2pm
    after3 = int((df_sorted["EndH"] > 15).sum())        # > 3pm
    after5 = int((df_sorted["EndH"] > 17).sum())        # > 5pm

    # Save CSV with just Name/Start/End (as requested)
    df_sorted[["Name", "Start", "End"]].to_csv(CSV_OUT, index=False)

    # Save TXT with table + counts appended at the end
    with open(TXT_OUT, "w", encoding="utf-8") as f:
        f.write(df_sorted[["Name", "Start", "End"]].to_string(index=False))
        f.write("\n\n")
        f.write(f"Closers: {closers}\n")
        f.write(f"Still Here after 2pm: {after2}\n")
        f.write(f"Still Here after 3pm: {after3}\n")
        f.write(f"Still Here after 5pm: {after5}\n")

    print("Wrote:")
    print(" -", CSV_OUT)
    print(" -", TXT_OUT)
    print()
    print("Counts:")
    print(" Closers:", closers)
    print(" Still Here after 2pm:", after2)
    print(" Still Here after 3pm:", after3)
    print(" Still Here after 5pm:", after5)

if __name__ == "__main__":
    main()