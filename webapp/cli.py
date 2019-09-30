import os

import logging
import click

from .auth.models import User, db

log = logging.getLogger(__name__)


def register(app):
    @app.cli.command("create-user")
    @click.argument("username")
    @click.argument("password")
    def create_user(username, password):
        user = User()
        user.username = username
        user.set_password(password)
        try:
            db.session.add(user)
            db.session.commit()
            click.echo(f"User {username} Added.")
        except Exception as e:
            log.error(f"Fail to add new user: {username} Error: {e} ")
            db.session.rollback()

    @app.cli.group()
    def translate():
        """Translation and localization commands."""
        pass

    @translate.command()
    def update():
        """Update all languages."""
        if os.system("pybabel extract -F ./babel/babel.cfg -k _l -o ./babel/messages.pot ."):
            raise RuntimeError("extract command failed")
        if os.system(
                "pybabel update -i ./babel/messages.pot -d webapp/translations"):
            raise RuntimeError("update command failed")
        os.remove("./babel/messages.pot")

    @translate.command()
    def compile():
        """Compile all languages."""
        if os.system("pybabel compile -d webapp/translations"):
            raise RuntimeError("compile command failed")

    @translate.command()
    @click.argument("lang")
    def init(lang):
        """Initialize a new language."""
        if os.system("pybabel extract -F ./babel/babel.cfg -k _l -o ./babel/messages.pot ."):
            raise RuntimeError("extract command failed")
        if os.system("pybabel init -i ./babel/messages.pot -d webapp/translations -l "
                     + lang):
            raise RuntimeError("init command failed")
        os.remove("./babel/messages.pot")
