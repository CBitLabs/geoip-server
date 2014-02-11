CREATE TABLE ratings_ipevents_tmp (LIKE ratings_ipevents);
\copy ratings_ipevents_tmp FROM 'ip-stats.csv' DELIMITER ',' CSV HEADER;

BEGIN;
DROP INDEX IF EXISTS addr_idx;
CREATE INDEX addr_idx ON ratings_ipevents_tmp (ip);
ALTER TABLE ratings_ipevents RENAME TO ratings_ipevents_old;
ALTER TABLE ratings_ipevents_tmp RENAME TO ratings_ipevents;
DROP TABLE ratings_ipevents_old;
COMMIT;
