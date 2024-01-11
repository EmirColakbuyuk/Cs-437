
import sys
import os
import django
from django.core.management import call_command


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cs437.settings')
django.setup()

def run_custom_command(*args):

    call_command(args[0], *args[1:])

if __name__ == '__main__':

    run_custom_command(*sys.argv[1:])
