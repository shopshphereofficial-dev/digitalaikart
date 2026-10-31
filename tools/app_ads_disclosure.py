#!/usr/bin/env python3
"""
Tell the truth about advertising, everywhere it matters.

The Neon Calculator app ships Google AdMob (banner + interstitial). Any page
that says "no ads", "ad-free" or "no advertising SDKs" is wrong, and Google
Play review compares the store listing, the privacy policy and the app itself.

This script runs after tools/build_apps.py and tools/app_page_extras.py and
rewrites those claims on the app page, the app privacy policy and the homepage
app card, so all three match what the app actually does.

Idempotent: text that already discloses AdMob is left alone.

Usage:  python3 tools/app_ads_disclosure.py [repo_root]
"""
import os
import re
import sys

ROOT = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")

TAGLINE = "A bright, colourful calculator with glowing neon buttons and big, easy-to-tap keys."

AD_PAGE_NOTE = (
    '<p><strong>Advertising:</strong> the app is free and supported by Google AdMob banner and '
    'interstitial ads. Google may use your advertising ID to serve them; you can reset or delete '
    'it in Android <em>Settings &rarr; Google &rarr; Ads</em>. '
    '<a href="/app-privacy-policy.html">Full details in the app privacy policy</a>.</p>'
)

AD_SECTION = """  <h2>Advertising</h2>
  <p>Neon Calculator is free and supported by advertising through <strong>Google AdMob</strong>
  (banner ads and an occasional full-screen ad). To serve ads, the Google Mobile Ads SDK may
  collect and process:</p>
  <ul>
    <li>your <strong>advertising ID</strong> (a resettable identifier Android provides for ads);</li>
    <li>device information such as the device model, operating-system version, language and the
    app version;</li>
    <li>your <strong>IP address</strong>, from which an approximate (city-level) location can be
    derived;</li>
    <li>which ads were shown and whether you interacted with them.</li>
  </ul>
  <p>We do not receive or store this data ourselves — it goes to Google. Google's use of it is
  described in <a href="https://policies.google.com/technologies/partner-sites" target="_blank"
  rel="noopener">Google's privacy and terms</a> and in the
  <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">Google Privacy
  Policy</a>.</p>
  <p><strong>Your choices:</strong> you can reset or delete your advertising ID, and turn off ad
  personalisation, in Android <em>Settings &rarr; Google &rarr; Ads</em>. The calculator keeps
  working if ads cannot load; it needs no connection for arithmetic.</p>

"""


def read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


def fix_app_page():
    path = os.path.join(ROOT, "apps", "neon-calculator", "index.html")
    t = read(path)
    if not t:
        return False
    original = t

    t = t.replace("Free \u2014 no ads, no in-app purchases",
                  "Free \u2014 supported by ads, no in-app purchases")
    t = t.replace("Free &#8212; no ads, no in-app purchases",
                  "Free &#8212; supported by ads, no in-app purchases")
    t = t.replace(
        "This app does not create an account for you, does not include advertising or analytics SDKs, "
        "and does not send your personal data to our servers.",
        "This app does not create an account for you and does not send your personal data to our own "
        "servers. It is free and supported by Google AdMob advertising.",
    )
    if "Advertising:</strong>" not in t and "App details" in t:
        t = t.replace('<section class="section"><h2 class="section-title">App details</h2>',
                      '<section class="section"><div style="max-width:720px;margin:0 auto;'
                      'color:var(--text-secondary);font-size:.85rem">' + AD_PAGE_NOTE + '</div></section>'
                      '<section class="section"><h2 class="section-title">App details</h2>', 1)

    if t != original:
        write(path, t)
        return True
    return False


def fix_privacy_policy():
    path = os.path.join(ROOT, "app-privacy-policy.html")
    t = read(path)
    if not t:
        return False
    original = t

    t = t.replace(
        "<li>We do not use third-party advertising, analytics or crash-reporting SDKs in these\n"
        "    apps. There are no ad networks and no trackers.</li>",
        "<li>The app is free and supported by <strong>Google AdMob</strong> advertising. Google may "
        "use your advertising ID to serve ads — see the Advertising section below. We do not use any "
        "analytics or crash-reporting SDK.</li>",
    )

    t = t.replace(
        "<li><strong>Internet, network state</strong> — used only to check whether a connection\n"
        "    exists. The app works fully offline.</li>",
        "<li><strong>Internet, network state</strong> — used to load ads and to check whether a "
        "connection exists. The calculator itself works fully offline.</li>",
    )

    t = t.replace(
        "<li>No analytics, advertising or tracking SDK is included.</li>",
        "<li>No analytics or crash-reporting SDK is included. The only third-party SDK is Google "
        "Mobile Ads (AdMob), used to show ads — see the Advertising section.</li>",
    )

    if "the advertising network that fills the app's banner" not in t:
        t = t.replace(
            "<li>We do not share app data with any other third party.</li>",
            "<li><strong>Google AdMob</strong> — the advertising network that fills the app's banner "
            "and interstitial slots. It receives your advertising ID, device information and IP "
            "address as described in the Advertising section.</li>\n"
            "    <li>We do not share app data with any other third party.</li>",
        )

    t = re.sub(
        r"<p>Neon Calculator is a general-audience app.*?</p>",
        "<p>Neon Calculator is a general-audience app with big, easy-to-tap keys. It does not\n"
        "  collect personal information on our servers, has no sign-up, no chat and no user-generated\n"
        "  content. It does show advertising through Google AdMob, and ads are not directed to\n"
        "  children. If you believe a child has sent us personal information by email or WhatsApp,\n"
        "  contact us and we will delete it.</p>",
        t, count=1, flags=re.S,
    )

    if "<h2>Advertising</h2>" not in t:
        t = t.replace("  <h2>Third-party services</h2>", AD_SECTION + "  <h2>Third-party services</h2>", 1)

    t = t.replace(
        "does not include advertising or analytics SDKs, and does not send your personal data to our servers",
        "is free and supported by Google AdMob ads, and does not send your personal data to our own servers",
    )

    if t != original:
        write(path, t)
        return True
    return False


def fix_homepage():
    path = os.path.join(ROOT, "index.html")
    t = read(path)
    if not t:
        return False
    original = t
    t = t.replace('<span class="app-tag">ad-free</span>', '<span class="app-tag">with ads</span>')
    t = t.replace(
        '<p class="app-desc">A colourful, kid-friendly calculator with glowing neon buttons.</p>',
        '<p class="app-desc">' + TAGLINE + '</p>',
    )
    if t != original:
        write(path, t)
        return True
    return False


def main():
    print("app page updated:", fix_app_page())
    print("app privacy policy updated:", fix_privacy_policy())
    print("homepage card updated:", fix_homepage())


if __name__ == "__main__":
    main()
