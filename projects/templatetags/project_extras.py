import re

from django import template

register = template.Library()

# Matches youtu.be/<id>, youtube.com/watch?v=<id>, youtube.com/shorts/<id>
YOUTUBE_PATTERNS = [
    r"(?:youtube\.com\/watch\?v=)([\w-]{11})",
    r"(?:youtu\.be\/)([\w-]{11})",
    r"(?:youtube\.com\/shorts\/)([\w-]{11})",
]
VIMEO_PATTERN = r"(?:vimeo\.com\/)(\d+)"


@register.filter
def embed_url(url):
    """
    Normalize a pasted YouTube/Vimeo link into an <iframe>-safe embed URL.

    Watch-page URLs (youtube.com/watch?v=..., youtu.be/...) send
    X-Frame-Options headers that block them from rendering inside an
    iframe — only the /embed/ path is embeddable. This filter converts
    whatever format was pasted into the admin into the correct one,
    and leaves already-correct embed URLs untouched.
    """
    if not url:
        return ""

    for pattern in YOUTUBE_PATTERNS:
        match = re.search(pattern, url)
        if match:
            return f"https://www.youtube.com/embed/{match.group(1)}"

    match = re.search(VIMEO_PATTERN, url)
    if match:
        return f"https://player.vimeo.com/video/{match.group(1)}"

    # Already an embed URL (or an unrecognized host) — pass through as-is.
    return url