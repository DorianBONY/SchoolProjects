from bs4 import BeautifulSoup

from website.models import User


def test_home(client):
    client.post("/sign-up", data={"firstName": "test", "email": "test@test.com", "password1": "test123", "password2": "test123"})
    client.post("/login", data={"email": "test@test.com", "password": "test123"})

    response = client.get("/")
    assert b"<title>Home</title>" in response.data


def test_prediction(client):
    response = client.post("/prediction", data={"siren": "123456789"})
    soup = BeautifulSoup(response.data, 'html.parser')
    div = soup.find('div', class_='alert alert-success alert-dismissable fade show')
    contenu_div = div.text.strip()

    assert "Ce siren n\'existe pas en base" in contenu_div.strip()


def test_registration(client, app):
    response = client.post("/sign-up",
                           data={"firstName": "Dodododo", "email": "test@test.com", "password1": "testpassword",
                                 "password2": "testpassword"})

    with app.app_context():
        assert User.query.count() == 1
        assert User.query.first().email == "test@test.com"
