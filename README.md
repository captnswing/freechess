fig up -d
fig run web python ./freechess/manage.py syncdb --noinput
fig run web python ./freechess/manage.py loaddata admin_user

http://freechess.herokuapp.com/
