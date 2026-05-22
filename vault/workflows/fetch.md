---
name: fetch
description: Retrieve your last chat message and respond with proper headings and timestamps.
---

# Fetch

1. Run `python3 _AI/core/scripts/fetch-read.py` — prints the user's last message from the active chat file.
2. Act on the message.
3. Write the response body to a temp file, then run `python3 _AI/core/scripts/fetch-write.py /tmp/response.md --heading "Claude Cowork (Sonnet 4.6)"` — injects the heading and timestamp, appends to the active chat file, or creates a new dated file if today is a new day.

Response format (body only — heading and timestamp are injected by `--heading`):
```
Response body here. Use [[wikilinks]] for vault files.
Use [!question] callouts for questions.
```

Pass the actual tool and model in `--heading`, e.g. `"Claude Cowork (Sonnet 4.6)"`, `"Claude Code (Opus 4)"`.

Do not summarise what you did in the chat window — just say "Replied in the chat log." The appended response is the response.

Always respond via the `fetch-write` script when using this workflow, unless I say otherwise in my message.
