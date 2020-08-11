-- Outputs all people to have starred in a movie in 2004, no duplicates

SELECT people.name FROM people
WHERE people.id IN (SELECT people.id FROM people
JOIN stars ON people.id = stars.person_id
JOIN movies ON movies.id = stars.movie_id
WHERE movies.year = 2004)
ORDER BY people.birth;