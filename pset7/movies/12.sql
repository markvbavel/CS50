-- Outputs all movies where Johnny Depp and Helena Bonham Carter have starred together

SELECT movies.title FROM movies
WHERE movies.id IN (SELECT stars.movie_id FROM stars
WHERE stars.person_id IN (SELECT people.id FROM people
WHERE people.name = "Johnny Depp"))
INTERSECT
SELECT movies.title FROM movies
WHERE movies.id IN (SELECT stars.movie_id FROM stars
WHERE stars.person_id IN (SELECT people.id FROM people
WHERE people.name = "Helena Bonham Carter"));