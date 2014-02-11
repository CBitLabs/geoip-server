import kronos

from ratings.cron_tasks.load_data import load_data


@kronos.register("* * * * *")
def daily_cron():
    # download_data()
    load_data()
