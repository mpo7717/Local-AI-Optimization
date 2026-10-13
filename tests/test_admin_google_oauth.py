import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import urllib.parse

SPEC = importlib.util.spec_from_file_location("admin_google_oauth", Path(__file__).parents[1] / "tools" / "admin_google_oauth.py")
oauth = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(oauth)


def fixture_token():
    return {"access_token": "synthetic-access", "refresh_token": "synthetic-refresh", "token_type": "Bearer", "expires_in": 3600, "scope": " ".join(oauth.SCOPES)}


class OAuthPreparationTests(unittest.TestCase):
    def test_pkce_known_vector(self):
        self.assertEqual(oauth.challenge("dBjftJeZ4CVP-mB92K27uhbUJU1p1r_wW1gFWFOEjXk"), "E9Melhoa2OwvFrEMTJguCHaoeK1t8URWbuGJSstw-cM")

    def test_authorization_exact_scopes_and_pkce(self):
        url = oauth.authorization_url("synthetic", "http://127.0.0.1:1234/callback", "state", "verifier")
        params = urllib.parse.parse_qs(urllib.parse.urlsplit(url).query)
        self.assertEqual(params["scope"], [" ".join(oauth.SCOPES)])
        self.assertEqual(params["include_granted_scopes"], ["false"])
        self.assertEqual(params["code_challenge_method"], ["S256"])
        self.assertEqual(params["access_type"], ["offline"])

    def test_callback_requires_state_and_single_fields(self):
        self.assertEqual(oauth.validate_callback("/callback?state=expected&code=synthetic", "expected"), "synthetic")
        for target in ("/callback?state=wrong&code=x", "/callback?state=expected&code=x&code=y", "/other?state=expected&code=x", "/callback?state=expected&error=access_denied", "http://evil.invalid/callback?state=expected&code=x"):
            with self.subTest(target=target), self.assertRaises(ValueError):
                oauth.validate_callback(target, "expected")

    def test_grants_fail_closed(self):
        for change in ({"scope": " ".join(oauth.SCOPES) + " https://www.googleapis.com/auth/drive"}, {"scope": oauth.SCOPES[0]}, {"refresh_token": ""}, {"token_type": "Basic"}, {"expires_in": True}):
            with self.subTest(change=change), self.assertRaises(ValueError):
                oauth.validate_token({**fixture_token(), **change})

    def test_repo_credentials_rejected(self):
        with tempfile.TemporaryDirectory() as root:
            (Path(root) / ".git").mkdir()
            with self.assertRaises(ValueError):
                oauth.private_path(Path(root) / "private" / "client.json")

    def test_only_desktop_google_client(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "client.json"
            client = {"client_id": "synthetic", "client_secret": "synthetic", "auth_uri": oauth.AUTHORIZE, "token_uri": oauth.TOKEN}
            path.write_text(json.dumps({"installed": client}))
            self.assertEqual(oauth.load_client(path), client)
            for config in ({"web": client}, {"installed": {**client, "token_uri": "https://evil.invalid"}}):
                path.write_text(json.dumps(config))
                with self.assertRaises(ValueError):
                    oauth.load_client(path)

    def test_store_protects_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "grant.dpapi"
            oauth.save_token(path, fixture_token(), protector=lambda _payload: b"protected-fixture")
            self.assertEqual(path.read_bytes(), b"protected-fixture")
            with self.assertRaises(ValueError):
                oauth.save_token(path, fixture_token(), protector=lambda _payload: b"replacement")

    def test_protection_failure_creates_no_token(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "grant.dpapi"
            def fail(_payload):
                raise RuntimeError("synthetic protection failure")
            with self.assertRaises(RuntimeError):
                oauth.save_token(path, fixture_token(), protector=fail)
            self.assertFalse(path.exists())

    def test_token_redirect_rejected(self):
        with self.assertRaises(ValueError):
            oauth.NoRedirect().redirect_request(None, None, 302, "", {}, "https://evil.invalid")

    @unittest.skipUnless(os.name == "nt", "Windows bootstrap")
    def test_encryption_failure_precedes_credentials_and_browser(self):
        with patch.object(oauth, "protect_windows", side_effect=RuntimeError("synthetic")), patch.object(oauth, "load_client") as load, patch.object(oauth.webbrowser, "open") as browser:
            with self.assertRaises(RuntimeError):
                oauth.run("unused-client", "unused-token")
            load.assert_not_called()
            browser.assert_not_called()

    @unittest.skipUnless(os.name == "nt", "Windows DPAPI")
    def test_real_dpapi_encrypts_synthetic_only(self):
        data = b"synthetic-no-credentials"
        protected = oauth.protect_windows(data)
        self.assertGreater(len(protected), len(data))
        self.assertNotIn(data, protected)


if __name__ == "__main__":
    unittest.main()
