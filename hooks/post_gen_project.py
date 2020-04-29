import os

TERMINATOR = "\x1b[0m"
WARNING = "\x1b[1;33m [WARNING]: "
INFO = "\x1b[1;33m [INFO]: "
HINT = "\x1b[3;33m"
SUCCESS = "\x1b[1;32m [SUCCESS]: "


def remove_celery_files():
    file_names = [
        os.path.join("config", "celery_app.py"),
    ]
    for file_name in file_names:
        os.remove(file_name)


def remove_graphene_files():
    file_names = [
        os.path.join("config", "schema.py"),
        os.path.join("apps", "custom_user", "mutations.py"),
        os.path.join("apps", "custom_user", "test_mutations.py"),
    ]
    for file_name in file_names:
        os.remove(file_name)


def main():
    if "{{ cookiecutter.celery }}".lower() == "n":
        remove_celery_files()

    if "{{ cookiecutter.graphene }}".lower() == "n":
        remove_graphene_files()


if __name__ == "__main__":
    main()
