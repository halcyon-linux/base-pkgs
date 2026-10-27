# CLAUDE.md

RPM packaging repo for the **base-pkgs** Copr project (`aahsnr-work/base-pkgs`): the hyprwm stack, portals and Qt theming for Fedora 44 (+45). Specs live here; Copr builds, signs and serves them. There is no application code to compile locally.

## Layout

- `pkgs/<pkg>/<pkg>.spec` — one spec per package, plus any local patches/sources.
- `ci/packages.toml` — the registry. **A package without an entry is never built.** Holds `batch` (dependency level) and an optional `[pkg.updates]` sweep feed.
- `ci/matrix.py` — selects packages to rebuild (changed `pkgs/<name>/` dirs plus transitive BuildRequires dependents) and emits the batch/wave matrix.
- `ci/sweep/` — upstream version sweeper (`sweep.py`, `feeds.py`, `spec.py`, `vercmp.py`, `custom.py`).
- `templates/` — starting specs: `source-build`, `python-hatchling`, `binary-wrapper`.
- `repo/base-pkgs.repo` — consumer drop-in (priority=1).
- `.github/workflows/` — `copr-build`, `update`, `repoclosure`, `builder-docker`; `.github/builder/Dockerfile` is the CI job image.

## Commands

```bash
python3 ci/matrix.py --list                  # whole build plan; validates registry vs. specs
python3 ci/matrix.py --list --since <rev>    # what a push from <rev> would rebuild
python3 ci/matrix.py --list --only <pkg> --dependents   # a bump's cascade (pkg + transitive BuildRequires dependents)
python3 ci/sweep/sweep.py --list             # registered feeds
python3 ci/sweep/sweep.py --dry-run          # report upstream bumps without editing any spec
python3 -m py_compile ci/*.py ci/sweep/*.py  # CI's Python syntax check
rpmspec -P pkgs/<pkg>/<pkg>.spec >/dev/null  # parse-check a spec (if rpm tooling is installed)
```

CI also runs `bash -n` + `shellcheck -S warning` on `pkgs/*/*.sh` and actionlint on workflows.

## Adding or changing a package

1. Start from the closest `templates/*.spec.tmpl`; save as `pkgs/<pkg>/<pkg>.spec`.
2. Register it in `ci/packages.toml` with the right `batch` and (usually) an `[pkg.updates]` feed: `github-release`, `github-tag` (both take `repo = "owner/name"`), or `custom` (a function in `ci/sweep/custom.py`).
3. **Batch rule:** a package may BuildRequire only packages in a *lower* batch. Packages within one batch must never depend on each other. Waves are submitted sequentially and each must finish before the next.
4. Spec conventions: full URLs in `Source*` (CI fetches them with `spectool`; never download in `%prep`), explicit `Release:`, hand-written `%changelog` (no rpmautospec), SPDX `License:`.
5. List shared-library files in `%files` with a soname glob (`%{_libdir}/lib%{name}.so.*`), never a hardcoded `.so.N` or `.so.%{version}` — upstream bumps SOVERSION on ABI breaks and the sweep bumps `Version:` unattended.
6. Keep the `Version:` line in the form the sweeper expects — `ci/sweep/spec.py` edits specs in place, so avoid restructuring `Version`/`Release`/`%global` lines it rewrites without checking it.

## Gotchas

- `ci/sweep/custom.py` is shared verbatim across the halcyon group repos and contains functions for packages not built here; the orphans are inert. Don't prune them.
- Changes under `ci/` or `.github/builder/` rebuild *every* package.
- `copr-build.yml` on push to `main` is gated by the `CASCADE_ENABLED` repo variable; `workflow_dispatch` bypasses it. PRs only validate.
- `update.yml` runs daily and after every successful `copr-build`, commits bumps straight to `main`, then dispatches `copr-build.yml` with `only=<bumped> dependents=true` (a GITHUB_TOKEN push triggers nothing by itself). Cancelling it mid-run can leave a bump without a build — dispatch `copr-build.yml` with `only` and `dependents=true`.
- The sweeper rejects versions containing `-` or whitespace and `github-tag` feeds ignore non-numeric tags (rc/beta), so a pre-release can't land in a spec. `ci/sweep/` is copied into the sibling halcyon repos but has diverged per repo — port fixes by hand, not by overwriting.
- Packages carrying patches (`qt6ct`, `hyprland-qt-support`, `xcur2png`) can fail a build after an unattended bump if the patch no longer applies; check the failing Copr build and refresh the patch.
- `hyprland` tracks stable releases only, using upstream's `source-v<version>` release asset (needed for hyprpm metadata).
- The noctalia packages are intentionally not built here (consumers use Terra's).
- Fedora 44 lacks glaze, hyprwire and hyprtoolkit, so they are packaged here. Terra supplies `anda-srpm-macros`.
- Workflow actions are pinned by SHA; Renovate handles bumps.

## Files to ignore

Don't read, edit, search or commit these; they are local scratch or generated:

- `.gitignore`d paths: `_srpms/`, `tmp/`, `.obsidian/`, `TaskNotes/`, `.cache/`, `__pycache__/`, `.zcode/`, `.zcodeignore`, and any `*.tar.gz`, `*.tar.bz2`, `*.rpm`, `*.zst`.
- `.git/`.
- Upstream tarballs/SRPMs/RPMs from local test builds. Put scratch output in `tmp/` or `_srpms/`.
- `renovate.json` unless the task is about dependency automation (it only manages GitHub Actions and the builder image pin).

## Workflows from the CLI

```bash
gh workflow run copr-build.yml -R halcyon-linux/base-pkgs --ref main -f only="<pkg> <pkg>" [-f dependents=true]
gh workflow run update.yml -R halcyon-linux/base-pkgs --ref main -f pkg="<pkg>"
gh run cancel <run-id> -R halcyon-linux/base-pkgs
```

Cancelling a run does not stop Copr builds already submitted; cancel those on the Copr project page.

## Git

Commit style: conventional commits scoped to `pkgs` or `ci` (e.g. `feat(pkgs): ...`, `fix(pkgs): ...`). Work on `main`.
