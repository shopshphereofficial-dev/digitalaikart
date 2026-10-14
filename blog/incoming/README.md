# Queued blog posts

An agent drops ONE JSON file per day in this folder. `tools/publish_queued.py`
(which the scheduled GitHub workflow runs) picks the oldest file here, generates
the cover image with Gemini, renders the post page, updates the blog index, the
RSS feed and the sitemap, then deletes the file it used.

If this folder is empty, the scheduled run does nothing — that is normal.

## File name

    <YYYY-MM-DD>-<short-slug>.json

e.g. `2026-10-15-india-ai-mission-update.json`

## Required fields

```json
{
  "title": "headline, max 70 characters, no clickbait",
  "slug": "kebab-case, max 55 characters",
  "category": "one of: AI Business, AI Policy, AI Products, AI Hardware, AI Jobs, AI Safety, AI Research, AI India",
  "description": "meta description, 140-160 characters, ends with a full stop",
  "emoji": "one emoji",
  "keywords": ["5 short keywords"],
  "tags": ["#Tag1", "#Tag2", "#Tag3", "#Tag4"],
  "tldr": ["3-4 one-line takeaways"],
  "sections": [
    {"heading": "short heading, no numbering", "paragraphs": ["paragraph", "paragraph"]}
  ],
  "faq": [{"q": "question", "a": "2-line answer"}],
  "image_prompt": "short English description of a natural, photorealistic photo for this story. No text, no logos, no brand colours, wide 16:9 landscape.",
  "source_name": "name of the news outlet used",
  "source_url": "full link of the story used"
}
```

Aim for 4-5 sections of 1-2 paragraphs each (about 700-900 words) and 3 FAQ
items. Plain English, no markdown, no emojis in the article text.

The article text must be written by the agent. Gemini is called only for the
cover image.
