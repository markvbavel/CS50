-- Outputs the average rating for all movies released in 2008
SELECT AVG(rating) FROM movies
JOIN ratings ON movies.id = ratings.movie_id
WHERE year = 2012;