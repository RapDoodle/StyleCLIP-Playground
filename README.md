# DegreeOverview
DegreeOverview is a course definition system that aims to help course designers better plan and design university courses and enables both the lecturers and students to understand and visualize the relationships between courses and their intended learning outcome.

## Generating test data

To populate your database with test data, run

  ```bash
  $ python populate.py
  ```

The default users:

- Default course designer

  Username: testcd1

  Password: 12345678

- Default lecturer

  Username: testlecturer1

  Password: 12345678

- Default student

  Username: teststudent1

  Password: 12345678

## Running in production mode

The default production mode uses MySQL as the backend for the database. Please make sure you have your instance of the database running. Specify your configuration in `./configurations/production.json`

To spin up the production server in test mode

```bash
$ python run.py production
```

## Getting Started with the Development

- Clone the repository

  ```shell
  git clone https://github.com/RapDoodle/comp3053-project.git
  ```

- Create virtual environments

  For Anaconda users
  ```bash
  $ conda create -n degreeoverview python=3.8.5
  ```

- Activate the environment

  To activate the virtual environment created
  ```bash
  $ conda activate degreeoverview
  ```

  If you are using the default command-line tool on Windows, use
  ```bash
  activate degreeoverview
  ```

- Install required Python packages

  For Linux users
  ```bash
  $ pip3 install -r requirements.txt
  ```

  For Windows users
  ```bash
  pip install -r requirements.txt
  ```

  Please be noted that some dependencies may not be installed on Debian and Ubuntu. If an error occurred while installing `bcrypt`, run the following command

  ```bash
  $ sudo apt-get install build-essential libffi-dev python-dev
  ```

- Spinup a development server

  ```bash
  $ python3 run.py dev
  ```
  For Windows users,
  ```bash
  python run.py dev
  ```
  In the last argument, `dev` specifies the name of the configuration. Please visit the documents on configurations under the `docs` folder for more information about the configurations.

## Contributors
- Group Lily

## Credits
Part of the code of this project is based on the open-source development framework, Mangee Flask-RESTful. The framework was developed by Bohui WU (@RapDoodle, one of our team members) and licensed under the GNU General Public License v3 (the same as this project). The complete source code of the framework can be found in https://github.com/RapDoodle/mangee-flask-restful.

## License
The project is licensed under the GNU General Public License v3.

## Copyright
Copyright (c) 2021.