# Third-party files in this folder

Everything here is downloaded by `build_pptx.py` (step 1) when missing. These files are data only:
they are never executed, and the Python that reads them runs with `python3 -I`.

## Fonts (`fonts/`) — SIL Open Font License 1.1

Source: the Google Fonts repository, https://github.com/google/fonts, fetched from
`https://raw.githubusercontent.com/google/fonts/main/ofl/<family>/`.

| Family | Files | Licence file |
|---|---|---|
| Alexandria (variable, wght 100–900) | `fonts/Alexandria/Alexandria[wght].ttf` | `fonts/Alexandria/OFL.txt` (from `ofl/alexandria/OFL.txt`) |
| IBM Plex Sans Arabic 400/500/600/700 | `fonts/IBMPlexSansArabic/IBMPlexSansArabic-{Regular,Medium,SemiBold,Bold}.ttf` | `fonts/IBMPlexSansArabic/OFL.txt` (from `ofl/ibmplexsansarabic/OFL.txt`) |
| IBM Plex Mono 400/600 | `fonts/IBMPlexMono/IBMPlexMono-{Regular,SemiBold}.ttf` | `fonts/IBMPlexMono/OFL.txt` (from `ofl/ibmplexmono/OFL.txt`) |

The same files and their `OFL.txt` are copied next to the deliverable (`<out dir>/fonts/`), as the
OFL allows when the licence travels with the fonts. "IBM Plex" is a Reserved Font Name: the files
are shipped unmodified under their original names.

## Icons (`icons/`) — MIT License

Phosphor Icons, "regular" weight, package `@phosphor-icons/core` version 2.1.1.
Source: https://github.com/phosphor-icons/core, fetched from
`https://unpkg.com/@phosphor-icons/core@2.1.1/assets/regular/<name>.svg`.
Licence: `icons/LICENSE-phosphor.txt` (from `https://unpkg.com/@phosphor-icons/core@2.1.1/LICENSE`),
MIT, Copyright (c) 2023 Phosphor Icons.

Mapping of the deck's `<x-icon name>` to Phosphor assets (see `ICONS` in `build_pptx.py`):

| x-icon | Phosphor | x-icon | Phosphor |
|---|---|---|---|
| Activity | pulse | Key | key |
| Book | book | Lightbulb | lightbulb |
| Chart | chart-bar | Lightning | lightning |
| Chat | chat-circle | Link | link |
| Check | check | Lock | lock |
| CheckCircle | check-circle | PaperPlane | paper-plane-tilt |
| Clock | clock | Play | play |
| Cloud | cloud | Search | magnifying-glass |
| Code | code | Settings | gear |
| Database | database | Star | star |
| Globe | globe | ThumbsUp | thumbs-up |
| GraduationCap | graduation-cap | Tool / Wrench | wrench |
| Home | house | Trust | handshake |
| Users | users | Verified | seal-check |
| Warning | warning | | |
