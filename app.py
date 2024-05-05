from flask import Flask, jsonify, redirect, request
import hashlib
import random
import string

app = Flask(__name__)

# Dictionary to store custom short URLs
custom_short_links = {}

def generate_short_link(url):
    """Generate a short link using the MD5 hash of the original URL."""
    hash_object = hashlib.md5(url.encode())
    return hash_object.hexdigest()[:8]

def generate_random_string(length):
    """Generate a random string of a given length."""
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for i in range(length))

@app.route('/shorten/<custom_name>/<path:original_url>')
def shorten_url(custom_name, original_url):
    """Shorten a URL with a custom name."""
    if not original_url.startswith('http'):
        original_url = 'http://' + original_url

    if custom_name in custom_short_links:
        return jsonify({'error': 'Custom name already in use'}), 400

    short_link = custom_name
    custom_short_links[short_link] = original_url

    return jsonify({'shortened_url': f'http://{request.host}/{short_link}'})

@app.route('/shorten_auto/<path:original_url>')
def shorten_auto_url(original_url):
    """Shorten a URL automatically."""
    if not original_url.startswith('http'):
        original_url = 'http://' + original_url

    short_link = generate_random_string(8)
    while short_link in custom_short_links:
        short_link = generate_random_string(8)

    custom_short_links[short_link] = original_url

    return jsonify({'shortened_url': f'http://{request.host}/{short_link}'})

@app.route('/<short_link>')
def redirect_to_original(short_link):
    """Redirect to the original URL when given the short link."""
    original_url = custom_short_links.get(short_link)
    if original_url:
        return redirect(original_url)
    else:
        return jsonify({'error': 'Shortened URL not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
