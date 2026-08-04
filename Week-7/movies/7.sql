-- 7. All movies and ratings from 2010, in decreasing order by rating (alphabetical for those with same rating)
SELECT title, rating FROM movies JOIN ratings
ON movies.id = ratings.movie_id WHERE year = 2010
ORDER BY rating DESC, title;
