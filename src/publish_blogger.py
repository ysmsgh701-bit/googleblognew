# Publish a markdown post to Blogger via Blogger API v3.
# Usage: py -3.11 src/publish_blogger.py <path-to-markdown> [--draft]
#
# One-time setup: place an OAuth client file at config/credentials/client_secret.json
# (Google Cloud Console > APIs & Services > Credentials > OAuth client ID, type "Desktop app",
#  with Blogger API v3 enabled). First run opens a browser for consent and caches token.json.

import json
import re
import sys
from pathlib import Path

import markdown
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

ROOT = Path(__file__).resolve().parent.parent
SETTINGS_PATH = ROOT / "config" / "settings.json"
SCOPES = ["https://www.googleapis.com/auth/blogger"]


def load_settings():
    return json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))


def save_settings(settings):
    SETTINGS_PATH.write_text(
        json.dumps(settings, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def get_credentials(settings):
    token_path = ROOT / settings["credentials"]["token"]
    secret_path = ROOT / settings["credentials"]["client_secret"]
    creds = None
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not secret_path.exists():
                sys.exit(
                    f"ERROR: OAuth client file not found: {secret_path}\n"
                    "Create a Desktop-app OAuth client in Google Cloud Console "
                    "(Blogger API v3 enabled) and save it to that path."
                )
            flow = InstalledAppFlow.from_client_secrets_file(str(secret_path), SCOPES)
            creds = flow.run_local_server(port=0)
        token_path.parent.mkdir(parents=True, exist_ok=True)
        token_path.write_text(creds.to_json(), encoding="utf-8")
    return creds


def parse_front_matter(text):
    # Minimal YAML front matter parser (title / labels / etc. as flat keys).
    meta = {}
    body = text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n", text, re.DOTALL)
    if m:
        body = text[m.end():]
        for line in m.group(1).splitlines():
            if ":" not in line:
                continue
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip().strip("\"'")
    return meta, body


def to_labels(meta):
    raw = meta.get("labels", "")
    raw = raw.strip("[]")
    return [x.strip().strip("\"'") for x in raw.split(",") if x.strip()]


def main():
    # Windows console defaults to cp949; force UTF-8 so Korean/em-dash output works.
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        sys.exit("Usage: py -3.11 src/publish_blogger.py <markdown-file> [--draft]")
    md_path = Path(sys.argv[1])
    as_draft = "--draft" in sys.argv[2:]

    settings = load_settings()
    creds = get_credentials(settings)
    service = build("blogger", "v3", credentials=creds)

    blog_id = settings.get("blog_id")
    if not blog_id:
        blog = service.blogs().getByUrl(url=settings["blog_url"]).execute()
        blog_id = blog["id"]
        settings["blog_id"] = blog_id
        save_settings(settings)

    text = md_path.read_text(encoding="utf-8")
    meta, body = parse_front_matter(text)
    title = meta.get("title") or md_path.stem
    html = markdown.markdown(body, extensions=["tables", "fenced_code"])

    post_body = {"title": title, "content": html}
    labels = to_labels(meta)
    if labels:
        post_body["labels"] = labels

    post = (
        service.posts()
        .insert(blogId=blog_id, body=post_body, isDraft=as_draft)
        .execute()
    )
    print(json.dumps(
        {"status": post.get("status", "LIVE" if not as_draft else "DRAFT"),
         "url": post.get("url"), "postId": post.get("id"), "title": title},
        ensure_ascii=False,
    ))


if __name__ == "__main__":
    main()
