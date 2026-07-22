# Releasing Inkpaper

Releases are built and published by `.github/workflows/release.yml`. The workflow uses a protected GitHub environment and PyPI Trusted Publishing; it does not use a stored PyPI token.

## One-time external activation

These steps were completed for the 0.1.0 release and are retained for reference. They apply only to a fresh repository setup:

1. Create the public GitHub repository `ronedgecomb/inkpaper` and push `main`.
2. Protect `main`: require the CI checks, require pull requests, and block force-pushes and branch deletion. Configure the rule so the single maintainer can still merge reviewed, passing work.
3. Enable secret scanning, push protection, and private vulnerability reporting.
4. Create a protected GitHub environment named `pypi`. For the default single-maintainer setup, add Ron Edgecomb as its required reviewer and leave self-review allowed so Ron can approve a release workflow that he triggered. If prevent-self-review is enabled instead, configure a genuinely independent reviewer who can approve Ron-triggered deployments.
5. Confirm `https://pypi.org/project/inkpaper/` is still unclaimed.
6. In PyPI, create a pending publisher for owner `ronedgecomb`, repository `inkpaper`, workflow `release.yml`, and environment `pypi`.

Do not add a PyPI API token to GitHub.

## Prepare the release

Bump the version (patch by default; choose minor or major when the changes call for it), move the `Unreleased` changelog entries under a dated heading for the new version, and update the README's pinned git-install tag to match. The docs test derives the expected tag from `pyproject.toml`, so a version bump without the README update fails CI.

PowerShell or bash:

```text
uv version --bump patch
uv lock
uv lock --check
```

Commit `pyproject.toml`, `uv.lock`, `CHANGELOG.md`, and `README.md` together.

## Automated local gates

Run in either PowerShell or bash:

```text
uv sync --locked
uv run ruff check .
uv run ruff format --check .
uv run pytest -q
uv run --isolated --with "gradio==6.20.0" --upgrade-package gradio pytest -q
uv run --isolated --with "gradio>=6.20,<7" --upgrade-package gradio pytest -q
```

Build into a unique temporary directory and validate both distributions.

PowerShell:

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

bash:

```bash
artifactDir="$(mktemp -d)"
uv build --out-dir "$artifactDir"
releaseVersion="$(uv version --short)"
uv run twine check "$artifactDir"/*.whl "$artifactDir"/*.tar.gz
uv run check-wheel-contents "$artifactDir"/*.whl
uv run --no-project --isolated --with "$artifactDir"/*.whl python -I scripts/smoke_install.py "$releaseVersion"
uv run --no-project --isolated --with "$artifactDir"/*.tar.gz python -I scripts/smoke_install.py "$releaseVersion"
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

Merge the reviewed version, changelog, and README changes through protected `main`. Then create the release from the exact `main` commit.

PowerShell:

```powershell
$releaseVersion = uv version --short
$visualGateSummary = Read-Host "Summarize the completed manual visual gate"
if ([string]::IsNullOrWhiteSpace($visualGateSummary)) {
    throw "A manual visual-gate summary is required."
}
gh release create "v$releaseVersion" --target main --title "inkpaper $releaseVersion" --notes $visualGateSummary --generate-notes
```

bash:

```bash
releaseVersion="$(uv version --short)"
read -p "Summarize the completed manual visual gate: " visualGateSummary
if [ -z "${visualGateSummary//[[:space:]]/}" ]; then
    echo "A manual visual-gate summary is required." >&2
    exit 1
fi
gh release create "v$releaseVersion" --target main --title "inkpaper $releaseVersion" --notes "$visualGateSummary" --generate-notes
```

`--notes` prepends the manual visual-gate summary to the generated release notes. Publishing the GitHub Release triggers CI again. The release tag must equal `v` plus the project version. The workflow builds once, validates and hashes the artifacts, waits for approval on the `pypi` environment, publishes those exact files, and uploads attestations.

## Verify publication

1. Confirm the GitHub workflow succeeded and the `pypi` environment approval is recorded.
2. Confirm PyPI lists one wheel and one source distribution with provenance.
3. Compare PyPI SHA-256 values with the workflow's `SHA256SUMS` artifact.
4. Run a clean install.

PowerShell:

```powershell
$releaseVersion = uv version --short
uv run --no-project --isolated --with "inkpaper==$releaseVersion" python -c "import inkpaper; print(inkpaper.__version__, type(inkpaper.THEME).__name__, bool(inkpaper.CSS.strip()))"
```

bash:

```bash
releaseVersion="$(uv version --short)"
uv run --no-project --isolated --with "inkpaper==$releaseVersion" python -c "import inkpaper; print(inkpaper.__version__, type(inkpaper.THEME).__name__, bool(inkpaper.CSS.strip()))"
```

Expected output begins with the release version and ends with `Inkpaper True`.

## Yank a broken release

Uploaded files and filenames cannot be overwritten or reused, and Inkpaper's project policy is to never reuse a published version. If a release is unsafe or unusable, open the release under the PyPI project's Manage page, choose **Options**, select **Yank**, and record a concise reason. Fix the defect, increment the version, repeat every gate, and publish a new GitHub Release.
