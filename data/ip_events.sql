CREATE TABLE ip_events_100 (
    date int,
    address inet,
    spam_count int,
    spam_freq int,
    bot_count int,
    bot_freq int,
    unexp_count int,
    unexp_freq int);

\copy ip_events_100 from '/Users/jblum/work/ip-stats-16000-16099.csv' DELIMITER ',' CSV;
CREATE INDEX addr_100_idx on ip_events_100 (address);