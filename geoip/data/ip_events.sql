CREATE TABLE ratings_ipevents_tmp LIKE ratings_ipevents;
\copy ratings_ipevents_tmp FROM '/Users/jblum/work/ip-stats.csv' DELIMITER ',' CSV;
CREATE INDEX addr_idx ON ratings_ipevents_tmp (address);
RENAME TABLE ratings_ipevents TO old_ratings_ipevents, 
            ratings_ipevents_tmp TO ratings_ipevents;

DROP TABLE old_ratings_ipevents;
