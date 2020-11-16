import json

import pytest

import main


@pytest.fixture
def client():
    main.app.config['TESTING'] = True
    return main.app.test_client()


class TestClass:
    def test_success(self, client):
        """Testing successful load and get."""

        response = client.post('/load', json=[
            "foobar", "aabb", "baba", "boofAr", "test",
        ])

        assert response.status_code == 200

        response = client.get('/get', query_string={'word': 'raboof'})
        assert response.status_code == 200
        response_data = response.get_data()

        assert json.loads(response_data) == ["foobar", "boofAr"]

        response = client.get('/get', query_string={'word': 'ghoti'})
        assert response.status_code == 200
        response_data = response.get_data()

        assert json.loads(response_data) is None

    def test_load_fail(self, client):
        """Testing unsuccessful load."""

        response = client.post('/load', json=[
            "foobar", "aabb", 2, "boofAr", "test",
        ])
        assert response.status_code == 400

        response = client.post('/load')
        assert response.status_code == 400

        response = client.post('/load', json={})
        assert response.status_code == 400

    def test_get_fail(self, client):
        """Testing unsuccessful get."""
        response = client.get('/get')
        assert response.status_code == 400

