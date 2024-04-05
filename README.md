# Instructions
## Installation
*This assumes that you have Python 3.12 installed*

Clone this repository into a folder with a virtual environment already set up or follow these steps to setup an environment
1. Install virtualenv with: 'pip install virtualenv'
2. Run 'virtualenv venv' in the same folder the repository was cloned into
3. Run '.\venv\Scripts\activate' on Windows or 'source venv/bin/activate' on Linux and Mac


After activating the virtual environment, navigate into the repository directory, and run 'pip install -r requirements.txt' to install dependencies


## To Run the Server
*  Navigate into the delta_marketplace directory, where manage.py is located
*  Run 'python manage.py runserver'

## Things to note
*  Before pushing to the repository, if any new packages were installed, make sure to run 'pip freeze > requirements.txt' to update the requirements file
