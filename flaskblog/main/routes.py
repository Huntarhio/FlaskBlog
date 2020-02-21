from flask import Blueprint, render_template
from flaskblog.models import Post

main = Blueprint('main', __name__)

@main.route("/")
@main.route("/home")
def home():
    # posts = Post.query.all()
    page = request.args.get('page', 1, type=int)   # gets the page and the id of the page
    posts = Post.query.order_by(Post.posted_date.desc()).paginate(page=page, per_page=5) #sets the ordering of the items in the page and also sets the number of items per page
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')