# Project B — Verse of the Day App

Build a small browser app that shows the verse of the day, lets the user browse nearby days, and lets them pick their preferred Bible version.

Read [START-HERE.md](START-HERE.md) first — it has the ground rules, the app key, and the YouVersion API reference.

## The feature

Getting a verse of the day takes two YouVersion API calls:

1. `GET /v1/verse_of_the_days/{day}` → returns a `passage_id` (e.g. `"REV.3.20"`)
2. `GET /v1/bibles/{version_id}/passages/{passage_id}?format=text` → returns the verse text

The API supports browser requests directly (CORS is open) — call it straight from your app. Send the app key in the `x-yvp-app-key` header.

Your app:

- **On load**, shows today's verse: the reference (e.g. "Revelation 3:20") and the verse text.
- **Previous / Next** controls let the user step through days of the year.
- **A version picker** lets the user choose which Bible version the verse is shown in (e.g. World English Bible, ASV, Berean Standard Bible).

The spec intentionally leaves some details open (for example: *whose* "today" determines the verse — the browser's timezone, UTC? what does "previous" mean when you're on day 1?). Make sensible calls and record them in your README's **Decisions & Assumptions** section — or email us and ask.

## Requirements

These are specific and we will check each one:

1. **Loading & error states** — a visible loading state while fetching; if a request fails, a human-friendly message with a working **Retry** control. Never a blank screen, a frozen spinner, or raw error text (no stack traces, no `[object Object]`).
2. **The version picker is populated from the API** (`GET /v1/bibles?language_ranges[]=en*`) — not a hardcoded list.
3. **The selected version persists** — reload the page and the user's chosen version is still selected (`localStorage` or similar is fine).
4. **Scope boundary** — do **not** build a backend or proxy server, and do **not** add routing, authentication, or user accounts. We mean it — extra scope here costs you, it doesn't impress us.
5. **Tests** — required, runnable with a single documented command, and must cover at least:
   - the verse renders correctly from a mocked API response,
   - the error state renders and Retry re-fetches,
   - the day-boundary logic (what your app does at day 1 and day 365/366).

   Tests must **not** call the live YouVersion API — mock/stub/fake it.

## Optional stretch (only if you're under the time box)

A "share" or "copy verse" control that copies the reference + text to the clipboard — or anything small that shows taste. Keep it inside the time box.

## What we're evaluating

Meeting the numbered requirements above, meaningful tests, how you handled the parts the spec left open, sensible component/state structure, and a UI that handles the unhappy paths gracefully. Not: pixel-perfect design, CSS frameworks, or animation. Clean and clear beats flashy.
