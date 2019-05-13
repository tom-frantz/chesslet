# CHESSLET
### A Wonderful SEF Project

## Setting Up The App
All of these commands should be run from the base folder (The directory this file is in)

### To install the python requirements
First, setup a python virtual env

`pip3 install virtualenv`

`virtualenv venv`

What this will do is create a virtual environment for the project. This will allow you to install python packages here that will not effect other projects.
Once you've completed that, the next step is to install the requirements to the project. To do so, run the command

`pip3 install -r requirements.txt`

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

## Diagrams

#### Use Case Diagram
https://www.lucidchart.com/invitations/accept/baba43c6-4b03-4f08-a93b-460b559f1ccd

#### Class Diagram
###### Back-End
https://www.lucidchart.com/invitations/accept/583400a4-40ec-4d8f-b4c3-3adf926b1079
###### Front-End
https://www.lucidchart.com/invitations/accept/30c3f5d6-3342-4e3e-a8ed-50e6a05fac4f

#### move_piece sequence diagram
https://www.lucidchart.com/invitations/accept/f208ebdb-788f-497f-8750-5ec8ffa15272

#### Front-End UI sequence diagram
https://www.lucidchart.com/invitations/accept/57a12b1b-26e1-4a41-8df2-a46152eb2f97

#### Front-End Board/ChessPiece object diagram
https://www.lucidchart.com/invitations/accept/86e85925-9adb-4e80-87e7-8d1044869f0f

#### Back-End Board and Piece object diagram
https://www.lucidchart.com/invitations/accept/79d0f616-b2d8-4e9d-9e15-f8abf8d94f38

#### Back-End Session object diagram
https://www.lucidchart.com/invitations/accept/0ddf00aa-c872-4b03-a9ce-324b228074c9

#### add_player sequence diagram
https://www.lucidchart.com/invitations/accept/95181f12-9020-476f-8fe2-f73da0cc75f8

#### Webserver sequence diagram
https://www.lucidchart.com/invitations/accept/b4563c9a-44ea-4d6f-b883-cb5e391ede25
