from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
import requests

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'your_secret_key_here'  # Replace with a strong secret key!

# MySQL connection (make sure XAMPP's MySQL is running)
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Leave blank if no root password is set
        database="animesan"
    )

# Mock YouTube API search
def mock_Youtube(query):
    if "bleach" in query.lower():
        return [
            {"title": "Bleach: Thousand-Year Blood War Official Trailer", "channel_name": "VIZ Media",
             "url": "https://www.youtube.com/watch?v=some_bleach_id", "view_count": 1000000},
            {"title": "Bleach Opening 1", "channel_name": "Anime Music",
             "url": "https://www.youtube.com/watch?v=some_opening_id", "view_count": 500000}
        ]
    elif "hunter x hunter" in query.lower():
        return [
            {"title": "Hunter X Hunter Best Moments", "channel_name": "Anime Central",
             "url": "https://www.youtube.com/watch?v=some_hxh_id", "view_count": 750000}
        ]
    else:
        return [
            {"title": f"Search result for {query} 1", "channel_name": "General Anime",
             "url": "https://www.youtube.com/watch?v=generic_id_1", "view_count": 10000},
            {"title": f"Search result for {query} 2", "channel_name": "Anime Hub",
             "url": "https://www.youtube.com/watch?v=generic_id_2", "view_count": 5000}
        ]

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, password FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (name, username, email, password) VALUES (%s, %s, %s, %s)",
                (name, username, email, hashed_password)
            )
            conn.commit()
            flash('Account created! Please login.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            flash('Email or username already exists.', 'danger')
        finally:
            cursor.close()
            conn.close()
    return render_template('signup.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access the dashboard.', 'info')
        return redirect(url_for('login'))

    return render_template('dashboard.html', session=session)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))

@app.route('/api/Youtube', methods=['POST'])
def Youtube_api():
    data = request.get_json()
    search_query = data.get('searchQuery')

    if not search_query:
        return jsonify({'error': 'Search query is missing'}), 400

    try:
        formatted_results = mock_Youtube(search_query)
        return jsonify({'results': formatted_results})
    except Exception as e:
        print(f"Error during YouTube API search: {e}")
        return jsonify({'error': str(e), 'message': 'An error occurred during search.'}), 500

@app.route('/anime')
def home():
    return render_template('home.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query', '').strip()
    results = []
    error = None

    if query:
        url = f"https://api.jikan.moe/v4/anime?q={query}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            results = data.get('data', [])
        except requests.exceptions.RequestException as req_err:
            error = f"Request error: {req_err}"
        except Exception as e:
            error = f"An error occurred: {e}"
    else:
        error = "Please enter a search term."

    return render_template('results.html', query=query, results=results, error=error)

if __name__ == '__main__':
    app.run(debug=True)