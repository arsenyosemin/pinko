from flask_security import current_user
from taozi.models import Post, Event, Issue
from flask import Blueprint, render_template, abort, redirect, request

routes = Blueprint('pinko', __name__)

@routes.route('/')
def index():
    issue = Issue.query.filter(Issue.published).order_by(Issue.id.desc()).first()
    posts = Post.query.filter(Post.published).limit(3)
    return render_template('index.html', issue=issue, posts=posts)

@routes.route('/<issue>/<slug>')
def post(issue, slug):
    post = Post.query.filter(Post.slug==slug, Post.issue.has(slug=issue)).first_or_404()
    if not post.published and not current_user.is_authenticated:
        abort(404)
    return render_template('post.html', post=post)

@routes.route('/issue/<slug>')
def issue(slug):
    issue = Issue.query.filter(Issue.slug==slug).first_or_404()
    if not issue.published and not current_user.is_authenticated:
        abort(404)
    return render_template('issue.html', issue=issue)

@routes.route('/archive')
def archive():
    posts = Post.query.filter(Post.published).all()
    return render_template('archive.html', posts=posts)

@routes.route('/issues')
def issues():
    issues = Issue.query.filter(Issue.published).all()
    return render_template('issues.html', issues=issues)

@routes.route('/search')
def search():
    query = request.args.get('query')
    posts = Post.search(query) if query else []
    return render_template('search.html', query=query, posts=posts)

@routes.route('/manifesto')
def manifesto():
    return 'TODO'
