import shlex
from config import *
from userCommands import *


def run_interface(cur):
    # Parse the user input
    command = shlex.split(input("Enter command: "))

    # Determine the main command and flags
    main_command = command[0]
    flags = [flag for flag in command[1:] if flag.startswith('-')]

    # Check for an invalid combination of flags
    if ('-la' in flags and '-ld' in flags):
        print("Invalid combination of flags.")
        return

    # Get the initial list of movies from the database
    movies = []
    # Check the main command and apply corresponding functionality
    if main_command == "l":
        movies = get_all_movies(cur)
        # Apply different filters based on flags
        if '-v' in flags:
            movies = get_movies_with_details(cur, movies)
        if '-t' in flags:
            # Extract and apply title filter using regex pattern
            regex_pattern = None
            if '-t' in command:
                index_t = command.index('-t')
                if index_t + 1 < len(command):
                    regex_pattern = command[index_t + 1]
            if regex_pattern:
                movies = filter_movies_by_title_regex(movies, regex_pattern)
            else:
                print("Bad input format, provide a regex!")
        if '-d' in flags:
            # Extract and apply director filter using regex pattern
            regex_pattern = None
            if '-d' in command:
                index_t = command.index('-d')
                if index_t + 1 < len(command):
                    regex_pattern = command[index_t + 1]
            if regex_pattern:
                movies = filter_movies_by_director_regex(movies, regex_pattern)
            else:
                print("Bad input format, provide a regex!")
        if '-a' in flags:
            # Extract and apply actor filter using regex pattern
            regex_pattern = None
            if '-a' in command:
                index_t = command.index('-a')
                if index_t + 1 < len(command):
                    regex_pattern = command[index_t + 1]
            if regex_pattern:
                # Include actors' details and filter by actor regex
                movies = filter_movies_by_actor_regex(get_movies_with_details(cur, movies), regex_pattern)
            else:
                print("Provide a regex")
        if "-la" in flags:
            # Sort movies by release date in ascending order
            movies = sorted(movies, key=lambda x: x[4])
        if "-ld" in flags:
            # Sort movies by release date in descending order
            movies = sorted(movies, key=lambda x: x[4], reverse=True)

    # Check if the main command is 'a' (add)
    elif main_command == "a":
        # Check for different flags associated with the 'a' command
        if "-p" in flags:
            add_person(cur)
        elif "-m" in flags:
            add_movie(cur)
        else:
            print("No command found")

    # Check if the main command is 'd' (delete)
    elif main_command == "d":
        # Check for the '-p' flag to delete a person
        if "-p" in flags:
            delete_person(cur)

    # Function to format movie information, optionally including actors' details
    def format_movie(movie, include_actors=True):
        movie_info = f"{movie[1]} by {movie[2]} in {movie[3]}, {movie[4]}"

        if include_actors and len(movie) > 5:
            starring_info = "\n\tStarring:"

            # Assuming the actors are stored in a separate list in the movie tuple
            actors = movie[5].split(";")

            for actor in actors:
                actor_info = f"\n\t\t-{actor.lstrip(' ')}"
                starring_info += actor_info
            return movie_info + starring_info
        else:
            return movie_info

    # Format movies with and without actors' details
    formatted_movies_with_actors = [format_movie(movie) for movie in movies]
    formatted_movies = [format_movie(movie, include_actors=False) for movie in movies]

    if len(formatted_movies_with_actors) == 0 or len(formatted_movies) == 0:
        print("Nothing was found")

    # Print formatted movie information based on user input
    if len(command) > 1:
        print("\n".join(formatted_movies_with_actors))
    elif len(command) == 1:
        print("\n".join(formatted_movies))

    print(movies)


if __name__ == "__main__":
    # Connect to the database
    conn, cur = connect_to_database()

    # Call the run_interface function and pass the cursor
    run_interface(cur)

    # Disconnect from the database
    disconnect_from_database(conn, cur)
