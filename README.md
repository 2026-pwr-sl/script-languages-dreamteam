# 🚀 Getting Started with Teamwork: Python + GitHub

## 👥 Group

**DREAM TEAM**

## 🧑‍💻 Team Members

* Piotr Rak
* German Moll
* Jakub Kuflik
* Emre Özbayrak

---

## 🎯 Project Goal

The purpose of this first assignment is to:

* Set up a **Python working environment**
* Learn the basics of **team collaboration using GitHub**
* Practice working with **branches, commits, and pull requests**
* Create a **simple Python program** in a shared team repository

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

##  📝 Project Summary
# 🛠️ Who Did What
* Jakub Kuflik: Developed the main Python program and implemented the 3 custom functions.

* German Moll: Prepared and formatted the README documentation, with assistance from Piotr Rak.

* Piotr Rak: Acted as Team Leader, handled task distribution, helped whoever needed help and conducted code reviews.

* Emre Özbayrak: Wrote the test cases in the tests/ directory to verify the behavior of the custom functions.

## ⚠️ Problems Encountered

* Environment Setup: Making sure everyone was working within the same virtual environment and had the correct Python paths configured took some            troubleshooting.

##  🧠 What We Learned

* GitHub Workflow: We learned the practical importance of using separate branches for features and tests, rather than committing directly to the main branch.

* Code Reviews: Utilizing Pull Requests allowed us to review each other's code and catch bugs before merging.

* Python Testing: We gained hands-on experience structuring a Python project with a dedicated src/ directory for code and a tests/ directory for test cases.

## Lab03 Note

For the Lab03 exercise, the functions can be grouped by how often they can be called:

* `successful_reads`, `failed_reads`, `html_entries`, and `print_html_entries` can be called multiple times because they only process the parsed list of entries.
* `read_log` should be called once per standard input stream because it consumes the input data.
* `run` is the entry point and normally runs once when the script is executed directly.
