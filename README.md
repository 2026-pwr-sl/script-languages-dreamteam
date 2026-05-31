# 🚀 Getting Started with Teamwork: Python + GitHub

## 👥 Group

**DREAM TEAM**

## 🧑‍💻 Team Members

- Piotr Rak
- German Moll
- Jakub Kuflik
- Emre Özbayrak

---

## 🎯 Project Goal

The purpose of this first assignment is to:

- Set up a **Python working environment**
- Learn the basics of **team collaboration using GitHub**
- Practice working with **branches, commits, and pull requests**
- Create a **simple Python program** in a shared team repository

---

## ▶️ How to Run the Program

### 1️⃣ Install Python

Download and install Python from:
https://www.python.org/downloads/

Verify installation:

```bash
python --version
```

---

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows**

```bash
venv\Scripts\activate
```

**macOS / Linux**

```bash
source venv/bin/activate
```

**Install requirements**

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Run the Program

```bash
python src/main.py
```

### 4️⃣ Run Tests

```bash
python -m pytest tests/
```

---

## 📝 Project Summary

# 🛠️ Who Did What

- Jakub Kuflik: Developed the main Python program and implemented the 3 custom functions.

- German Moll: Prepared and formatted the README documentation, with assistance from Piotr Rak.

- Piotr Rak: Acted as Team Leader, handled task distribution, helped whoever needed help and conducted code reviews.

- Emre Özbayrak: Wrote the test cases in the tests/ directory to verify the behavior of the custom functions.

## ⚠️ Problems Encountered

- Environment Setup: Making sure everyone was working within the same virtual environment and had the correct Python paths configured took some troubleshooting.

## 🧠 What We Learned

- GitHub Workflow: We learned the practical importance of using separate branches for features and tests, rather than committing directly to the main branch.

- Code Reviews: Utilizing Pull Requests allowed us to review each other's code and catch bugs before merging.

- Python Testing: We gained hands-on experience structuring a Python project with a dedicated src/ directory for code and a tests/ directory for test cases.

## Lab03 Note

For the Lab03 exercise 9, the functions can be grouped by how often they can be called:

- `successful_reads`, `failed_reads`, `html_entries`, and `print_html_entries` can be called multiple times because they only process the parsed list of entries.
- `read_log` should be called once per standard input stream because it consumes the input data.
- `run` is the entry point and normally runs once when the script is executed directly.

---

## 🏷️ Logging

For logging we're using Python built-in module - [logging](https://docs.python.org/3/library/logging.html).

To use it, it's enough to import it by using:

```python
import logging
```

## ipaddress documentation

https://docs.python.org/3/library/ipaddress.html

## datetime documentation

https://docs.python.org/3/library/datetime.html


## link to data on keggle:

https://www.kaggle.com/datasets/laveshjadon/ai-impact-on-students

---

## Lab 08 / List 10: AI Student Impact Analysis

This repository includes a CSV analysis script in `src/app8.py`.

### Dataset

Dataset URL: https://www.kaggle.com/datasets/laveshjadon/ai-impact-on-students

The dataset describes simulated student records and the relationship between
AI tool usage and academic factors such as major category, GPA, paid AI
subscription status, study hours, anxiety level, burnout risk, and skill
retention.

The local dataset file is expected at `data/ai_student_inpact.csv`, but the
script also accepts a direct path to another `.csv` file.

### Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a local `.env` file from `.env.example` if you want to change the
analysis settings:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

### Run the App

Print the summary results to the terminal:

```bash
python src/app8.py ai_student_inpact.csv
```

You can also pass the path explicitly:

```bash
python src/app8.py data/ai_student_inpact.csv
```

Show help:

```bash
python src/app8.py -h
```

### Generate the Excel Report

Create an `.xlsx` report:

```bash
python src/app8.py ai_student_inpact.csv -o report.xlsx
```

The Excel report contains a title, summary section, statistics section, and
aggregation section. It is generated with Python standard-library `zipfile`
and Office Open XML files, so no pandas or Excel writer package is required.

### Environment Variables

The script loads `.env` using `python-dotenv`.

- `STAT_COLUMN`: numeric column used for average and median calculations.
  Default: `Post_Semester_GPA`.
- `AGGREGATION_COLUMN`: column used for grouped row counts.
  Default: `Major_Category`.
- `FILTER_COLUMN`: column used for the summary filter count.
  Default: `Paid_Subscription`.
- `FILTER_VALUE`: value counted in `FILTER_COLUMN`.
  Default: `True`.
