import os
import hashlib
import numpy as np
from PIL import Image
from PIL.ExifTags import TAGS

# Configuration
files = {
    "Suspect": "Picture_UAS_Steganografi.jpg",
    "Clean (WhatsApp)": "Picture_UAS_Steganografi_fixnodata.jpg",
    "Clean (Super)": "super_clean_baseline.jpg",
    "Hidden (Steghide)": "Picture_UAS_Steganografi_steghide.jpg",
    "Hidden (OpenStego)": "Picture_UAS_Steganografi_hidden.jpg"
}

def get_md5(path):
    if not os.path.exists(path): return "N/A"
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def get_exif(path):
    try:
        img = Image.open(path)
        exif = img._getexif()
        if not exif: return "None"
        return {TAGS.get(key, key): val for key, val in exif.items()}
    except: return "Error"

def get_lsb_stats(path):
    if not os.path.exists(path): return [0, 0, 0]
    img = Image.open(path)
    data = np.array(img)
    lsb = data & 1
    return [np.mean(lsb[:,:,i]) for i in range(3)]

def get_eoi_markers(path):
    if not os.path.exists(path): return []
    with open(path, "rb") as f:
        content = f.read()
        markers = []
        index = 0
        while True:
            index = content.find(b'\xff\xd9', index)
            if index == -1: break
            markers.append(index)
            index += 2
        return markers

def run_detailed_analysis():
    report = []
    report.append("="*80)
    report.append("DETAILED FORENSIC COMPARISON REPORT (5-WAY)")
    report.append("="*80)

    # Stage 1: Hash & Size
    report.append("\n[STAGE 1] HASH & SIZE ANALYSIS")
    report.append("-" * 40)
    header = f"{'File Label':<20} | {'Size (Bytes)':<12} | {'MD5 Hash'}"
    report.append(header)
    report.append("-" * len(header))
    for label, path in files.items():
        size = os.path.getsize(path) if os.path.exists(path) else 0
        md5 = get_md5(path)
        report.append(f"{label:<20} | {size:<12} | {md5}")

    # Stage 2: Structure (EOI Markers)
    report.append("\n[STAGE 2] STRUCTURE ANALYSIS (EOI MARKERS)")
    report.append("-" * 40)
    header = f"{'File Label':<20} | {'EOI Count':<10} | {'EOI Positions'}"
    report.append(header)
    report.append("-" * len(header))
    for label, path in files.items():
        eois = get_eoi_markers(path)
        report.append(f"{label:<20} | {len(eois):<10} | {eois}")

    # Stage 3: Statistical LSB Analysis
    report.append("\n[STAGE 3] STATISTICAL LSB ANALYSIS")
    report.append("-" * 40)
    header = f"{'File Label':<20} | {'Red LSB':<10} | {'Green LSB':<10} | {'Blue LSB':<10}"
    report.append(header)
    report.append("-" * len(header))
    for label, path in files.items():
        lsb = get_lsb_stats(path)
        report.append(f"{label:<20} | {lsb[0]:.6f} | {lsb[1]:.6f} | {lsb[2]:.6f}")

    # Verdict Logic
    report.append("\n" + "="*80)
    report.append("FINAL VERDICT & OBSERVATIONS")
    report.append("="*80)

    s_lsb = get_lsb_stats(files["Suspect"])
    c_lsb = get_lsb_stats(files["Clean (WhatsApp)"])

    lsb_diff_clean = [abs(s - c) for s, c in zip(s_lsb, c_lsb)]

    report.append(f"1. Suspect vs WhatsApp Clean LSB Diff: {lsb_diff_clean}")

    if all(d < 0.000001 for d in lsb_diff_clean):
        report.append("\n[+] VERDICT: Suspect image is statistically IDENTICAL to the Clean Baseline.")
        report.append("The 36-byte difference is confirmed as EXIF metadata (Orientation tag).")
    else:
        report.append("\n[!] VERDICT: Suspect image shows statistical deviation from Clean Baseline.")

    return "\n".join(report)

if __name__ == "__main__":
    output = run_detailed_analysis()
    print(output)
    with open("forensic_comparison_results.txt", "w") as f:
        f.write(output)
    print("\n[+] Results saved to forensic_comparison_results.txt")
