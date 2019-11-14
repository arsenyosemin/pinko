import config
from flask_security import current_user
from taozi.models import Post, Event, Issue
from taozi.compile import compile_markdown
from konbini.core import get_product, get_products
from flask import Blueprint, render_template, abort, redirect, request, url_for

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

@routes.route('/in-print/<slug>')
def issue(slug):
    issue = Issue.query.filter(Issue.slug==slug).first_or_404()
    if not issue.published and not current_user.is_authenticated:
        abort(404)
    issue.description = compile_markdown(issue['description'])
    return render_template('issue.html', issue=issue)

@routes.route('/magazine')
def archive():
    posts = Post.query.filter(Post.published, Post.print_only==False, Post.event==None).all()
    return render_template('archive.html', posts=posts)

@routes.route('/in-print')
def issues():
    issues = Issue.query.filter(Issue.published, Issue.name != 'Web').all()
    manifesto = get_product(config.MANIFESTO_PRODUCT_ID)
    zines = [p for p in get_products() if p.metadata.get('zine') == 'true']
    return render_template('issues.html', issues=issues, manifesto=manifesto, zines=zines)

@routes.route('/events')
def events():
    events = [e.post for e in Event.query.order_by(Event.end.desc(), Event.start.asc()).all() if e.post.published]
    events.reverse()
    return render_template('events.html', events=events)

@routes.route('/search')
def search():
    query = request.args.get('query')
    posts = Post.search(query) if query else []
    return render_template('search.html', query=query, posts=posts)

@routes.route('/about')
def about():
    return render_template('about.html')

@routes.route('/subscribe')
def subscribe():
    return redirect(url_for('shop.plan', id=config.SUBSCRIPTION_PLAN_ID))

@routes.route('/store/manifesto')
def manifesto():
    return redirect(url_for('shop.product', id=config.MANIFESTO_PRODUCT_ID))
