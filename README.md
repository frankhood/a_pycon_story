# A Pycon Story

## Index

- [Dockerized Development](#dockerized-development)
- [Local Development](#local-development)
- [Install or Update requirements](#install-or-update-requirements)
- [Remove requirements](#remove-requirements)
- [Create new app](#create-new-app)

## Dockerized Development

This is the recommended method for developing a project as it does not require special installations on your machine.

After the project creation you need to run this command:

```console
make dup
```

This command will start all development dockers which will be used for:

- a_pycon_story_postgres  # DATABASE

- a_pycon_story_nginx  # TO EXPOSE SERVICE WITH HTTP or HTTPS TO TEST stage or prod environment
- a_pycon_story_backend  # TO RUN AND DEVELOP YOUR DJANGO PROJECT
- a_pycon_story_backend_qcluster  # TO RUN QCLUSTER ON ANOTHER INSTANCE OF YOUR CODE WHILE DEVELOPING
- a_pycon_story_mailhog  # TO TEST YOUR EMAILS

If you want to develop in an environment more similar to that of stage and prod you should know that ngnix is displayed on the ports indicated in your `.env` in the variables:

- LOCAL_HTTP_PORT  # BY DEFAULT IS 8080
- LOCAL_HTTPS_PORT  # BY DEFAULT IS 8443

If you want to develop in a faster environment you can directly use the port exposed by the a_pycon_story_backend service and override it in your `.env` at the variable:

- EXPOSE_PORT  # BY DEFAULT 8030

After change this environment variable you need to rebuild dockers, then run:

```console
make ddown
make dup
```

## Local Development

![Are you sure?](https://dev.frankhood.dev/media/nonono.gif)

First of all you need to know that this configuration is meant to have only the database docker for development, if you want to change the database using one locally just change this environment variable in your `.env`:

- DATABASE_URL=DATABASE_ENGINE://root:DATABASE_PASSWORD@127.0.0.1:DATABASE_PORT/DATABASE_NAME  # documentation for dj-database-url at <https://github.com/kennethreitz/dj-database-url>
  - If your password contains special characters urlencode the password like: `@ => %40`.
    You can use for example this command:
    `python3 -c 'import urllib.parse; print(urllib.parse.quote_plus("<youpassword>"))'`

You need to know that there are variables that you can insert in your `.zshrc` or `.bashrc` to assign different user passwords for creating the mysql database locally, this can be done by inserting the variables:

- ENV_STARTFH_DB_MYSQL_ROOT_PWD=<db_rootuser_private_pwd>
- ENV_STARTFH_DB_PWD=<db_private_pwd>

To start your local environment with virtualenv and database for docker run:

```console
./dev.sh
```

This command will:

- Create a python virtualenv
- Install requirements/dev.txt
- Create `.env` file if not exist using the content of `.env_template`
- Create and run db container
- Create and run mailhog container for mail testing
- Make pull of the current branch
- Install pre-commit
- Create database if not exist using the content of the environment variable `DATABASE_URL` (if used database user can create database)
- Migrate new migration if there are
- Install FE requirements

If the `./dev.sh` command raise or similar :

```console
warning postcss-preset-env > postcss-color-functional-notation > postcss-values-parser > flatten@1.0.3: flatten is deprecated in favor of utility frameworks such as lodash.
[2/4] :truck:  Fetching packages...
error https://registry.yarnpkg.com/core-js/-/core-js-3.18.1.tgz: Extracting tar content of undefined failed, the file appears to be corrupt: "Invalid tar header. Maybe the tar is corrupted or it needs to be gunzipped?"
info Visit https://yarnpkg.com/en/docs/cli/install for documentation about this command.
```

if you have a mac with M1, you have to make sure you have opened the terminal with Rosetta (Applications/Utility/terminal > Get information > check the option "Open with Rosetta").

If the problem recurs you have to substitute your tar open archiver with gnu-tar using brew, then run

```console
# if you are on M1
arm brew install gnu-tar
# else
brew install gnu-tar
```

### Install or Update requirements

Edit the appropriate requirements file `*.in`, to add/remove pinned libraries or modify their versions.

To update the compiled requirements files (`requirements/*.txt`), execute:

```console
inv pip  # this will update all the packages
# or
inv pip-upgrade-package -p="{name_of_package}, {name_of_package}"
# it is no longer necessary to run the inv dev command to update packages
```

Then update your virtualenv with this command:

```console
pip-sync requirements/dev.txt
```

### Remove requirements

To remove a specific library from your virtualenv execute:

```console
# if you want to remove a package from all requirements run:
inv pip-downgrade-package -p="{name_of_package}, {name_of_package}"
# if you want to remove a package only from a certain requirements run:
inv pip-downgrade-package -p="{name_of_package}, {name_of_package}" -r="common or dev or prod or tests"
# it is no longer necessary to run the inv dev command to downgrade packages
```

Then update your virtualenv with this command:

```console
pip-sync requirements/dev.txt
```

## Create new app

To create a new app run:

```console
./manage.py startapp_fh
```

This command wille execute the cookiecutter.json of <https://gitlab.com/fh-start/fh-startapp-cookiecutter-template>
