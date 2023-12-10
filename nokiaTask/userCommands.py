import re
from datetime import datetime
import sys


# Function to get all movies from the database
def get_all_movies(cur):
    cur.execute('''
        SELECT
            m.movie_id,
            m.title,
            p_director.name AS director_name,
            m.release_year,
            TO_CHAR(m.length_minutes / 60, 'FM00') || ':' || TO_CHAR(m.length_minutes % 60, 'FM00') AS formatted_length
        FROM
            Movies m
        JOIN
            People p_director ON m.director_id = p_director.person_id
    ''')

    movie_list = cur.fetchall()
    sorted_movie_list = sorted(movie_list, key=lambda movie: movie[1])

    # Returns a list of all movies in the database
    return sorted_movie_list


# Function to get movies with starring actors
def get_movies_with_details(cur, movie_list):
    result_list = []

    for movie in movie_list:
        movie_id, title, director, release_year, length = movie

        query = '''
        SELECT 
    m.movie_id,
    m.title,
    d.name AS director_name,
    m.release_year,
    m.length_minutes,
    STRING_AGG(
        a.name || ' at age ' || (m.release_year - a.birth_year)::text, '; '
    ) AS actors_info
FROM 
    Movies m
JOIN 
    People d ON m.director_id = d.person_id
JOIN 
    MoviePeople mp ON m.movie_id = mp.movie_id
JOIN 
    People a ON mp.person_id = a.person_id AND a.is_actor = TRUE
WHERE 
    m.movie_id = %s
GROUP BY 
    m.movie_id, m.title, d.name, m.release_year, m.length_minutes;
        '''

        cur.execute(query, (movie_id,))
        movie_info = cur.fetchall()

        for mi in movie_info:
            _, _, director_name, _, _, actors_info = mi
            result_list.append((movie_id, title, director, release_year, length, actors_info))
    return result_list


# Function to filter list of movies by title using regex
def filter_movies_by_title_regex(movies_list, title_regex):
    try:
        re.compile(title_regex)
    except re.error:
        print("Invalid regex. Please enter a valid regex.")
        sys.exit(1)
    return [movie for movie in movies_list if re.match(title_regex, movie[1])]


# Function to filter list of movies by director name using regex
def filter_movies_by_director_regex(movies_list, director_regex):
    try:
        re.compile(director_regex)
    except re.error:
        print("Invalid regex. Please enter a valid regex.")
        sys.exit(1)

    return [movie for movie in movies_list if re.match(director_regex, movie[2])]


# Function to filter list of movies by actor name using regex
def filter_movies_by_actor_regex(movies_list, actor_regex):
    res = []

    try:
        re.compile(actor_regex)
    except re.error:
        print("Invalid regex. Please enter a valid regex.")
        sys.exit(1)

    for movie in movies_list:
        pattern = r"([a-zA-Z. ]+)(?= at age)"
        names = re.findall(pattern, movie[5])
        for name in names:
            if re.match(actor_regex, name.lstrip(' ')):
                res.append(movie)
    return res


# Function to add a person to the database
def add_person(cur, name, birth_year, is_director, is_actor):
    try:
        cur.execute(
            'INSERT INTO people (name, birth_year, is_director, is_actor) VALUES (%s, %s, %s, %s) RETURNING person_id',
            (name, birth_year, is_director, is_actor))
        new_person_id = cur.fetchone()[0]
        print(f"Person '{name}' was added successfully.")

        # Commit the changes to the database
        cur.connection.commit()
    except ValueError:
        print("Invalid input. Please enter a valid year of birth.")


# Function to validate time format (hh:mm)
def validate_time_format(time_str):
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False


# Function to add a movie to the database
def add_movie(cur):
    try:
        print("Adding a new movie:")

        # Get movie details from the user
        title = input("Title: ")
        while True:
            length = input("Length (hh:mm): ")
            if validate_time_format(length):
                break
            else:
                print("> Bad input format (hh:mm), try again!")

        # Get the director's name
        while True:
            director_name = input("Director: ")
            cur.execute('SELECT person_id FROM People WHERE name = %s', (director_name,))
            director_result = cur.fetchone()
            if director_result:
                director_id = director_result[0]
                break
            else:
                print(f'>"{director_name}" is not in the database, try again!')

        # Get the release year
        release_year = int(input("Released in: "))

        # Get the list of actors
        actors = []
        while True:
            actor_name = input("Starring (type 'exit' to finish): ")
            if actor_name.lower() == 'exit':
                break
            cur.execute('SELECT person_id FROM People WHERE name = %s AND is_actor = true', (actor_name,))
            actor_result = cur.fetchone()
            if actor_result:
                actor_id = actor_result[0]
                actors.append(actor_id)
            else:
                print(f'> We could not find actor "{actor_name}", try again!')

        # Convert hh:mm format to hours and minutes
        hours, minutes = map(int, length.split(':'))
        total_minutes = hours * 60 + minutes
        # Insert the movie into the database
        cur.execute(
            'INSERT INTO Movies (title, director_id, release_year, length_minutes) VALUES (%s, %s, %s, %s) RETURNING movie_id',
            (title, director_id, release_year, total_minutes)
        )
        new_movie_id = cur.fetchone()[0]

        # Insert the relationships between the movie and its actors
        for actor_id in actors:
            cur.execute('INSERT INTO MoviePeople (movie_id, person_id) VALUES (%s, %s)', (new_movie_id, actor_id))

        print(f"Movie '{title}' with ID {new_movie_id} added successfully.")
        cur.connection.commit()

    except ValueError:
        print("Invalid input. Please enter valid values.")
        cur.connection.rollback()


# Function to delete a person from the database
def delete_person(cur, name_to_delete):
    try:
        # Check if the person exists in the database
        cur.execute('SELECT person_id, is_director FROM People WHERE name = %s', (name_to_delete,))
        person_result = cur.fetchone()

        if person_result:
            person_id, is_director = person_result

            # Check if the person is a director
            if is_director:
                print(f'Cannot delete "{name_to_delete}" as they are a director in a movie.')
                return

            # Delete the person from movies they starred in
            cur.execute('DELETE FROM MoviePeople WHERE person_id = %s', (person_id,))

            # Delete the person from the People table
            cur.execute('DELETE FROM People WHERE person_id = %s', (person_id,))

            print(f'Person "{name_to_delete}" deleted successfully.')
            cur.connection.commit()

        else:
            print(f'Person "{name_to_delete}" not found in the database.')

    except Exception as e:
        print(f"An error occurred: {e}")
        cur.connection.rollback()
