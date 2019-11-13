# ProctorialSystemBackend
Server-side code for Aftaab99/ProctorialSystemApp


## Running locally
Make sure python3 is installed, then install requirements using
    pip install -r requirements.txt

To start the server run,
    python main.py

This starts a server listening at `http://localhost:5000/`. Clicking on the link should take you to a empty index page. Head over to `http://localhost:5000/admin/login` to login with the admin password. 

## Note

Departments route is at `http://localhost:5000/admin/department`.

All html files need to placed inside the `templates` direcctory. All JS in `static/js`. Check out some of the HTML files for how to link the JS files.

## Git commands
From inside the clone of your forked directory, run this in your clone before making changes
    
    git checkout development

Then push your changes

    git add .
    git commit -m 'What changes you made'
    git push origin development

Then headover to your forked repo on Github, click new pull request and create new pull request.