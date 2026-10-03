# Repository instructions

This repository is a collection of self-contained browser games. `index.html` is the public landing page and must remain the canonical list of playable games.

## Adding or changing a game

- Every playable game must be a self-contained `.html` file in the repository root unless there is a clear technical reason to add an asset folder.
- Whenever a game is added, renamed, or removed, update the card collection in `index.html` in the same change. A new game is not complete until it appears on the landing page and its card link works from a GitHub Pages project URL.
- Give every landing-page game card a `data-icon`; the above-the-fold quick-launch menu is generated from the card collection.
- Update the visible game count on the landing page whenever the card collection changes.
- Keep the game list in `README.md` synchronized with the landing-page collection.
- Use relative links. Do not use root-relative paths such as `/game.html`; the site must work when GitHub Pages serves it below `/<repository-name>/`.
- Keep the site dependency-free unless the task explicitly requires otherwise. Do not add remote fonts, analytics, trackers, or third-party scripts.
- Preserve the visual identity of each existing game. Landing-page artwork should be made with local HTML/CSS/SVG or committed image assets, never hotlinked assets.
- Record each new game's creation prompt, date, and actual model in its UI or browser console. Preserve existing generation metadata when changing a game. If a prompt names a commercial game, toy, or other brand, record it paraphrased with the brand replaced by a generic description, and mark it as paraphrased.

## Original content only

Classic game mechanics may be reused, but everything players see must be original.

- Do not name games, files, or CSS classes after commercial games, toys, or brands, and do not use brand names in game text, landing-page copy, or the README.
- Do not copy board layouts, maps, territory or city networks, card or rule text, price or score tables, colour schemes, logos, or artwork from commercial games. Design new ones instead.
- Do not reproduce trademarks or wordmarks, including on decorative devices such as phones or consoles.
- Describe a game by its genre (for example, "property trading" or "falling-block puzzle"), not as "X-style".

## Browser and device requirements

Every game and the landing page must work in current Safari and Chrome on iPhone and iPad, and current Safari, Chrome, Firefox, and Edge on Mac and PC.

- Include `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">`.
- Support both pointer input and touch input. Never make hover the only way to reveal a control or essential information.
- Support keyboard input where it fits the game, and do not break the browser's normal keyboard navigation.
- Make interactive targets at least 44 by 44 CSS pixels on touch layouts.
- Account for notches and home indicators with `env(safe-area-inset-*)` where controls touch a screen edge.
- Use `100dvh` only with a `100vh` or equivalent fallback. Avoid layouts that rely on a fixed desktop viewport.
- Prevent unwanted page scrolling and browser gestures only inside the active game surface; keep ordinary landing-page scrolling intact.
- Respect `prefers-reduced-motion` for nonessential animation.
- Treat audio, fullscreen, local storage, and vibration as optional enhancements. Games must remain playable if any of them is unavailable or denied.

## Completion checklist

Before considering a game change complete:

1. Open `index.html` at a narrow phone width, a tablet width, and a desktop width.
2. Follow every game-card link and check that there are no missing local files or console errors.
3. Play the changed game with mouse/keyboard and with touch emulation.
4. Check portrait and landscape layouts when the game supports mobile play.
5. Confirm that text does not overflow, controls remain reachable, and important content is not hidden behind safe areas.
6. Confirm that the landing-page card list and displayed game count match all playable root-level game HTML files other than `index.html`.


### Post-PR Review Protocol

After opening a Pull Request, your task is not complete until you have monitored it for reviewer feedback. Stay active and periodically check the PR status for the next 10 minutes using whatever tools you have available (e.g., GitHub CLI, API, or terminal scripts).

Your objectives during this window:
* **On Approval (including automated 👍 reviews):** Automatically merge after either an authorized human reviewer other than the PR author approves the latest changes or the repository's configured automated reviewer (currently the Codex GitHub integration, `chatgpt-codex-connector[bot]`) signals approval of the latest changes with an approving review or a 👍 comment/reaction. Automated approval is sufficient; a separate human approval is not required unless repository rules require it. Before merging, verify that all required checks have passed, no unresolved change requests remain, and all repository merge requirements are satisfied. Thumbs-up from the author or an unrelated commenter/bot does not qualify. If the approval's source, applicability to the latest changes, or any prerequisite cannot be verified, leave the PR open.
* **On Feedback / Requested Changes:** Read the comments, modify the code to address them, push your updates, and ask for a re-review.
* **On Timeout:** If 10 minutes pass with no review activity, conclude the task and exit naturally.
