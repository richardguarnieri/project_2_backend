/* validate number of records */ 
SELECT COUNT(*) FROM imdb_movies; /* 85,855 records */

SELECT COUNT(*) FROM imdb_ratings; /* 85,855 records */

SELECT COUNT(*) FROM imdb_movies_b; /* 81,273 records */


/* validate number of records missing in both universes */ 
/* missing 5,431*/
SELECT COUNT(*) 
FROM imdb_movies
WHERE imdb_title_id NOT IN (SELECT imdb_title_id
						    FROM imdb_movies_b)
;

/* missing 849*/
SELECT COUNT(*) 
FROM imdb_movies_b
WHERE imdb_title_id NOT IN (SELECT imdb_title_id
						    FROM imdb_movies)
;

/* matches 80,424 */
SELECT COUNT(*)
FROM imdb_movies
WHERE imdb_title_id IN (SELECT imdb_title_id
						 FROM imdb_movies_b)
;


/* Union of all the records for main universe */
CREATE TABLE imdb_movies_global_b
AS
(SELECT * 
 FROM imdb_movies
 WHERE imdb_title_id IN (SELECT imdb_title_id 
						 FROM imdb_movies_b)
 UNION 
 SELECT * 
 FROM imdb_movies
 WHERE imdb_title_id NOT IN (SELECT imdb_title_id
						     FROM imdb_movies_b) 
 UNION
 SELECT *
 FROM imdb_movies_b
 WHERE imdb_title_id NOT IN (SELECT imdb_title_id
						     FROM imdb_movies)
 )
;

/* Transformate, math and clean of final universe*/ 
CREATE TABLE imdb_movies_global_2
AS
SELECT 	A.*, 
		B.avg_vote as avg_vote2
FROM imdb_movies_global_b AS A
LEFT JOIN imdb_ratings AS B
ON A.imdb_title_id = B.imdb_title_id
;

DROP TABLE imdb_movies_global_b;

CREATE TABLE imdb_movies_global
AS
SELECT  *,
		CASE WHEN avg_vote = avg_vote2 THEN avg_vote
			 WHEN avg_vote2 IS NULL THEN avg_vote
		ELSE (avg_vote + avg_vote2) / 2
		END AS avg_vote_f
FROM imdb_movies_global_2 
;

DROP TABLE imdb_movies_global_2;

ALTER TABLE imdb_movies_global
DROP COLUMN avg_vote, 
DROP COLUMN avg_vote2
;








