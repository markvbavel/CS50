-- Outputs a list of all titles and ratings for movies released in 2010. Excluding ones that don't have a rating.
SELECT title, rating FROM movies
JOIN ratings
ON movies.id = ratings.movie_id
WHERE year = 2010 AND rating != "\\N"
ORDER BY rating DESC, title ASC;