from unittest import TestCase
from fastapi import HTTPException
from fastapi.testclient import TestClient
from pytest import mark
from parameterized import parameterized

from app.main import app as web_app
from .data import get_test_data


# get the test datasets
right_signature_data_list, wrong_signature_data_list = get_test_data()


class APITestCase(TestCase):
    def setUp(self) -> None:
        self.client = TestClient(web_app)

    @mark.get
    def test_request_with_wrong_path_parameter(self) -> None:
        """
        Test for a request to a non-existent endpoint.
        """
        response = self.client.get("/")
        self.assertEqual(
            response.status_code,
            404,
            "Redirects to an Existing Page")

    @mark.post
    @parameterized.expand(right_signature_data_list)
    def test_posts_with_right_signatures(
        self, json_data, app_id, account_id, session_id, signature
    ) -> None:
        """
        Test POST request with the correct signature.

        Args:
            json_data (dict): request body.
            app_id (str): application ID.
            account_id (str): account ID.
            session_id (str): session ID.
            signature (str): signature.
        """
        response = self.client.post(
            f"/server_event/?appId={app_id}"
            f"&accountId={account_id}"
            f"&sessionId={session_id if session_id else 'undefined'}"
            f"&signature={signature}",
            json=json_data,
        )
        self.assertEqual(
            response.text,
            '{"status":"Event Successfully Sent"}',
            "Event Was Not Sent"
        )
        self.assertEqual(response.status_code, 200, "Incorrect Status Code")

    @mark.post
    @parameterized.expand(wrong_signature_data_list)
    def test_posts_with_wrong_signatures(
        self, json_data, app_id, account_id, session_id, signature
    ) -> None:
        """
        Test POST request with the incorrect signature.

        Args:
            json_data (dict): request body.
            app_id (str): application ID.
            account_id (str): account ID.
            session_id (str): session ID.
            signature (str): signature.
        """
        response = self.client.post(
            f"/server_event/?appId={app_id}"
            f"&accountId={account_id}"
            f"&sessionId={session_id if session_id else 'undefined'}"
            f"&signature={signature}",
            json=json_data
        )
        self.assertEqual(
            response.text,
            '{"detail":"Signatures didn\'t Match"}', "Event Was Sent"
        )
        self.assertEqual(response.status_code, 403, "Incorrect Status Code")
        self.assertRaises(HTTPException)
