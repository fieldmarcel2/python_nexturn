from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user
)

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
app.config["SECRET_KEY"] = "secret123"

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@app.get("/")
def home():

    posts = Post.query.all()

    return render_template(
        "home.html",
        posts=posts
    )


@app.get("/post/<int:post_id>")
def post_detail(post_id):

    post = db.session.get(Post, post_id)

    if not post:
        flash("Post not found")
        return redirect(url_for("home"))

    return render_template(
        "post.html",
        post=post
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(
            username=username
        ).first()

        if user and user.password == password:

            login_user(user)

            flash("Login successful")

            return redirect(url_for("home"))

        flash("Invalid username or password")

    return render_template("login.html")


@app.get("/logout")
@login_required
def logout():

    logout_user()

    flash("Logged out successfully")

    return redirect(url_for("home"))


@app.route("/create", methods=["GET", "POST"])
@login_required
def create_post():

    if request.method == "POST":

        title = request.form.get("title")
        content = request.form.get("content")

        if not title or not content:

            flash("Title and content are required")

            return redirect(url_for("create_post"))

        post = Post(
            title=title,
            content=content,
            user_id=current_user.id
        )

        db.session.add(post)
        db.session.commit()

        flash("Post created successfully")

        return redirect(url_for("home"))

    return render_template("create.html")


@app.route("/edit/<int:post_id>", methods=["GET", "POST"])
@login_required
def edit_post(post_id):

    post = db.session.get(Post, post_id)

    if not post:
        flash("Post not found")
        return redirect(url_for("home"))

    if post.user_id != current_user.id:
        return "Unauthorized", 403

    if request.method == "POST":

        title = request.form.get("title")
        content = request.form.get("content")

        if not title or not content:

            flash("Title and content are required")

            return redirect(
                url_for(
                    "edit_post",
                    post_id=post.id
                )
            )

        post.title = title
        post.content = content

        db.session.commit()

        flash("Post updated successfully")

        return redirect(
            url_for(
                "post_detail",
                post_id=post.id
            )
        )

    return render_template(
        "edit.html",
        post=post
    )


@app.post("/delete/<int:post_id>")
@login_required
def delete_post(post_id):

    post = db.session.get(Post, post_id)

    if not post:
        flash("Post not found")
        return redirect(url_for("home"))

    if post.user_id != current_user.id:
        return "Unauthorized", 403

    db.session.delete(post)
    db.session.commit()

    flash("Post deleted successfully")

    return redirect(url_for("home"))


if __name__ == "__main__":

    with app.app_context():

        db.create_all()

        user = User.query.filter_by(
            username="gautam"
        ).first()

        if not user:

            user = User(
                username="gautam",
                password="1234"
            )

            db.session.add(user)
            db.session.commit()

    app.run(debug=True, port=5003)