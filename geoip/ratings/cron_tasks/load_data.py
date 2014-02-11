from django.core.management import call_command


def load_data():
    call_command('load_data')
