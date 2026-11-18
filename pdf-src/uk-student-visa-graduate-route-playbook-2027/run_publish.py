# -*- coding: utf-8 -*-
"""Build the playbook PDF into downloads/ and update the site listing."""
import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.dirname(here))

sys.path.insert(0, here)
import build  # noqa: E402

out_dir = os.path.join(root, "downloads")
os.makedirs(out_dir, exist_ok=True)
out = os.path.join(out_dir, "uk-study-visa-graduate-route-playbook-2027.pdf")
build.build(out)
print("wrote", out, os.path.getsize(out), "bytes")

from pypdf import PdfReader  # noqa: E402
pages = len(PdfReader(out).pages)
print("pages", pages)
if pages < 45:
    raise SystemExit("page count too low: %s" % pages)

sys.path.insert(0, os.path.join(root, "tools"))
import publish_uk_playbook as pub  # noqa: E402

changed = [pub.add_card(root), pub.add_json(root), pub.add_sitemap(root)]
print("site updated:", any(changed))
