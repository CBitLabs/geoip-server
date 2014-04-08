"""
	Single place to run any cron tasks.
	Utilizes the kronos module to schedule commands
"""


from django.core.management import call_command

import kronos


@kronos.register("0 0 * * *")
def daily_cron():
    call_command('add_location')
    call_command('download_data')
    call_command('load_data')
