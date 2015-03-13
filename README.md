# docker-compose

    docker-compose up -d
    docker-compose run web python ./freechess/manage.py syncdb --noinput
    docker-compose run web python ./freechess/manage.py loaddata admin_user

# Google Container engine

https://cloud.google.com/container-engine/docs/hello-wordpress

# Heroku bootstrap

    brew install heroku-toolbelt
    heroku login
    heroku info --app freechess
    git remote add heroku git@heroku.com:freechess.git
    git push -f heroku master
    heroku ps:scale web=1
    heroku run python manage.py syncdb --noinput
    heroku logs --tail

http://freechess.herokuapp.com/
