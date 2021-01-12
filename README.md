# Contact Tracker

Contact Tracker is a way to track who is comming and going from a building so that if someone were to come down with a case of covid those in the building at the time can be notified.

## Getting Started

### Python

You must have Python 3.8 installed.

Install all the packages in requirements.txt using  `pip3 install -r requirements.txt.`

### Mongo DB

You must have a database for the buildings and logs to be stored.

For help setting up a database see [Mongo DB Atlas](https://www.mongodb.com/cloud/atlas)

### Config File

Place a file named **confing.env** inside the root directory. This file should include:

* A password to be  used to login to the logs page labeled ADMIN_PASSWORD
* A username to be used to login to the logs page labeled ADMIN_USERNAME
* A string or phrase to be stored as a cookie under SECRETKEY
* The path to the logo you want to appear in the upper left labeled LOGOPATH
* A list of the buildings to be tracked labeled BUILDINGS
* A URL to the Mongo DB database under MONGOURL

For formating help view the **example_config.env** file.

### Running

You can run this using `python3 main.py` using terminal from the root directory.

## Using the Website

### Homepage

The homepage on the root url allows the user to enter their name and select the building they are entering as well as if they are leaving or entering.

### Direct Links

For ease of use a link can be provided in the formatt of _www.thiswebsite.com/Building1_ which will take the user directly to a signin page for that building and that building only.

### Viewing Logs

On the top right of every page there is a login button clicking this allows and Admin to login using the username and password.

On this page you can select a building and then hit go which will allow the user to select a date. Hitting Go will then show the logs for that building and date.

Pressing the download button will download a pdf of the date you are viewing.
