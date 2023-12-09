This project is a simple Movie Database Management System implemented in Python using PostgreSQL as the database. 
The system allows users to interact with the database by adding and deleting movies, directors, and actors.
Additionally, users can retrieve information about movies, directors, and actors based on various filters.

Prerequisites
Before running the project, ensure that you have the following installed:

Python 3.8
PostgreSQL 15

Setup
Clone the repository to your local machine.

git clone https://github.com/torogeldiiev/nokiaTask.git

cd nokiaTask

Install the required Python packages.
pip install -r requirements.txt

Set up the PostgreSQL database.
Create a new database named movies.

Restore my database from dump.sql file using cmd
pg_restore -U user_name -h host -d database_name < dump.sql

Update the PostgreSQL connection details in the config.py file. Change port from 5433 to port that you use and same with host, user, dbname and password 

Running the Application
Open a terminal and navigate to the project directory.

Run the main script.

python main.py
Follow the on-screen instructions to interact with the Movie Database Management System.

Commands

List Movies: "l" and then you can provide specific flags like: 
"-v" - lists movies with detailed actor information 
"-t" - lists movies where title match with the regex. Regex should be given after the flag in quotes 
"-d" - lists movies where director name match with the regex. Regex should be given after the flag in quotes
"-a" - lists movies where actor name match with the regex. Regex should be given after the flag in quotes
"-la" - sorts list of movies with ascending order by their length
"-ld" - sorts list of movies with descending order by their length

Make changes in movie or people: "a" and then provide specific flags like: 
"-p" - adding new people to the database 
"-m" - adding new movie to the database
Delete Person: "d -p"

Example Commands:
List all movies: l 
List movies with detailed actor information: l -v
List movies with mathcing the regex: l -t "Inception .*"
List movies with matching regex : l -d "Christopher Nolan .*"
Lists movies where actor name match with the regex: l -a "Tom Hardy"
List sorted movies by their length: "l -la"

You can combine different flags into one command
Example Command:
l -t "Inception .*" -v : will print list of movies where title of the movie starts with "Inception" and also will print it detailed informaion with actors
l -v -la  : will print sorted list of movies in ascending order with it detailed information with actors
l -v -ld  : will print sorted list of movies in descending order with it detailed information with actors
Feel free to combine this flags in different ways as you like , but combination of flags should be logically correct 
