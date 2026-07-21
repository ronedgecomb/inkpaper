# Releasing Inkpaper

Releases are built and published by `.github/workflows/release.yml`. The workflow uses a protected GitHub environment and PyPI Trusted Publishing; it does not use a stored PyPI token.

## One-time external activation

Complete these steps only after the publication-ready repository is reviewed:

1. Create the public GitHub repository `ronedgecomb/inkpaper` and push `main`.
2. Protect `main`: require the CI checks, require pull requests, and block force-pushes and branch deletion. Configure the rule so the single maintainer can still merge reviewed, passing work.
3. Enable secret scanning, push protection, and private vulnerability reporting.
4. Create a protected GitHub environment named `pypi`. For the default single-maintainer setup, add Ron Edgecomb as its required reviewer and leave self-review allowed so Ron can approve a release workflow that he triggered. If prevent-self-review is enabled instead, configure a genuinely independent reviewer who can approve Ron-triggered deployments.
5. Confirm `https://pypi.org/project/inkpaper/` is still unclaimed.
6. In PyPI, create a pending publisher for owner `ronedgecomb`, repository `inkpaper`, workflow `release.yml`, and environment `pypi`.

Do not add a PyPI API token to GitHub.

## Prepare version 0.1.0

The repository already declares 0.1.0. Confirm it and update the changelog entry from `Unreleased` to the release date:

```powershell
uv version --short
uv lock
uv lock --check
```

Expected version output: `0.1.0`.

For later patch releases, run `uv version --bump patch`, then update `CHANGELOG.md` and commit both `pyproject.toml` and `uv.lock`.

## Automated local gates

```powershell
uv sync --locked
uv run ruff check .
uv run ruff format --check .
uv run pytest -q
uv run --isolated --with "gradio==6.20.0" --upgrade-package gradio pytest -q
uv run --isolated --with "gradio>=6.20,<7" --upgrade-package gradio pytest -q
```

Build into a unique temporary directory and validate both distributions:

```powershell
$artifactDir = Join-Path ([System.IO.Path]::GetTempPath()) ("inkpaper-release-" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $artifactDir | Out-Null
uv build --out-dir $artifactDir
$wheel = (Get-ChildItem -LiteralPath $artifactDir -Filter *.whl).FullName
$sdist = (Get-ChildItem -LiteralPath $artifactDir -Filter *.tar.gz).FullName
$releaseVersion = uv version --short
uv run twine check $wheel $sdist
uv run check-wheel-contents $wheel
uv run --no-project --isolated --with $wheel python -I scripts/smoke_install.py $releaseVersion
uv run --no-project --isolated --with $sdist python -I scripts/smoke_install.py $releaseVersion
uv run python scripts/check_release.py "v$releaseVersion"
```

Every command must exit successfully.

## Manual visual gate

Run `uv run python demo/app.py`, then inspect desktop and narrow layouts before creating the GitHub Release:

- initial dark-mode load and the `__theme=dark` URL behavior;
- text, number, dropdown, radio, checkbox, slider, and keyboard focus states;
- primary, secondary, and stop buttons at rest, hover, focus, and active states;
- long-job progress and cancellation;
- chat messages, tables, code surfaces, prose hierarchy, and links; and
- keyboard-only navigation with visible slate outlines.

Prepare a non-empty summary of the result for the release notes. The publish command below requires it. Stop the demo with Ctrl+C.

## Publish

Merge the reviewed version and changelog changes through protected `main`. Then create the release from the exact `main` commit:

```powershell
$releaseVersion = uv version --short
$visualGateSummary = Read-Host "Summarize the completed manual visual gate"
if ([string]::IsNullOrWhiteSpace($visualGateSummary)) {
    throw "A manual visual-gate summary is required."
}
gh release create "v$releaseVersion" --target main --title "inkpaper $releaseVersion" --notes $visualGateSummary --generate-notes
```

`--notes` prepends the manual visual-gate summary to the generated release notes. Publishing the GitHub Release triggers CI again. The release tag must equal `v` plus the project version. The workflow builds once, validates and hashes the artifacts, waits for approval on the `pypi` environment, publishes those exact files, and uploads attestations.

## Verify publication

1. Confirm the GitHub workflow succeeded and the `pypi` environment approval is recorded.
2. Confirm PyPI lists one wheel and one source distribution with provenance.
3. Compare PyPI SHA-256 values with the workflow's `SHA256SUMS` artifact.
4. Run a clean install:

```powershell
$releaseVersion = uv version --short
uv run --no-project --isolated --with "inkpaper==$releaseVersion" python -c "import inkpaper; print(inkpaper.__version__, type(inkpaper.THEME).__name__, bool(inkpaper.CSS.strip()))"
```

Expected output begins with the release version and ends with `Inkpaper True`.

## Yank a broken release

Uploaded files and filenames cannot be overwritten or reused, and Inkpaper's project policy is to never reuse a published version. If a release is unsafe or unusable, open the release under the PyPI project's Manage page, choose **Options**, select **Yank**, and record a concise reason. Fix the defect, increment the version, repeat every gate, and publish a new GitHub Release.
