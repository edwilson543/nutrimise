def test_health_check_returns_status_ok(frontend_api_client):
    response = frontend_api_client.get("/general/version")

    assert response.status_code == 200
    assert response.json()["version"] == "0"
