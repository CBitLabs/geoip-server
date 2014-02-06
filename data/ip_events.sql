CREATE TABLE ip_events (
    date int,
    address inet,
    spam_count int,
    spam_freq int,
    bot_count int,
    bot_freq int,
    unexp_count int,
    unexp_freq int);

\copy ip_events from '/Users/stuart/Desktop/ip-stats-50.txt' DELIMITER ',' CSV;
CREATE INDEX addr_idx on ip_events (address);