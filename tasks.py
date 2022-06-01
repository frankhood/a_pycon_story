import os
import secrets
import sys
from pathlib import Path

from invoke import task


def encode(to_encode):
    import urllib.parse

    return urllib.parse.quote_plus(to_encode)


def generate_random_password(password_length):
    import random
    import string

    characters = list(string.ascii_letters + string.digits + "!@#%^&*()")

    random.shuffle(characters)
    random_password = []
    for _i in range(password_length):
        random_password.append(random.choice(characters))

    random.shuffle(random_password)

    return "".join(random_password)


@task
def check(c):
    c.run("black --check .")
    c.run("isort --check .")
    c.run("flake8")
    c.run("mypy .")


@task
def fix(c):
    c.run("black .")
    c.run("isort .")
    c.run("flake8")
    c.run("mypy .")


@task
def collectstatic(c):
    c.run("python manage.py collectstatic --clear --noinput")


@task
def compilemessages(c):
    c.run("python manage.py compilemessages -i .tox")


DEFAULT_DATABASE_URL = "mysql://root@127.0.0.1/a_pycon_story"


def populate_dotenv(database_url: str = DEFAULT_DATABASE_URL):

    env_template = Path(".env_template").read_text()
    # Se ci sono le variabili della password nel zshrc/bashrc usa quelle per generare il db
    # se così non fosse utilizza DATABASE_URL, rimuovi dalla firma del metodo database_url e dalla definizione sopra il metodo
    # Utilizza Postgres 12 per capire quale databaseurl usare
    db_pwd = os.environ.get("ENV_STARTFH_DB_PWD", generate_random_password(15))
    db_root_pwd = os.environ.get("ENV_STARTFH_DB_MYSQL_ROOT_PWD", generate_random_password(15))
    env_text = (
        env_template.replace("__SECRETKEY__", secrets.token_urlsafe(40))
        .replace("__DATABASE_PASSWORD__", db_pwd)
        .replace("__DATABASE_PASSWORD_ENCODED__", encode(db_pwd))
        .replace("__DATABASE_ROOT_PASSWORD__", db_root_pwd)
        .replace("__DATABASE_ROOT_PASSWORD_ENCODED__", encode(db_root_pwd))
    )
    Path(".env").write_text(env_text)


@task
def create_environment(c):
    from dotenv import find_dotenv, load_dotenv

    try:
        if find_dotenv():
            load_dotenv(find_dotenv())
            print(".env file already created!")
        else:
            print("Creating .env file...")
            populate_dotenv()
            print(".env file created!")
    except Exception as ex:
        print(ex)


def create_database_if_not_exist():
    from dotenv import find_dotenv, load_dotenv
    from sqlalchemy import create_engine
    from sqlalchemy_utils import create_database, database_exists

    load_dotenv(find_dotenv())
    # TODO VEDIAMOLO DOPO CON BOT
    #   OPTIONS, COLLATE E CHARSET
    url = os.environ["DATABASE_URL"]
    engine = create_engine(url, echo=True)

    if not database_exists(engine.url):
        create_database(engine.url)
    else:
        engine.connect()


@task
def create_database(c):
    create_database_if_not_exist()
    c.run("python manage.py migrate")


@task
def create_and_run_db_container(c):
    c.run(
        "docker compose up -d postgres --wait || echo '🚨 NON È STATO POSSIBILE CREARE IL DOCKER PER IL DATABASE!!! 🚨'"
    )
    c.run("docker compose up -d mailhog --wait || echo '🚨 NON È STATO POSSIBILE CREARE IL DOCKER PER MAILHOG !!! 🚨'")


@task
def git_configuration(c):
    c.run("git pull -v || true")
    c.run("pre-commit install || true")


@task(
    post=[
        create_environment,
        create_and_run_db_container,
        git_configuration,
        create_database,
    ],
)
def dev(c):
    print("Running Invoke Dev command")


@task
def delete_all_tables(c):
    from dotenv import find_dotenv, load_dotenv
    from sqlalchemy import create_engine
    from sqlalchemy_utils import create_database, database_exists, drop_database

    load_dotenv(find_dotenv())
    url = os.environ["DATABASE_URL"]
    engine = create_engine(url, echo=True)

    if database_exists(engine.url):
        drop_database(engine.url)
    create_database(engine.url)
    c.run("python manage.py migrate")


@task
def graph_models(c):
    c.run("python manage.py graph_models -o models.svg")


@task
def messages(c):
    c.run("python manage.py makemessages --add-location file")


@task
def migrate(c):
    c.run("python manage.py migrate --noinput")


@task
def migrations(c):
    c.run("python manage.py makemigrations --no-header")


@task
def pip(c):
    # c.run("pip install -q -U pip~=22.0.0")
    print("Started compiling all requirements")
    c.run("pip-compile -q -U -o requirements/dev.txt requirements/dev.in")
    print("Compiled dev.txt")
    c.run("pip-compile -q -U -o requirements/tests.txt requirements/tests.in")
    print("Compiled tests.txt")


@task
def pip_upgrade_package(c, packages=""):
    c.run("pip install -q pip~=22.0.0")
    print("Installed pip~=22.0.0")
    for package in packages.split(","):
        package = package.strip()
        print(f"Started compiling all requirements for {package}")
        c.run(f"pip-compile -q -o requirements/dev.txt requirements/dev.in --upgrade-package {package}")
        print(f"Compiled dev.txt for {package}")
        c.run(f"pip-compile -q -o requirements/tests.txt requirements/tests.in --upgrade-package {package}")
        print(f"Compiled tests.txt for {package}")


def remove_package_from_requirements(package_name, filename):
    # Remove from common.in and common.txt a package
    in_filename = "requirements/" + filename + ".in"
    txt_filename = "requirements/" + filename + ".txt"
    with open(in_filename, "r") as in_file:
        in_lines = in_file.readlines()
    with open(txt_filename, "r") as txt_file:
        txt_lines = txt_file.readlines()

    for idx, line in enumerate(in_lines):
        if package_name in line:
            del in_lines[idx]

    for idx, line in enumerate(txt_lines):
        if package_name in line:
            del txt_lines[idx]
            if "#" in line and "#" not in txt_lines[idx - 1]:
                del txt_lines[idx - 1]

    with open(in_filename, "w+") as in_file:
        for line in in_lines:
            in_file.write(line)
    print(f"Successfully removed {package_name} from {in_filename}")
    with open(txt_filename, "w+") as txt_file:
        for line in txt_lines:
            txt_file.write(line)
    print(f"Successfully removed {package_name} from {txt_filename}")


@task
def pip_downgrade_package(c, packages="", requirement_name="all"):
    if packages:
        for package in packages.split(","):
            package = package.strip()
            if package:
                if requirement_name in ["dev", "all"]:
                    remove_package_from_requirements(package, "dev")
                if requirement_name in ["tests", "all"]:
                    remove_package_from_requirements(package, "tests")
    else:
        sys.exit("Choose packages to downgrade a package with pip-downgrade-package")


@task
def simplecoverage(c):
    c.run(
        "coverage run --concurrency=multiprocessing manage.py test --noinput --parallel --debug-sql && coverage combine && coverage report"
    )


@task
def simpletest(c):
    c.run("python manage.py test --configuration=Testing --parallel --debug-sql")
    # simpletest


@task
def test(c):
    c.run("tox -e coverage,reporthtml,report")


@task
def dumpdata(c, output, models=None):
    """
    Call this task in this way.

    invoke dumpdata --output="path/to/your/dir" --models="app_label.ModelName app_label.ModelName"
    """
    c.run(
        "python manage.py dumpdata --indent=4 --natural-foreign --format=json -o={output} {models}".format(
            output=output, models=models
        )
    )


# =============================
# Docker utils
# =============================
@task(
    help={
        "container_name": "Insert a container name default = ''",
    }
)
def rebuild(c, container_name=""):
    """Stop and rebuild a specific container or all containers specified in docker-compose.yml."""
    c.run(
        f"docker compose stop {container_name} && docker compose rm -f {container_name} && docker compose up -d --build {container_name}"
    )


@task(
    help={
        "container_name": "Insert a container name default = a_pycon_story_backend",
        "command": "Insert a specific command to execute default = shell",
    }
)
def django(c, container_name="a_pycon_story_backend", command="shell"):
    """Run a specific manage.py command in a container."""
    print(f"docker exec -it {container_name} python manage.py {command}")
    os.system(f"docker exec -it {container_name} python manage.py {command}")


@task(
    help={
        "container_name": "Insert a container name default = a_pycon_story_backend",
    }
)
def touchbackend(c, container_name="a_pycon_story_backend"):
    """Update a specific container."""
    print(f"Update docker of {container_name}")
    os.system(f"docker exec -it {container_name} touch uwsgiconf/docker.ini")


@task
def dumpdb(c):
    """Dump a zipped copy of your docker database in the parent dir of your project."""
    from dotenv import find_dotenv, load_dotenv

    load_dotenv(find_dotenv())
    db_name = os.environ["DATABASE_NAME"]
    db_container = "a_pycon_story_postgres"
    db_user = os.environ["DATABASE_USER"]
    db_password = os.environ["DATABASE_PASSWORD"]
    print(f"Dumping {db_name} database")
    if "/backend/" in str(Path(__file__).resolve().parents[0]):
        dumpdir = "../../backups/a_pycon_story"
    else:
        dumpdir = "../backups/a_pycon_story"
    c.run(f"mkdir -p {dumpdir}")
    print(f"Dumping {db_name} database")
    os.system(f"mkdir -p {dumpdir}")

    os.system(
        f"docker exec -it {db_container} bash -c 'PGPASSWORD={db_password} pg_dump --no-owner -U {db_user} -d {db_name}' > {dumpdir}/{db_name}.sql"
    )

    print(f"Successfully dumped {db_name}")
    os.system(f"rm -f {dumpdir}/{db_name}.zip")
    os.system(f"cd {dumpdir}; zip -er {db_name}.zip {db_name}.sql")
    os.system(f"rm -f {dumpdir}/{db_name}.sql")


@task
def stop_and_delete_all_volumes(c):
    """Stop all containers."""
    c.run("docker compose down -v --remove-orphans")
    print("Docker stopped")


@task
def stop(c):
    """Stop all containers."""
    c.run("docker compose down --remove-orphans")
    print("Docker stopped")


@task(pre=[stop])
def drop(c):

    c.run("docker volume rm a_pycon_story_pg_data || echo 'volume not found'")

    print("Docker volume dropped")


@task
def start(c):
    c.run("docker compose up --build -d")
    print("Successfully started dockers")


@task(pre=[stop, start])
def restart(c):
    """Restart all containers."""
    print("Successfully restarted dockers")


@task(pre=[drop, restart])
def resetdb(c):
    """Reset docker, clearing volumes(db)."""
    print("Successfully resetted db")


@task(pre=[resetdb])
def restoredb(c):
    """imports db from backups/a_pycon_story/a_pycon_story.zip"""
    from dotenv import find_dotenv, load_dotenv

    load_dotenv(find_dotenv())
    db_name = os.environ["DATABASE_NAME"]
    db_container = "a_pycon_story_postgres"
    db_user = os.environ["DATABASE_USER"]
    db_password = os.environ["DATABASE_PASSWORD"]
    if "/backend/" in str(Path(__file__).resolve().parents[0]):
        dumpdir = "../../backups/a_pycon_story"
    else:
        dumpdir = "../backups/a_pycon_story"

    os.system(f"unzip {dumpdir}/a_pycon_story.zip -d {dumpdir}")
    print("DB Decompressed")
    print("Pause for up DB service")
    import time

    time.sleep(10)
    # TODO capire come fare ad importare il db

    c.run(
        f"cat {dumpdir}/a_pycon_story.sql | grep -v -E '^(CREATE\\ EXTENSION)|CREATE\\ SCHEMA|COMMENT ON)' | docker exec -i {db_container} /bin/bash -c 'PGPASSWORD={db_password} psql -U {db_user} -q -E -d {db_name}' 2>&1 > /dev/null && echo -e restore done"
    )

    c.run(f"rm -f {dumpdir}/a_pycon_story.sql")
    c.run("python manage.py migrate")
    print("...Restore db done")
