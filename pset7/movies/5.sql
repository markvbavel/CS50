-- Outputs the title and release years of all movies starting with "Harry Potter...."
SELECT title, year
FROM movies
WHERE title LIKE "Harry Potter%"
ORDER BY year;