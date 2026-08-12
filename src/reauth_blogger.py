# Re-authenticate the Blogger OAuth token without publishing anything.
# Usage: py -3.11 src/reauth_blogger.py
#
# Why this exists: publish_blogger.py only refreshes credentials as a side effect of
# publishing a post, so there is no way to restore a dead token ahead of time. The
# refresh token expires every 7 days while the Google Cloud consent screen stays in
# "Testing" mode, which has blocked the nightly pipeline repeatedly. Run this from an
# interactive desktop session (it opens a browser); headless runs cannot consent.

import json
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parent.parent
SETTINGS_PATH = ROOT / "config" / "settings.json"
SCOPES = ["https://www.googleapis.com/auth/blogger"]


def main():
    settings = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
    token_path = ROOT / settings["credentials"]["token"]
    secret_path = ROOT / settings["credentials"]["client_secret"]

    if not secret_path.exists():
        sys.exit(f"ERROR: OAuth client file not found: {secret_path}")

    creds = None
    if token_path.exists():
        try:
            creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
        except ValueError:
            creds = None

    # Try a silent refresh first; fall back to browser consent.
    if creds and creds.valid:
        print("Token is already valid. No re-authentication needed.")
    else:
        refreshed = False
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                refreshed = True
                print("Refreshed the existing token silently.")
            except Exception as exc:
                print(f"Silent refresh failed ({type(exc).__name__}). Opening browser consent...")
        if not refreshed and not (creds and creds.valid):
            # Keep the dead token so the failure history stays inspectable.
            if token_path.exists():
                backup = token_path.with_suffix(f".json.expired-{__import__('datetime').date.today()}")
                if not backup.exists():
                    backup.write_text(token_path.read_text(encoding="utf-8"), encoding="utf-8")
                    print(f"Backed up the dead token to {backup.name}")
            flow = InstalledAppFlow.from_client_secrets_file(str(secret_path), SCOPES)
            creds = flow.run_local_server(port=0)
        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(creds.to_json(), encoding="utf-8")
        print(f"Saved credentials to {token_path}")

    # Prove the credentials actually work against the target blog.
    blog = build("blogger", "v3", credentials=creds).blogs().get(
        blogId=settings["blog_id"]
    ).execute()
    print(f"OK: {blog['name']} — {blog['posts']['totalItems']} posts, {blog['url']}")


if __name__ == "__main__":
    main()
