-- Outputs the 5 highest rated movies starring Chadwick Boseman

SELECT movies.title FROM movies
JOIN ratings on movies.id = ratings.movie_id
WHERE movies.id IN (SELECT stars.movie_id FROM stars
JOIN people ON stars.person_id = people.id
WHERE people.name = "Chadwick Boseman")
ORDER BY ratings.rating DESC
LIMIT 5;