from flask import Flask, render_template, abort, redirect, url_for, request, g
from flask.ext.babelex import Babel,format_datetime, gettext, lazy_gettext, Domain
from os.path import join, exists
from os import environ, makedirs
from shutil import rmtree
from cache import cache
import translation
from blog import blog
from docs import docs
from main import main
from parts import parts
from . import utils, html, cms

app = Flask(__name__)

cachedir = join(environ["OPENSHIFT_DATA_DIR"],"cache")
#clear cache
if exists(cachedir):
	rmtree(cachedir)
makedirs(cachedir)

app.config['CACHE_DIR'] = cachedir

#set timeout to about a month, as content only changes on push, and we clear
#the cache then. This results in a lazy static site generator
app.config['CACHE_TYPE'] = 'filesystem'
app.config['CACHE_DEFAULT_TIMEOUT'] = 3000000

cache.init_app(app)

app.register_blueprint(main)
app.register_blueprint(blog)
app.register_blueprint(docs)
app.register_blueprint(parts)
app.debug = True

babel = Babel(app,default_domain=translation.messages_domain)

app.jinja_env.filters['markdown_docs'] = cms.markdown_docs
app.jinja_env.filters['markdown_blog'] = cms.markdown_blog
app.jinja_env.globals['gettext_parts'] = translation.gettext_parts
app.jinja_env.globals['gettext_docs'] = translation.gettext_docs

@babel.localeselector
def get_locale():
	lang_code = getattr(g,'lang_code',None)
	if lang_code is None:
		#the four most popular languages from the website
		lang_code = request.accept_languages.best_match(translation.languages)
	return lang_code

@app.route('/')
def index():
	g.lang_code = get_locale()
	return redirect(url_for('main.index',))


if __name__ == "__main__":
		app.run()