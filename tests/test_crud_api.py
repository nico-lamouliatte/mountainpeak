import random


def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Mountain Peak"}


def test_create_get_peak(test_client, peak_payload):
    response = test_client.post("/peaks", json=peak_payload)
    assert response.status_code == 200
    response_json = response.json()
    created_peak_id = response_json["id"]

    # Get the created peak
    response = test_client.get(f"/peaks/{created_peak_id}")
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["id"] == created_peak_id
    assert response_json["name"] == "Pic du Midi de Bigorre"
    assert response_json["lat"] == 42.936
    assert response_json["lng"] == 0.137
    assert response_json["altitude"] == 2877


def test_create_update_put_peak(test_client, peak_payload, peak_payload_updated):
    response = test_client.post("/peaks", json=peak_payload)
    assert response.status_code == 200
    response_json = response.json()
    created_peak_id = response_json["id"]

    response = test_client.put(f"/peaks/{created_peak_id}", json=peak_payload_updated)
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["name"] == "Pic du Midi de Bigorre after hearthquake"
    assert response_json["lat"] == 43.1
    assert response_json["lng"] == 0.1
    assert response_json["altitude"] == 2650


def test_create_update_patch_peak(test_client, peak_payload, peak_payload_updated):
    response = test_client.post("/peaks", json=peak_payload)
    assert response.status_code == 200
    response_json = response.json()
    created_peak_id = response_json["id"]

    response = test_client.patch(f"/peaks/{created_peak_id}", json={"altitude": 14650})
    response_json = response.json()
    assert response.status_code == 200
    assert response_json["altitude"] == 14650


def test_create_delete_peak(test_client, peak_payload):
    response = test_client.post("/peaks", json=peak_payload)
    assert response.status_code == 200
    response_json = response.json()
    created_peak_id = response_json["id"]

    # Delete the created peak
    response = test_client.delete(f"/peaks/{created_peak_id}")
    assert response.status_code == 204

    # Get the deleted peak
    response = test_client.get(f"/peaks/{created_peak_id}")
    assert response.status_code == 404


def test_get_non_existant_peak(test_client):
    response = test_client.get(f"/peaks/{int(random.random()*100000)}")
    assert response.status_code == 404


def test_create_peak_wrong_payload(test_client):
    response = test_client.post("/peaks/", json={})
    assert response.status_code == 422
