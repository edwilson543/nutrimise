def test_health_check_returns_status_ok(frontend_api_client):
    response = frontend_api_client.get("/general/health")

    assert response.status_code == 200
