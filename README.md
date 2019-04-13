# CHESSLET
### A Wonderful SEF Project

## Setting Up The App
All of these commands should be run from the base folder (The directory this file is in)

### To install the python requirements
First, setup a python virtual env

`pip install virtualenv`

`virtualenv venv`

What this will do is create a virtual environment for the project. This will allow you to install python packages here that will not effect other projects.
Once you've completed that, the next step is to install the requirements to the project. To do so, run the command

`pip install -r requirements.txt`

### To install the javascript requirements
This section requires Yarn. Download and install this on your machine.

To install the requirements of the project, simply run this command from the project directory

`yarn`

### To start the project 
Running scripts from the package.json is just as simple.

`yarn start` will start the project.

## Project Structure
The project consists of three parts that detail the core components in our other documents. In no particular order, these are:
1. the `chesslet` module. This will store all the game code, or the model, for the project
2. the `reactive` module. This is where the react code will sit for our front end, or our view.
3. the `webserver.py` file. This is the core of our program. This will host all communications from the model back to the user and the game.

## Important Links for Further Reading
#### Trello
https://trello.com/b/Pwdvc1zz/hey-mayne

#### Google Docs : Core Structures
https://docs.google.com/document/d/1G85eKuhSzEnAJBUcgc2ED9rLh3lWM0DfO46wqDf5czw/edit#heading=h.6lsteycwwlpo
