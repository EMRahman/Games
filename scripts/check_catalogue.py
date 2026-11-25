#!/usr/bin/env python3
"""Check that the landing page, README and game files agree.

Enforces the catalogue rules in AGENT.md:

* every root-level game file (*.html other than index.html) has exactly one
  card on index.html, and every card links to an existing game file;
* card links are relative (no "/game.html", no external URLs);
* every card has a data-icon;
* the game counts written on index.html match the number of cards;
* the README game list names the same games as the cards;
* every game links back to index.html.

Standard library only. Run from anywhere:  python3 scripts/check_catalogue.py
Exits with status 1 and lists every problem if any check fails.
"""

from __future__ import annotations

import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INDEX = "index.html"


class LandingPage(HTMLParser):
    """Collect game cards and the displayed counts from index.html."""

    def __init__(self) -> None:
        super().__init__()
        self.cards: list[dict] = []
        self.counts: dict[str, str] = {}
        self._card: dict | None = None
        self._card_depth = 0
        self._in_title = False
        self._count_id: str | None = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if self._card is not None:
            self._card_depth += tag == "a"
            if tag == "h3" and self._card["title"] is None:
                self._in_title = True
                self._card["title"] = ""
        elif tag == "a" and "data-game" in attrs:
            self._card = {
                "href": attrs.get("href") or "",
                "icon": (attrs.get("data-icon") or "").strip(),
                "title": None,
                "line": self.getpos()[0],
            }
            self._card_depth = 1
        if attrs.get("id") in ("game-count", "quick-status"):
            self._count_id = attrs["id"]
            self.counts[self._count_id] = ""

    def handle_endtag(self, tag):
        if tag == "h3":
            self._in_title = False
        if self._count_id and tag in ("p", "span"):
            self._count_id = None
        if self._card is not None and tag == "a":
            self._card_depth -= 1
            if self._card_depth == 0:
                self.cards.append(self._card)
                self._card = None

    def handle_data(self, data):
        if self._in_title and self._card is not None:
            self._card["title"] += data
        if self._count_id:
            self.counts[self._count_id] += data


def readme_titles(text: str) -> list[str]:
    """Game names from README bullets of the form '- **Name** — description'."""
    return [m.group(1).strip() for m in re.finditer(r"^\s*[-*]\s+\*\*(.+?)\*\*", text, re.M)]


def main() -> int:
    errors: list[str] = []
    game_files = sorted(p.name for p in ROOT.glob("*.html") if p.name != INDEX)

    page = LandingPage()
    page.feed((ROOT / INDEX).read_text(encoding="utf-8"))
    cards = page.cards

    # Cards and files
    seen: dict[str, int] = {}
    for card in cards:
        where = f"{INDEX}:{card['line']}"
        href = card["href"]
        name = card["title"].strip() if card["title"] else ""
        if not name:
            errors.append(f"{where}: card for '{href}' has no <h3> title")
        if not card["icon"]:
            errors.append(f"{where}: card '{name or href}' has no data-icon")
        if re.match(r"^([a-z][a-z0-9+.-]*:|//|/)", href, re.I):
            errors.append(f"{where}: card link '{href}' must be a relative path such as 'game.html'")
            continue
        target = href.split("#")[0].split("?")[0]
        if not (ROOT / target).is_file():
            errors.append(f"{where}: card '{name or href}' links to '{href}', which does not exist")
        if target in seen:
            errors.append(f"{where}: '{target}' already has a card (line {seen[target]})")
        seen.setdefault(target, card["line"])

    for game in game_files:
        if game not in seen:
            errors.append(f"{game}: playable game has no card on {INDEX}")

    # Displayed counts (the page script rewrites these, but the HTML should be right without it)
    for count_id in ("game-count", "quick-status"):
        text = page.counts.get(count_id)
        if text is None:
            errors.append(f"{INDEX}: element #{count_id} is missing")
            continue
        number = re.search(r"\d+", text)
        if not number or int(number.group()) != len(cards):
            errors.append(f"{INDEX}: #{count_id} says '{text.strip()}', but there are {len(cards)} cards")

    # README
    readme_path = ROOT / "README.md"
    listed = readme_titles(readme_path.read_text(encoding="utf-8")) if readme_path.is_file() else []
    card_titles = [c["title"].strip() for c in cards if c["title"]]
    for title in card_titles:
        if title not in listed:
            errors.append(f"README.md: game list is missing '{title}'")
    for title in listed:
        if title not in card_titles:
            errors.append(f"README.md: lists '{title}', which has no card on {INDEX}")

    # Route back to the library
    back_link = re.compile(r"""href\s*=\s*["'](?:\./)?index\.html["']""")
    for game in game_files:
        if not back_link.search((ROOT / game).read_text(encoding="utf-8")):
            errors.append(f'{game}: no link back to the library (href="index.html")')

    if errors:
        print(f"Catalogue check failed with {len(errors)} problem(s):")
        for error in errors:
            print(f"  - {error}")
        return 1
    print(f"Catalogue check passed: {len(cards)} cards, {len(game_files)} game files, README in sync.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
