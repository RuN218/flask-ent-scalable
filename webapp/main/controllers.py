from flask import redirect, url_for, Blueprint, render_template

main_blueprint = Blueprint("main", __name__,
                           template_folder="../templates/main")


@main_blueprint.route("/")
def index():
    return redirect(url_for("blog.home"))
