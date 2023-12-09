import unittest
from nokiaTask.userCommands import *
import psycopg2


class MyTestCase(unittest.TestCase):

    def test_get_all_movies(self):
        conn = psycopg2.connect(
            host="localhost",
            dbname="movies",
            user="postgres",
            password="31082013bA",
            port=5433
        )

        cur = conn.cursor()
        result = get_all_movies(cur)
        expected_result = [(2, 'Django Unchained', 'Quentin Tarantino', 2012, '02:45'),
                           (3, 'Pulp Fiction', 'Quentin Tarantino', 1994, '02:34'),
                           (1, 'Inception 1', 'Christopher Nolan', 2010, '02:28'),
                           (4, 'Inception 2', 'Christopher Nolan', 2023, '02:24')]

        self.assertEqual(result, expected_result)

    def test_get_movies_with_details(self):
        conn = psycopg2.connect(
            host="localhost",
            dbname="movies",
            user="postgres",
            password="31082013bA",
            port=5433
        )

        cur = conn.cursor()
        result = get_movies_with_details(cur, get_all_movies(cur))
        expected_result = [(2, 'Django Unchained', 'Quentin Tarantino', 2012, '02:45', 'Samuel L. Jackson at age 64'),
                           (3, 'Pulp Fiction', 'Quentin Tarantino', 1994, '02:34',
                            'Samuel L. Jackson at age 46; Uma Thurman at age 24'),
                           (1, 'Inception 1', 'Christopher Nolan', 2010, '02:28',
                            'Leonardo DiCaprio at age 36; Tom Hardy at age 33')]
        self.assertEqual(result, expected_result)

    def test_filter_movies_by_title_regex(self):
        conn = psycopg2.connect(
            host="localhost",
            dbname="movies",
            user="postgres",
            password="31082013bA",
            port=5433
        )

        cur = conn.cursor()
        result = filter_movies_by_title_regex(get_all_movies(cur), "Inception .*")
        expected_result1 = [(1, 'Inception 1', 'Christopher Nolan', 2010, '02:28'),
                            (8, 'Inception 2', 'Christopher Nolan', 2022, '02:50')]
        self.assertEqual(result, expected_result1)

    def test_filter_movies_by_director_regex(self):
        conn = psycopg2.connect(
            host="localhost",
            dbname="movies",
            user="postgres",
            password="31082013bA",
            port=5433
        )

        cur = conn.cursor()
        result = filter_movies_by_director_regex(get_all_movies(cur), "Quentin .*")
        expected_result = [(2, 'Django Unchained', 'Quentin Tarantino', 2012, '02:45'),
                           (3, 'Pulp Fiction', 'Quentin Tarantino', 1994, '02:34')]
        self.assertEqual(result, expected_result)

    def test_filter_movies_by_actor_regex(self):
        conn = psycopg2.connect(
            host="localhost",
            dbname="movies",
            user="postgres",
            password="31082013bA",
            port=5433
        )

        cur = conn.cursor()
        list = [
            (1, 'Inception 1', 'Christopher Nolan', 2010, '02:28', 'Leonardo DiCaprio at age 36; Tom Hardy at age 33'),
            (3, 'Pulp Fiction', 'Quentin Tarantino', 1994, '02:34',
             'Samuel L. Jackson at age 46; Uma Thurman at age 24')]
        result = filter_movies_by_actor_regex(list, "Tom .*")
        expected_result = [
            (1, 'Inception 1', 'Christopher Nolan', 2010, '02:28', 'Leonardo DiCaprio at age 36; Tom Hardy at age 33')]
        self.assertEqual(result, expected_result)

    def test_add_person(self):
        conn = psycopg2.connect(
            host="localhost",
            dbname="movies",
            user="postgres",
            password="31082013bA",
            port=5433
        )

        cur = conn.cursor()

        name = 'John Doe'
        birth_year = 1980
        is_director = False
        add_person(cur, name, birth_year, is_director)

        cur.execute('SELECT * FROM people WHERE name = %s', (name,))
        result = cur.fetchone()

        self.assertIsNotNone(result)
        self.assertEqual(result[1], name)
        self.assertEqual(result[2], birth_year)
        self.assertEqual(result[3], is_director)

    def test_delete_person(self):
        conn = psycopg2.connect(
            host="localhost",
            dbname="movies",
            user="postgres",
            password="31082013bA",
            port=5433
        )

        cur = conn.cursor()
        name = 'John Doe'
        cur.execute('SELECT * FROM people WHERE name = %s', (name,))
        result1 = cur.fetchone()
        self.assertEqual(result1[1], name)

        delete_person(cur, name)
        cur.execute('SELECT * FROM people WHERE name = %s', (name,))
        result2 = cur.fetchone()

        self.assertIsNotNone(result1)


if __name__ == '__main__':
    unittest.main()
