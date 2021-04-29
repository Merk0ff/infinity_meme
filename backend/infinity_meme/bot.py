import os
import sys
import django

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'infinity_meme.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

django.setup(set_prefix=False)

from bots.tg_review_bot import main

main()

