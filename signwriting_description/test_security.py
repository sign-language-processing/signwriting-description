import os
from unittest.mock import patch

from fastapi.testclient import TestClient

with patch.dict(os.environ, {"OPENAI_API_KEY": "test-no-network"}):
    from signwriting_description.server import app


def test_oversized_fsw_does_not_call_paid_upstream():
    with patch("signwriting_description.server.describe_sign") as describe:
        response = TestClient(app).get("/", params={"fsw": "a" * 8193})
    assert response.status_code == 422
    describe.assert_not_called()
