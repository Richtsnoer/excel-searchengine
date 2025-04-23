1. Clone the Repository from GitHub
You need to clone the repository (which contains your app code) onto the new computer.

Install Git (if it's not installed) on the new computer from Git.

Open the terminal (Command Prompt for Windows, or Terminal for macOS/Linux).

Clone the repository:

Navigate to the directory where you want to store your project (use cd command to change the directory).

Clone the project from GitHub by running:

bash
git clone https://github.com/your-username/excel-search-engine.git
Replace your-username/excel-search-engine with the actual GitHub repository link.

Change into the project directory:

bash
cd excel-search-engine

2. Set Up Python Virtual Environment
Create a virtual environment to isolate the Python dependencies:

For Windows:

bash
python -m venv venv
venv\Scripts\activate
For macOS/Linux:

bash
python3 -m venv venv
source venv/bin/activate
Activate the virtual environment:

For Windows, run:

bash
venv\Scripts\activate
For macOS/Linux, run:

bash
source venv/bin/activate
You should see (venv) in your terminal, indicating that you're now working inside the virtual environment.

3. Install Dependencies
Once your virtual environment is active, you'll need to install the required dependencies listed in the requirements.txt file.

Install the required Python libraries:

bash
pip install -r requirements.txt
This will install all the dependencies that your Flask app requires (e.g., Flask, Pandas, openpyxl, etc.).

4. Set Up Directories and Files
Ensure that the uploads and rdl_files directories exist to store uploaded files and .rdl files. If they don't exist, create them:

Create necessary directories:

bash
mkdir uploads rdl_files
5. Run the Application
Now that everything is set up, you're ready to run the Flask app.

Run the Flask app:

bash
python app.py
This will start the Flask server, and you should see something like:

bash
* Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)
This indicates that the Flask app is running locally on your computer at port 8080.

6. Access the Application
On the same machine (where the Flask app is running), open a web browser and go to:

bash
http://127.0.0.1:8080
On another machine (in the same network), replace 127.0.0.1 with the IP address of the machine running the Flask app. For example:

bash
http://192.168.x.x:8080
To get the IP address of the machine running Flask:

Windows: Open Command Prompt and run ipconfig, look for your IPv4 address.

macOS/Linux: Run ifconfig (or ip a on newer Linux systems) to find the IP address.
