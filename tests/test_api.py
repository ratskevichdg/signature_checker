from unittest import TestCase
from fastapi.testclient import TestClient
from pytest import mark
from parameterized import parameterized


from app.main import app as web_app
from .data import get_test_data


right_data_list, wrong_signature_data_list = get_test_data()

class APITestCase(TestCase):

    def setUp(self) -> None:
        self.client = TestClient(web_app)

    @mark.get
    def test_request_with_wrong_path_parameter(self) -> None:
        response = self.client.get(f"/12")
        self.assertEqual(response.status_code, 404, "Redirects to an Existing Page")
    

    @mark.post
    @parameterized.expand(right_data_list)
    def test_post_right_signatures(self, json_data, app_id, account_id, session_id, signature) -> None:
        response = self.client.post(
            f"/server_event/?appId={app_id}&accountId={account_id}&sessionId={session_id if session_id else 'undefined'}&signature={signature}",
            json=json_data
        )
        assert response.text == '{"status":"Event Successfully Sent"}', "Event Was Not Sent"

    @mark.post
    @parameterized.expand(wrong_signature_data_list)
    def test_post_wrong_signatures(self, json_data, app_id, account_id, session_id, signature) -> None:
        response = self.client.post(
            f"/server_event/?appId={app_id}&accountId={account_id}&sessionId={session_id if session_id else 'undefined'}&signature={signature}",
            json=json_data
        )
        assert response.text == '{"detail":"Signatures didn\'t Match"}', "Event Was Sent"
