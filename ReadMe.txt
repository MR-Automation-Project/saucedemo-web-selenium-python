This guide will help you to running Selenium Python using Pytest Framework for UI automation testing on your local machine.
Follow the steps below to get started.

## Prerequisites:
Make sure you have the following installed:
- Python 3.xx (recommend using the latest version of Python 3).
- pip (Python's package installer) – should be installed along with Python.


## How To Run the Test of project (in Windows OS):
1. Clone this repository to your local machine

2. Open a terminal or command prompt(recommend using Administrator account)

3. Navigate to the directory where you clone the repository.
	--> E.g.: cd /d D:\Automation\saucedemo-web-selenium-python

4. Navigate to Scripts directory to Activate virtual environtment 
	--> cd /d .venv\Scripts
	--> Type "activate" or "activate.bat" and then press enter :
		D:\Automation\saucedemo-web-selenium-python\.venv\Scripts>activate(enter)

5. After activation successfully, ensure your terminal should be showing (.venv) before the prompt, indicating that the virtual environment is active.

6. Back to main project directory :D:\Automation\saucedemo-web-selenium-python

7. Install all dependencies from requirements.txt file
	--> (.venv) D:\Automation\saucedemo-web-selenium-python>pip install -r requirements.txt

8. Navigate to the \Tests directory for running the test :
	--> (.venv) D:\Automation\saucedemo-web-selenium-python>cd Tests

9. Run the Test :
	--> (.venv) D:\Automation\saucedemo-web-selenium-python\Tests> pytest -vs --browser=chrome --url=testing --html=report.html
	Note : If you want to running in some browser* , just add the parameters --browser again
		e.g. : pytest -vs --browser=chrome --browser=firefox --url=testing --html=report.html
		*for now only 3 parameter of browser is allowed (chrome, firefox, & edge)
		*if you want to running in safari browser, you must execute on mac os (just put the parameter --browser=safari)

10. Please check the report file "report.html", and you should be open the html report file of automation test

Happy Testing!
Thank You.







