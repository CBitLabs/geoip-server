import kronos

from ratings.cron_tasks.load_data import load_data


@kronos.register("0 0 * * *")
def daily_cron():
    # download_data()
    load_data()
