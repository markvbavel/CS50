
-- Outputs a list of people to have starred alonside "Kevin Bacon", born in 1958, excluding "Kevin Bacon"
SELECT people.name FROM people
WHERE people.name != "Kevin Bacon"
AND people.id IN (SELECT stars.person_id FROM stars
WHERE stars.movie_id IN (SELECT movies.id FROM movies
WHERE movies.id IN (SELECT stars.movie_id FROM stars
WHERE stars.person_id IN (SELECT people.id FROM people
WHERE (people.name = "Kevin Bacon" AND people.birth = 1958)))))
ORDER BY people.name ASC;