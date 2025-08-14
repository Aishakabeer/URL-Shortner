from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, URLMap
from forms import URLForm
import string, random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///url_shortener.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db.init_app(app)

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.before_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    form = URLForm()
    if form.validate_on_submit():
        long_url = form.url.data
        # Check if URL already exists
        existing = URLMap.query.filter_by(long_url=long_url).first()
        if existing:
            short_code = existing.short_code
        else:
            short_code = generate_short_code()
            # Ensure unique short_code
            while URLMap.query.filter_by(short_code=short_code).first():
                short_code = generate_short_code()
            url_map = URLMap(long_url=long_url, short_code=short_code)
            db.session.add(url_map)
            db.session.commit()
        short_url = url_for('redirect_short_url', short_code=short_code, _external=True)
        session['short_url'] = short_url
        session['long_url'] = long_url
        return redirect(url_for('result'))
    return render_template('index.html', form=form)

@app.route('/result')
def result():
    short_url = session.get('short_url')
    long_url = session.get('long_url')
    if not short_url:
        return redirect(url_for('index'))
    return render_template('result.html', short_url=short_url, long_url=long_url)

@app.route('/<short_code>')
def redirect_short_url(short_code):
    url_map = URLMap.query.filter_by(short_code=short_code).first()
    if url_map:
        return redirect(url_map.long_url)
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)