from flask import Flask, render_template, make_response

app = Flask(__name__)


# Home page 
@app.route('/')
def home():
    return render_template('home.html')

# Login page 
@app.route('/login')
def login():
    return render_template('login.html')

# Register page 
@app.route('/register')
def register():
    return render_template('register.html')

# If page is not found 
@app.errorhandler(404)
def not_found(error):
    return make_response(render_template('404.html'), 404)
    

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
 
 
 