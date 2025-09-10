import os
from dotenv import load_dotenv

load_dotenv()


CLOUDNAME = os.getenv('CLOUDNAME')
CLOUDKEY = os.getenv('CLOUDKEY')
CLOUDSECRET = os.getenv('CLOUDSECRET')