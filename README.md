

# 🔎 Excel Search Engine (Flask Web App)

A simple web app to search Excel spreadsheets using Python and Flask.

---

## ⚙️ Requirements

- Python 3.10+
- Git

---
### 🧭 How to Open Bash / Terminal

- **Windows**: Press `Windows + R`, type `cmd` or `powershell`, and press Enter.  
  You can also install **Git Bash** (comes with Git) and right-click → **Git Bash Here**.

- **macOS**: Open **Spotlight** (`Cmd + Space`), type `Terminal`, and press Enter.

- **Linux**: Press `Ctrl + Alt + T` or find “Terminal” in your applications.
- 
## 🧑‍💻 Setup (Step-by-Step)

### 1. Clone the Repository
```bash
git clone https://github.com/Richtsnoer/excel-searchengine.git
cd excel-searchengine
```

### 2. Create & Activate Virtual Environment (optional but recommended)
```bash
python -m venv venv
```

- On **Windows**:
```bash
venv\Scripts\activate
```

- On **macOS/Linux**:
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
Make sure the bottom of your `app.py` contains this:
```python
if __name__ == "__main__":
    app.run(debug=True, port=8080)
```

Then run it:
```bash
python app.py
```

### 5. Open the Web App
In your browser, go to:
```
http://localhost:8080
```



