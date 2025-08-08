# PA Formatter

**PA Formatter** is an internal tool originally developed for **TransPerfect** to streamline the processing of translation project data from Excel spreadsheets.  
It automates data extraction, formatting, and price calculation — generating both:

- A **cleaned and reformatted Excel** file for internal review.
- A **CSV file** ready to import into our invoicing software (**ProjectA / PA**).

---

## ✨ Features

- **Drag & Drop GUI** — No need for command-line use.
- **Automatic rush fee handling** — Applies rush fees when flagged.
- **Word count expansion** — Uses a configurable expansion rate (e.g., 25%) to estimate translated text growth.
- **Variable pricing** — Calculates costs based on Exact, Fuzzy, and New word counts.
- **Minimum job pricing** — Automatically applies minimum rates for small jobs.
- **Dual output formats** — Excel for review, CSV for invoicing software import.

---

## 📂 How it Works

1. **Input:**  
   Drag and drop a `.xlsx` file exported from our translation management system.
   
2. **Processing:**  
   - Reads and merges line items by `Sub ID`.
   - Calculates expanded word counts.
   - Determines pricing (with rush fees & minimum charges).
   - Prepares both Excel-friendly and PA-ready CSV data.

3. **Output:**  
   - `output.xlsx` — For internal record-keeping.  
   - `pa_output.csv` — Directly importable into ProjectA.

---

## 🖥️ GUI Overview

- **Drop Area:** Drag an `.xlsx` file here.
- **Folder Selection:** Choose where to save the output files.
- **Status Updates:** Real-time processing updates.

---

## ⚙️ Installation & Setup

**Requirements:**
- Python 3.10+
- [tkinter](https://docs.python.org/3/library/tkinter.html) (built-in on most systems)
- pandas
- openpyxl
- tkinterdnd2

**Install dependencies:**
```bash
pip install pandas openpyxl tkinterdnd2
