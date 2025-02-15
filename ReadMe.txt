This guide will help you to running Selenium Python using Pytest Framework for UI automation testing on your local machine. Follow the steps below to get started.

## Prerequisites:
Make sure you have the following installed:
- Python 3.xx (recommend using the latest version of Python 3).
- pip (Python's package installer) – should be installed along with Python.


## How To Run the Test of project (in Windows OS):
1. Extract the project folder to your local machine 

2. Open a terminal or command prompt(recommend using Administrator account)

3. Navigate to the directory where you store the project folder.
	--> E.g.: cd /d D:\Automation\extract test file\AutomationTest_MiftahRamadhan

4. Navigate to Scripts directory to Activate virtual environtment 
	--> cd /d .venv\Scripts
	--> Type "activate" or "activate.bat" and then press enter :
		D:\Automation\extract test file\AutomationTest_MiftahRamadhan\.venv\Scripts>activate(enter)

5. After activation successfully, ensure your terminal should be showing (.venv) before the prompt, indicating that the virtual environment is active.

6. Back to main project directory :D:\Automation\extract test file\AutomationTest_MiftahRamadhan

7. Install all dependencies from requirements.txt file
	--> (.venv) D:\Automation\extract test file\AutomationTest_MiftahRamadhan>pip install -r requirements.txt

8. Navigate to the \Tests directory for running the test :
	--> (.venv) D:\Automation\extract test file\AutomationTest_MiftahRamadhan>cd Tests

9. Run the Test :
	--> (.venv) D:\Automation\extract test file\AutomationTest_MiftahRamadhan\Tests> pytest -vs --browser=chrome --url=testing --html=report.html
	Note : If you want to running in some browser, just add parameters --browser again
		e.g. : pytest -vs --browser=chrome --browser=firefox --url=testing --html=report.html
		for now only 3 parameter of browser is allowed (chrome, firefox, & edge)

10. Please check the report file "report.html", and you should be open the html report file of automation test

Happy Testing!
Thank You.







