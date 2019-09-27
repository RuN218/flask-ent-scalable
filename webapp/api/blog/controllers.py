import datetime

from flask import abort, current_app, jsonify, request
from flask_restful import Resource, fields, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity

from webapp.blog.models import db, Post, Tag, Comment
from webapp.auth.models import User
from .parsers import (
    post_get_parser,
    post_post_parser,
    post_put_parser,
    comment_get_parser, comment_put_parser, comment_post_parser)
from .fields import HTMLField

nested_tag_fields = {
    "id": fields.Integer(),
    "title": fields.String()
}

comment_fields = {
    "id": fields.Integer(),
    "name": fields.String(),
    "text": fields.String(),
    "date": fields.DateTime(dt_format="iso8601"),
    "post_id": fields.Integer()
}

post_fields = {
    "id": fields.Integer(),
    "author": fields.String(attribute=lambda x: x.user.username),
    "title": fields.String(),
    "text": HTMLField(),
    "tags": fields.List(fields.Nested(nested_tag_fields)),
    "comments": fields.List(fields.Nested(comment_fields)),
    "publish_date": fields.DateTime(dt_format="iso8601")
}


def add_tags_to_post(post, tags_list):
    for item in tags_list:
        tag = Tag.query.filter_by(title=item).first()

        if tag:
            post.tags.append(tag)
        else:
            new_tag = Tag(item)
            post.tags.append(new_tag)


class PostApi(Resource):
    @marshal_with(post_fields)
    @jwt_required
    def get(self, post_id=None):
        if post_id:
            post = Post.query.get(post_id)
            if not post:
                abort(404)
            return post
        else:
            args = post_get_parser.parse_args()
            page = args["page"] or 1

            if args["user"]:
                user = User.query.filter_by(usesrname=args["user"]).first()
                if not user:
                    abort(404)

                posts = user.posts.order_by(
                    Post.publish_date.desc()
                ).paginate(page, current_app.config["POSTS_PER_PAGE"])
            else:
                posts = Post.query.order_by(
                    Post.publish_date.desc()
                ).paginate(page, current_app.config["POSTS_PER_PAGE"])

            return posts.items

    @jwt_required
    def post(self):
        print(request.data)
        args = post_post_parser.parse_args(strict=True)
        new_post = Post(args["title"])
        new_post.user_id = get_jwt_identity()
        new_post.text = args["text"]

        if args["tags"]:
            add_tags_to_post(new_post, args["tags"])

        db.session.add(new_post)
        db.session.commit()
        return {"id": new_post.id}, 201

    @jwt_required
    def put(self, post_id=None):
        if not post_id:
            abort(400)
        post = Post.query.get(post_id)
        if not post:
            abort(404)
        args = post_put_parser.parse_args(strict=True)
        if get_jwt_identity() != post.user_id:
            abort(403)
        if args["title"]:
            post.title = args["title"]
        if args["text"]:
            post.text = args["text"]
        if args["tags"]:
            print(f"Tags {args['tags']}")
            add_tags_to_post(post, args["tags"])

        db.session.merge(post)
        db.session.commit()
        return {"id": post.id}, 201

    @jwt_required
    def delete(self, post_id=None):
        if not post_id:
            abort(400)
        post = Post.query.get(post_id)
        if not post:
            abort(404)
        if get_jwt_identity() != post.user_id:
            abort(401)

        db.session.delete(post)
        db.session.commit()
        return "", 204


class CommentsByPostApi(Resource):
    @marshal_with(comment_fields)
    @jwt_required
    def get(self, post_id=None):
        if post_id:
            post = Post.query.get(post_id)
            if not post:
                abort(404)
            args = comment_get_parser.parse_args()
            page = args["page"] or 1

            comments = post.comments.order_by(
                Comment.date.desc()
            ).paginate(page, current_app.config["POSTS_PER_PAGE"])
            if not comments:
                abort(404)
            return comments.items
        else:
            abort(404)

    @jwt_required
    def post(self, post_id=None):
        print(request.data)
        if post_id:
            if Post.query.filter_by(id=post_id).count() < 1:
                abort(404)
            args = comment_post_parser.parse_args(strict=True)
            user = User.query.get(get_jwt_identity())
            new_comment = Comment(name=user.username, text=args["text"])
            new_comment.post_id = post_id

            db.session.add(new_comment)
            db.session.commit()
            return {"id": new_comment.id}, 201
        else:
            abort(404)

    @jwt_required
    def put(self, post_id=None, comment_id=None):
        if post_id:
            post = Post.query.get(post_id)
            if not post:
                abort(404)
            comment = post.comments.filter_by(id=comment_id).one()
            if not comment:
                abort(404)
            args = comment_put_parser.parse_args(strict=True)
            if args["text"]:
                comment.text = args["text"]

            db.session.merge(comment)
            db.session.commit()
            return {"post_id": post_id, "id": comment.id}, 201
        else:
            abort(404)

    @jwt_required
    def delete(self, post_id=None, comment_id=None):
        if post_id:
            post = Post.query.get(post_id)
            if not post:
                abort(404)
            comment = post.comments.filter_by(id=comment_id).one()
            if not comment:
                abort(404)

            db.session.delete(comment)
            db.session.commit()
            return "", 204
        else:
            abort(404)


class CommentApi(Resource):
    @marshal_with(comment_fields)
    @jwt_required
    def get(self, comment_id=None):
        if comment_id:
            comment = Comment.query.get(comment_id)
            if not comment:
                abort(404)
            return comment
        else:
            args = comment_get_parser.parse_args()
            page = args["page"] or 1

            comments = Comment.query.order_by(
                Comment.date.desc()
            ).paginate(page, current_app.config["POSTS_PER_PAGE"])

            return comments.items

    @jwt_required
    def put(self, comment_id=None):
        if not comment_id:
            abort(400)
        comment = Comment.query.get(comment_id)
        if not comment:
            abort(404)
        args = comment_put_parser.parse_args(strict=True)
        if args["text"]:
            comment.text = args["text"]

        db.session.merge(comment)
        db.session.commit()
        return {"id": comment.id}, 201

    @jwt_required
    def delete(self, comment_id=None):
        if not comment_id:
            abort(400)
        comment = Comment.query.get(comment_id)
        if not comment:
            abort(404)

        db.session.delete(comment)
        db.session.commit()
        return "", 204
