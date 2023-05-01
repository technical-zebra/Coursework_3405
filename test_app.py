from flask import Flask
from QuizPod.Facade import create_app, socketio
import pytest

app = create_app(debug=True)


@pytest.fixture
def client():
    """
    This function creates a test client for a Flask application.
    """
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_home_page(client):
    """
    This function tests the home page of a website by checking if the response status code is 200 and if
    the response data contains the string "Welcome to QuizPod".
    
    :param client: The client is an object that allows us to simulate HTTP requests to our Flask
    application. 
    """
    response = client.get('/')

    assert response.status_code == 200

    assert b"Welcome to QuizPod" in response.data


def test_login(client):
    """
    This function tests the login functionality of a web application by sending a POST request with a
    username and password and checking if the response contains certain strings.
    
    :param client: The client is an instance of the Flask test client, which is used to simulate
    requests to the Flask application during testing. 
    """
    response = client.post('/login', data=dict(username='testuser', password='password'), follow_redirects=True)

    assert response.status_code == 200

    assert b"Logged in successfully" in response.data
    assert b"Welcome, testuser" in response.data


def test_invalid_login(client):
    """
    This function tests for an invalid login attempt by sending a POST request to the '/login' endpoint
    with incorrect login credentials and checking if the response contains the message "Invalid username
    or password".
    
    :param client: The client is an instance of the Flask test client, which is used to simulate
    requests to the Flask application during testing.
    """
    response = client.post('/login', data=dict(username='testuser', password='wrongpassword'), follow_redirects=True)

    assert response.status_code == 200

    assert b"Invalid username or password" in response.data



if __name__ == '__main__':
    socketio.run(app)
    pytest.main()
