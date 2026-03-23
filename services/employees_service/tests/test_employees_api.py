def auth_headers(token: str = "fake-token"):
    return {"Authorization": f"Bearer {token}"}


def test_list_employees_as_admin_returns_200(client, mock_admin):
    response = client.get(
        "/api/employees_info",
        headers=auth_headers(),
    )

    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert "meta" in body
    assert body["meta"]["total_count"] == 0


def test_list_employees_as_observer_returns_200(client, mock_observer):
    response = client.get(
        "/api/employees_info",
        headers=auth_headers(),
    )

    assert response.status_code == 200
    body = response.json()
    assert "data" in body
    assert body["meta"]["total_count"] == 0


def test_list_employees_as_participant_returns_403(client, mock_participant):
    response = client.get(
        "/api/employees_info",
        headers=auth_headers(),
    )

    assert response.status_code == 403
    body = response.json()
    assert body["detail"]["error"] == "Forbidden"


def test_get_employee_not_found_returns_404(client, mock_admin):
    response = client.get(
        "/api/employees_info/999",
        headers=auth_headers(),
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Employee not found"


def test_create_employee_as_admin_returns_201(client, mock_admin):
    payload = {
        "name": "Иван Иванов",
        "email": "ivan@corp.example",
        "city": "Москва",
        "position": "QA Engineer",
        "company": "LiderPro",
        "department": "QA",
    }

    response = client.post(
        "/api/employees_info",
        json=payload,
        headers=auth_headers(),
    )

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Иван Иванов"
    assert body["email"] == "ivan@corp.example"
    assert body["city"] == "Москва"
    assert body["total_points"] == 0


def test_create_employee_with_invalid_email_returns_422(client, mock_admin):
    payload = {
        "name": "Иван Иванов",
        "email": "not-an-email",
        "city": "Москва",
    }

    response = client.post(
        "/api/employees_info",
        json=payload,
        headers=auth_headers(),
    )

    assert response.status_code == 422


def test_delete_employee_as_observer_returns_403(client, mock_observer):
    response = client.delete(
        "/api/employees_info/1",
        headers=auth_headers(),
    )

    assert response.status_code == 403
    body = response.json()
    assert body["detail"]["error"] == "Forbidden"
