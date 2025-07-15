from flask import Blueprint, render_template
from app.models.post import Post
from app.extensions import db

blog = Blueprint('blog', __name__)

@blog.route('/blog')
def blog_page():
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    return render_template('blog.html', posts=posts)
