#!/usr/bin/env python3
"""
Google Play readiness for the app pages.

Adds to every /apps/<slug>/ page (and the /apps/ index):
  * a "Permissions & data" section that lists, in plain words, the Android
    permissions that app actually declares and why it needs them
  * a line naming UTILITYNEST as the publisher, with links to the app privacy
    policy, the data-deletion page and About & Contact

The permission lists below were read from each app's AndroidManifest.xml.
Keep them in sync if an app starts asking for something new.

Idempotent: pages that already link the app privacy policy are skipped.

Usage:  python3 tools/app_playstore_pages.py [repo_root]
"""
import os
import sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")

APPS = {
    "neon-calculator": [
        "Internet and network state \u2014 only to check whether a connection exists. The app works fully offline.",
    ],
    "neon-piano": [
        "No permissions at all. The app runs entirely offline.",
    ],
    "car-simulator": [
        "No permissions at all. The game runs entirely offline.",
    ],
    "grabit": [
        "Internet and network state \u2014 to load the pages and files you ask it to download.",
        "Storage / all-files access \u2014 to save downloads to the folder you choose and to show your own media in the cleaner. It only reads the files needed for the action you start.",
        "Foreground service and wake lock \u2014 to keep a download running while the screen is off, with a visible notification.",
        "Notifications \u2014 to show download progress and completion.",
    ],
    "soulstream": [
        "Internet and network state \u2014 to play and fetch the media you request.",
        "Storage / all-files access \u2014 to list and play your own media files and save downloads.",
        "Foreground service and wake lock \u2014 so playback or a transfer continues in the background with a visible notification.",
        "Notifications \u2014 for playback and transfer status.",
    ],
    "pulsechat": [
        "Microphone and audio settings \u2014 to record voice messages and make voice calls, only when you tap the microphone or call button.",
        "Camera \u2014 to take a photo or scan a code, only when you open the camera from inside the app.",
        "Bluetooth \u2014 to find and connect to nearby devices for chat and calling.",
        "Internet, network state and notifications \u2014 to deliver messages and notify you of new ones.",
    ],
    "twinspace": [
        "Package visibility \u2014 the app must be able to see which apps are installed so it can create and launch a second copy of the app you pick. Your app list is never sent anywhere.",
        "Device administrator \u2014 used only for the optional protection feature that stops the second space being uninstalled by someone else. You enable it yourself and can switch it off in Settings \u2192 Security \u2192 Device admin apps.",
    ],
    "voltaura": [
        "Notification access \u2014 to read notification content so the app can show your alerts in its own dashboard. That data stays on your device.",
        "Display over other apps \u2014 to show its overlay and dashboard on top of other apps.",
        "Foreground service and notifications \u2014 to keep the dashboard running with a visible notification.",
    ],
}

PUBLISHER_LINE = (
    '<p><strong>Published by UTILITYNEST</strong> (registered MSME / Udyam, Govt. of India), '
    'the company behind Digitalaikart. '
    '<a href="/app-privacy-policy.html">App privacy policy</a> \u00b7 '
    '<a href="/account-deletion.html">Delete your data</a> \u00b7 '
    '<a href="/about.html">About &amp; Contact</a></p>'
)

PRIVACY_NOTE = (
    '<p>This app does not create an account for you, does not include advertising or '
    'analytics SDKs, and does not send your personal data to our servers. Every permission is '
    'optional and can be revoked in Android Settings at any time.</p>'
)


def section(items):
    lis = "".join("<li>%s</li>" % i for i in items)
    return (
        '<section class="section"><h2 class="section-title">Permissions &amp; data</h2>'
        '<div class="gold-divider"></div>'
        '<div style="max-width:720px;margin:0 auto;color:var(--text-secondary);font-size:.85rem">'
        + PRIVACY_NOTE + "<ul>" + lis + "</ul>" + PUBLISHER_LINE + "</div></section>"
    )


def read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def main():
    changed = []

    for slug, items in APPS.items():
        page = os.path.join(ROOT, "apps", slug, "index.html")
        t = read(page)
        if not t or "/app-privacy-policy.html" in t or "<footer" not in t:
            continue
        t = t.replace("<footer", section(items) + "<footer", 1)
        write(page, t)
        changed.append("apps/%s/" % slug)

    index = os.path.join(ROOT, "apps", "index.html")
    t = read(index)
    if t and "/app-privacy-policy.html" not in t and "<footer" in t:
        block = (
            '<section class="section"><div style="max-width:720px;margin:0 auto;'
            'color:var(--text-secondary);font-size:.85rem">'
            '<h2 class="section-title">Apps, data and privacy</h2><div class="gold-divider"></div>'
            '<p>Every app here is published by <strong>UTILITYNEST</strong> (registered '
            'MSME / Udyam, Govt. of India), the company behind Digitalaikart. None of the apps '
            'needs an account, none shows advertising, and none sends your personal data to our '
            'servers. Each app page lists the Android permissions it asks for and why.</p>'
            '<p><a href="/app-privacy-policy.html">App privacy policy</a> \u00b7 '
            '<a href="/account-deletion.html">Delete your data</a> \u00b7 '
            '<a href="/about.html">About &amp; Contact</a></p></div></section>'
        )
        t = t.replace("<footer", block + "<footer", 1)
        write(index, t)
        changed.append("apps/index.html")

    # let the help bot know about the two new pages
    kb = os.path.join(ROOT, "tools", "build_site_knowledge.py")
    t = read(kb)
    if t and '"/account-deletion.html"' not in t and '("/about.html", "about.html"),' in t:
        t = t.replace(
            '("/about.html", "about.html"),',
            '("/about.html", "about.html"),\n'
            '        ("/app-privacy-policy.html", "app-privacy-policy.html"),\n'
            '        ("/account-deletion.html", "account-deletion.html"),',
            1,
        )
        write(kb, t)
        changed.append("tools/build_site_knowledge.py")

    print("updated: %d page(s)" % len(changed))
    if changed:
        print(" ", ", ".join(changed))


if __name__ == "__main__":
    main()
