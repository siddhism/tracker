virtualenv env_tracker
source env_tracker/bin/activate
pip install -r requirements.txt
./manage.py migrate
./manage.py runserver 7001
