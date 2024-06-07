import pytest
from flask import session
from urllib.parse import urlencode

# Test the login route
def test_login_get(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Login" in response.data  # Assuming 'Login' text is in the login page

def test_login_post(client):
    response = client.post('/', follow_redirects=False)
    assert response.status_code == 302  # Check if it redirects
    assert 'location' in response.headers
    assert response.headers['location'].startswith('http')  # Ensure it's an external URL

# Test the home route
def test_home_redirect(client):
    response = client.get('/home', follow_redirects=True)
    assert response.status_code == 200
    assert b"Login" in response.data  # Should redirect to login if not logged in

# Test adding a customer
def test_add_customer_get(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id_token': 'test_token'}
    
    response = client.get('/add_customer')
    assert response.status_code == 200

def test_add_customer_post(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id_token': 'test_token'}
    
    data = {
        'name': '<script>alert("XSS")</script>',
        'code': '<b>code</b>',
        'phone': '<img src=x onerror=alert(1)>'
    }
    response = client.post('/add_customer', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'alert("XSS")' not in response.data
    assert b'<b>code</b>' not in response.data
    assert b'<img src=x onerror=alert(1)>' not in response.data

# Test adding an order
def test_add_order_get(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id_token': 'test_token'}
    
    response = client.get('/add_order')
    assert response.status_code == 200

def test_add_order_post(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id_token': 'test_token'}
    
    data = {
        'customer_id': '1',
        'item': '<script>alert("XSS")</script>',
        'amount': '<img src=x onerror=alert(1)>'
    }
    response = client.post('/add_order', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'alert("XSS")' not in response.data
    assert b'<img src=x onerror=alert(1)>' not in response.data

# Test logout
def test_logout(client):
    with client.session_transaction() as sess:
        sess['user'] = {'id_token': 'test_token'}
    
    response = client.get('/logout', follow_redirects=False)
    assert response.status_code == 302  # Check if it redirects
    assert 'location' in response.headers
    assert response.headers['location'].startswith('http')  # Ensure it's an external URL
