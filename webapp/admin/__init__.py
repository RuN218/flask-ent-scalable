from flask_admin import Admin

from .. import db
from webapp.auth.models import Role, User
from webapp.blog.models import Tag, Comment, Reminder, Post
from .controllers import CustomView, CustomModelView, CustomFileAdmin, PostView

admin = Admin()


def create_module(app, **kwargs):
    admin.init_app(app)
    admin.add_view(CustomView(name="Custom"))

    models = [User, Role, Comment, Tag, Reminder]

    for model in models:
        admin.add_view(CustomModelView(model, db.session, category="Models"))

    admin.add_view(PostView(Post, db.session, category="Models"))
    admin.add_view(CustomFileAdmin(app.static_folder, "/static/",
                                   name="Static Files"))
