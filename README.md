# Instructions
## Installation
*This assumes that you have Python 3.12 installed*

Clone this repository into a folder with a virtual environment already set up or follow these steps to setup an environment
1. Install virtualenv with: 'pip install virtualenv'
2. Run 'virtualenv venv' in the same folder the repository was cloned into
3. Run '.\venv\Scripts\activate' on Windows or 'source venv/bin/activate' on Linux and Mac


After activating the virtual environment, navigate into the repository directory, and run 'pip install -r requirements.txt' to install dependencies
Before running the sever, setup the database using the information provided in the Current Database Setup section of this document

## To Run the Server
*  Navigate into the delta_marketplace directory, where manage.py is located
*  Run 'python manage.py collectstatic' and type yes when prompted
*  Run 'python manage.py runserver'

## Things to note
*  Before pushing to the repository, if any new packages were installed, make sure to run 'pip freeze > requirements.txt' to update the requirements file


## Current Database Setup
The application is currently setup to use MySQL on your local machine. The create_db.py file in the top level delta_marketplace directory will create the database for you if the correct user and password are specified in the settings.py file. If your MySQL password is anything other than 'password', make sure to either change your MySQL password or change the password listed in the .env file.

After installing the package requirements with the command aboin the installation section, execute the create_db.py file to create the required database.

Then call the manage.py file with 'python manage.py migrate' to apply the database changes.

Call populate.py to add some example data to the databases. It may need to be called multiple times due to errors with foreign key restraints.