## What I built

- **Backend:** `GET /data` returns each item with the client's details redacted from the question, citations turned into numbered links, and a favicon for every source.
- **Frontend:** each item is a card showing the redacted question, the answer with working citation links, and every source with its favicon.

### redaction.py

- The model's three name labels (`full_name`, `first_name`, `last_name`) all map to the same type, `[NAME]`. Presidio only merges overlapping finds when they have the same type, so "Sarah Jones", "Sarah" and "Jones" become a single `[NAME]` rather than `[NAME] [NAME]`.
- Redaction happens in the backend, so the client's real details never reach the browser.

### citations.py

- Sources are numbered in the order they're first cited.
- One citation in the debt answer points to an ID that doesn't match any source (`dOQ-BJgBLViOYD1OzWM` vs `dOQ-BJgBBLViOYD1OzWM`, one letter missing). I removed it rather than guessing the closest match, because linking advice to the wrong source is worse than not linking it.
- The backend builds the links as HTML, because the answers already contain HTML (`<b>`) and the task asks for this to happen in the backend. Source URLs are escaped before they go into the HTML.

### favicons.py

- I used Google's favicon service rather than fetching each site's icon myself. It needs no network calls from the backend and always returns an image, even for sites without one.
- The trade-off is that the user's browser asks Google for the icons, so Google can see which sites were looked up. For a real service I'd fetch and host the icons on our own server.

### Content.tsx

- Cited sources are listed first in number order, Uncited sources come after, faded and marked "Not cited".
- The answer is inserted with `dangerouslySetInnerHTML` so the bold text and links display properly. `whitespace-pre-line` keeps the answer's line breaks.
- Favicons use a plain `<img>` with `alt=""`, because they're decorative (the title next to each one says what it is) and `next/image` adds nothing for a 16px icon.
- TypeScript types in `frontend/lib/types.ts` match the backend's Pydantic models.

## What didn't work / what I'd improve

- **The answer HTML isn't sanitised.** It's safe with this data, but if future answers come from an AI model or another system, harmful HTML could run in the adviser's browser. I'd clean it in the backend with an allow list (only `<b>` and `<a>`), using a library like `nh3`.
- **The model can miss things.** I checked all four questions by eye, but a model can't guarantee it catches every name in future data, especially for longer questions.
- Removing the broken citation leaves a stray space before the full stop ("circumstances .").
- The model runs on every request to `/data`. If the data doesn't change, I'd redact it once and cache the result.
- The backend URL is hard-coded in `page.tsx`. It should come from an environment variable.
- There are no tests for anything. Usually, I'd test every feature using mocking strategies.

## Use of AI

I used Claude for writing some code and ideas. It's important that no sensitive information is put into AI tools. Client details are personal data, and I know sharing them with a AI is against UK data protection law.