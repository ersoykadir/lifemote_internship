"""
Kadir Ersoy
Internship Project
Utils for tests
"""
def check_response_validity(response, expected_result, expected_status_code):
    """ Check the validity of the response"""
    # Check the response status code
    assert response.status_code == expected_status_code

    if expected_status_code == 200:
        # Parse the JSON response and check the expected result
        data = response.json()
        assert data == expected_result
    elif expected_status_code == 400:
        # Parse the JSON error response
        error_data = response.json()
        assert error_data.get("detail") == expected_result
    elif expected_status_code == 422:
        # Parse the JSON error response
        error_data = response.json()
        assert error_data.get("detail")[0].get("msg") == expected_result
