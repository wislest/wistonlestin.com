# wistonlestin.com

Personal site of **Wiston Lestin** — detection & response, detection-as-code and
AI-driven security automation. My permanent home for writing, projects and ideas,
independent of any single platform.

Static site (plain HTML + one CSS file), hosted on **Cloudflare Pages**.

## Structure

- `index.html` — home
- `writing.html` — posts index · `posts/` — articles
- `projects.html` — original open-source projects
- `about.html` — about + links
- `style.css` — shared styles (light/dark, responsive)

## Deploy

Cloudflare Pages, connected to this repo. No build step — framework preset
**None**, build output **`/`**. Every push to `main` redeploys automatically.
