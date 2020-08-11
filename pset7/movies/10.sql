-- Outputs a list of directers to have directed a movie rated 9.0 or higher

SELECT people.name FROM people
WHERE people.id IN (SELECT directors.person_id FROM directors
JOIN movies ON directors.movie_id = movies.id
JOIN ratings ON movies.id = ratings.movie_id
WHERE ratings.rating >= 9.0);