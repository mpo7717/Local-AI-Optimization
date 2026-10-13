"""One-shot Google Desktop OAuth bootstrap. No model or WebUI calls.

Credentials and tokens must stay outside Git checkouts. Windows DPAPI protects
the token file for the current Windows user. This does not install a tool.
"""
import argparse
import base64
import ctypes
from ctypes import wintypes
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from pathlib import Path
import secrets
import time
import urllib.parse
import urllib.request
import webbrowser

SCOPES = (
    "https://www.googleapis.com/auth/drive.readonly",
    "https://www.googleapis.com/auth/documents.readonly",
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/presentations.readonly",
)
AUTHORIZE = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN = "https://oauth2.googleapis.com/token"


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *_args, **_kwargs):
        raise ValueError("Token endpoint redirects are forbidden")


def private_path(value):
    path = Path(value).resolve()
    if any((parent / ".git").exists() for parent in (path.parent, *path.parents)):
        raise ValueError("Credential files must be outside Git checkouts")
    return path


def load_client(path):
    path = private_path(path)
    if path.stat().st_size > 65536:
        raise ValueError("Client file exceeds size limit")
    config = json.loads(path.read_text(encoding="utf-8"))
    client = config.get("installed")
    if not isinstance(client, dict):
        raise ValueError("A Google Desktop app client is required")
    if client.get("auth_uri") != AUTHORIZE or client.get("token_uri") != TOKEN:
        raise ValueError("Unexpected OAuth endpoints")
    for field in ("client_id", "client_secret"):
        if not isinstance(client.get(field), str) or not client[field]:
            raise ValueError("Incomplete Desktop client")
    return client


def challenge(verifier):
    return base64.urlsafe_b64encode(hashlib.sha256(verifier.encode("ascii")).digest()).rstrip(b"=").decode("ascii")


def authorization_url(client_id, redirect, state, verifier):
    return AUTHORIZE + "?" + urllib.parse.urlencode({
        "client_id": client_id, "redirect_uri": redirect,
        "response_type": "code", "scope": " ".join(SCOPES),
        "state": state, "code_challenge": challenge(verifier),
        "code_challenge_method": "S256", "access_type": "offline",
        "prompt": "consent", "include_granted_scopes": "false",
    })


def validate_callback(target, state):
    parsed = urllib.parse.urlsplit(target)
    if parsed.path != "/callback" or parsed.fragment or parsed.scheme or parsed.netloc:
        raise ValueError("Invalid callback path")
    values = urllib.parse.parse_qs(parsed.query, keep_blank_values=True)
    if any(len(items) != 1 for items in values.values()):
        raise ValueError("Duplicate callback fields")
    received = values.get("state", [""])[0]
    if not secrets.compare_digest(received, state):
        raise ValueError("Callback state mismatch")
    if "error" in values:
        raise ValueError("Authorization declined")
    code = values.get("code", [""])[0]
    if not code or len(code) > 4096:
        raise ValueError("Missing or oversized authorization code")
    return code


def callback_server(state):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_args):
            pass  # Never log query strings or authorization codes.

        def do_GET(self):
            expected = "127.0.0.1:" + str(self.server.server_port)
            if self.headers.get("Host") != expected or len(self.path) > 8192:
                self.send_error(400, "Invalid request")
                return
            try:
                code = validate_callback(self.path, state)
            except ValueError:
                self.send_response(400)
                message = b"Authorization callback rejected. Return to the local helper."
            else:
                self.server.authorization_code = code
                self.send_response(200)
                message = b"Authorization received. You may close this tab."
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Cache-Control", "no-store")
            self.send_header("Content-Length", str(len(message)))
            self.end_headers()
            self.wfile.write(message)

        def setup(self):
            super().setup()
            self.connection.settimeout(2)

    server = HTTPServer(("127.0.0.1", 0), Handler)
    server.timeout = 1
    server.authorization_code = None
    return server


def validate_token(token):
    if not isinstance(token, dict):
        raise ValueError("Invalid token response")
    if set(str(token.get("scope", "")).split()) != set(SCOPES):
        raise ValueError("Granted scopes differ from approved scopes; do not use this grant")
    if token.get("token_type", "").lower() != "bearer":
        raise ValueError("Unexpected token type")
    for field in ("access_token", "refresh_token"):
        if not isinstance(token.get(field), str) or not token[field]:
            raise ValueError("Missing access or refresh token")
    expires = token.get("expires_in")
    if isinstance(expires, bool) or not isinstance(expires, int) or expires <= 0:
        raise ValueError("Invalid token expiry")
    return token


def protect_windows(payload):
    if os.name != "nt":
        raise RuntimeError("This helper requires Windows DPAPI")

    class Blob(ctypes.Structure):
        _fields_ = [("length", wintypes.DWORD), ("data", ctypes.POINTER(ctypes.c_ubyte))]

    buffer = ctypes.create_string_buffer(payload)
    source = Blob(len(payload), ctypes.cast(buffer, ctypes.POINTER(ctypes.c_ubyte)))
    destination = Blob()
    crypt = ctypes.WinDLL("crypt32", use_last_error=True)
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    crypt.CryptProtectData.argtypes = [ctypes.POINTER(Blob), wintypes.LPCWSTR, ctypes.POINTER(Blob), ctypes.c_void_p, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(Blob)]
    crypt.CryptProtectData.restype = wintypes.BOOL
    kernel.LocalFree.argtypes = [ctypes.c_void_p]
    kernel.LocalFree.restype = ctypes.c_void_p
    if not crypt.CryptProtectData(ctypes.byref(source), "Local AI Admin Google", None, None, None, 1, ctypes.byref(destination)):
        raise RuntimeError("DPAPI protection failed; Windows error " + str(ctypes.get_last_error()))
    try:
        return ctypes.string_at(destination.data, destination.length)
    finally:
        kernel.LocalFree(destination.data)


def save_token(path, token, protector=protect_windows):
    path = private_path(path)
    if path.exists():
        raise ValueError("Token file already exists; refusing to overwrite")
    validate_token(token)
    encrypted = protector(json.dumps(token).encode("utf-8"))
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as output:
        output.write(encrypted)


def run(client_file, token_file):
    if os.name != "nt":
        raise RuntimeError("Windows is required")
    # Fail before consent if this Windows session cannot protect saved tokens.
    protect_windows(b"synthetic-encryption-preflight")
    client = load_client(client_file)
    output = private_path(token_file)
    if output.exists():
        raise ValueError("Token file already exists")
    state, verifier = secrets.token_urlsafe(32), secrets.token_urlsafe(48)
    with callback_server(state) as server:
        redirect = f"http://127.0.0.1:{server.server_port}/callback"
        url = authorization_url(client["client_id"], redirect, state, verifier)
        if not webbrowser.open(url, new=1):
            raise RuntimeError("Could not open the default browser")
        print("Complete Google authorization in your regular browser. No codes are needed here.")
        deadline = time.monotonic() + 180
        while not server.authorization_code and time.monotonic() < deadline:
            server.handle_request()
        if not server.authorization_code:
            raise TimeoutError("Authorization timed out")
        data = urllib.parse.urlencode({
            "client_id": client["client_id"], "client_secret": client["client_secret"],
            "code": server.authorization_code, "code_verifier": verifier,
            "redirect_uri": redirect, "grant_type": "authorization_code",
        }).encode("ascii")
        request = urllib.request.Request(TOKEN, data=data, headers={"Content-Type": "application/x-www-form-urlencoded"})
        opener = urllib.request.build_opener(NoRedirect())
        with opener.open(request, timeout=15) as response:
            payload = response.read(65537)
        if len(payload) > 65536:
            raise ValueError("Token response exceeds size limit")
        token = validate_token(json.loads(payload))
        token["obtained_at"] = int(time.time())
        token["client_id"] = client["client_id"]
        save_token(output, token)
    print("Read-only authorization saved with Windows DPAPI. No provider data was read.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client-file")
    parser.add_argument("--token-file")
    parser.add_argument("--self-test", action="store_true", help="Encrypt synthetic bytes only; no browser, credentials or network")
    args = parser.parse_args()
    try:
        if args.self_test:
            protect_windows(b"synthetic-encryption-preflight")
            print("PASS: Windows DPAPI protected synthetic bytes. No credentials or network used.")
            return 0
        if not args.client_file or not args.token_file:
            parser.error("--client-file and --token-file are required for authorization")
        run(args.client_file, args.token_file)
    except Exception as error:
        # Exception text can contain provider response data, paths, or credentials.
        print("Authorization failed (" + type(error).__name__ + "). No credentials printed. Review/revoke the app grant in Google if needed.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
