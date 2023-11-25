import httpx
import pytest
from fastapi.testclient import TestClient
from httpx import Response
from gateway.main import app


# Fixture for TestClient
@pytest.fixture()
def client():
    return TestClient(app)


# Fixture to mock AsyncClient
@pytest.fixture()
def mock_async_client_post(mocker):
    mock = mocker.patch('httpx.AsyncClient.post')
    yield mock
    mock.stop()


def test_root_endpoint(client):
    """
    Test the root endpoint of the gateway service.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Gateway Service is active"}


@pytest.mark.parametrize(
    "test_input,expected_status,expected_response",
    [
        ({"username": "test", "password": "test"}, 200, {"token": "testtoken"}),
        ({"username": "wrong", "password": "credentials"}, 503, {"detail": "Auth service is unavailable"}),
    ],
)
def test_auth_login(client, mock_async_client_post, test_input, expected_status, expected_response):
    if test_input["username"] == "test":
        mock_async_client_post.return_value = Response(200, json={"token": "testtoken"})
    else:
        mock_async_client_post.side_effect = httpx.RequestError("Auth service unavailable")

    response = client.post("/auth/login", json=test_input)
    assert response.status_code == expected_status
    assert response.json() == expected_response
