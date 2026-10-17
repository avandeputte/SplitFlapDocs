# SplitFlap documentation site

The source of **[splitflap.iothing.net](https://splitflap.iothing.net)** — the complete guide
to building a mechanical split-flap display and driving it with live content. It covers the
[module firmware](https://github.com/avandeputte/SplitFlapUniversalFirmware), the
[SplitFlap Gateway](https://github.com/avandeputte/SplitFlapGateway), the
[Companion](https://github.com/avandeputte/SplitFlapGatewayCompanion), the
[Matrix](https://github.com/avandeputte/MatrixPortalGateway) and
[LCD](https://github.com/avandeputte/SplitFlapGatewayLCD) gateways, and Home Assistant.

Two things live here:

- **`landing/`** — the one-page site at the root of the domain (`index.html`, hand-written).
- **`docs/`** — the guide, served under **`/docs/`**. Plain Markdown, built with
  [MkDocs](https://www.mkdocs.org/) and the [Material](https://squidfunk.github.io/mkdocs-material/)
  theme, styled to the landing page's palette (`docs/stylesheets/extra.css`). The sidebar is the
  `nav:` block in `mkdocs.yml`.

`build.sh` assembles both into `site/`.

## Working on it

```bash
pip install -r requirements.txt
mkdocs serve      # live preview of the docs at http://127.0.0.1:8000/docs/
sh build.sh       # the full site into site/ -- what CI and the deploy run
```

Every push to `main` is built by GitHub Actions (`--strict`: a broken link fails the build) and
deployed by Cloudflare Pages.

## Where the content came from

The pages were imported from the
[SplitFlapGateway wiki](https://github.com/avandeputte/SplitFlapGateway/wiki), keeping the
wiki's page names so every URL mirrors the wiki's. `tools/import_wiki.py` does that import —
page links rewritten, images copied, the nav regenerated from the wiki's sidebar — and can be
re-run against a wiki checkout if the wiki is ever edited again:

```bash
git clone https://github.com/avandeputte/SplitFlapGateway.wiki.git ../SplitFlapGateway.wiki
python3 tools/import_wiki.py ../SplitFlapGateway.wiki
```

**This repository is the source of truth from now on.** Edit the Markdown here.

## Deploying

The site is the Cloudflare Pages project **`splitflap`** (direct upload, custom domain
`splitflap.iothing.net`). Deploy a build with wrangler, using an API token that has
*Cloudflare Pages: Edit* on the account:

```bash
export CLOUDFLARE_API_TOKEN=...            # never commit this
export CLOUDFLARE_ACCOUNT_ID=...           # see below
sh build.sh
npx wrangler@latest pages deploy site --project-name splitflap --branch main
```

The deploy is live on the domain within a minute. The account id has to be given explicitly
when the token is scoped too narrowly to list accounts, which a *Pages: Edit* token usually
is. Find it in the Cloudflare dashboard, on the account's overview page or in the URL of any
page inside the account.

## Alternatively: let Cloudflare build it from Git

If you would rather not run wrangler, connect the project to this repository instead and
Cloudflare builds on every push (one-time setup, no secrets needed):

1. Cloudflare dashboard → **Workers & Pages → `splitflap` → Settings → Builds** → connect to
   Git → pick this repository, production branch `main`.
2. Build settings:
   - **Build command:** `pip install -r requirements.txt && sh build.sh`
   - **Build output directory:** `site`
   - **Environment variable:** `PYTHON_VERSION` = `3.12`

The custom domain is already attached to the project, so nothing changes there.

## License

The documentation is **CC BY-NC-SA 4.0** (non-commercial, share-alike, attribution). The
split-flap module hardware and the original bus protocol are by
[Adam G Makes](https://www.youtube.com/@AdamGMakes).
