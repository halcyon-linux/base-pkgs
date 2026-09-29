# base-pkgs

halcyon desktop core — the hyprwm stack, portals, Qt theming — Fedora 44 (+45) RPMs built on
[Copr](https://copr.fedorainfracloud.org/coprs/aahsnr-work/base-pkgs/).

```
dnf copr enable aahsnr-work/base-pkgs fedora-44
```

One of the six halcyon group repositories: base-pkgs · cli-tools ·
applications · fonts · texlive-packages · linux-p03.

## CI

- `copr-build.yml` — a push to `main` rebuilds changed packages plus every
  higher batch, wave-by-wave. Gated on the `CASCADE_ENABLED` repository
  variable (kill-switch; `workflow_dispatch` bypasses it). PRs validate
  only.
- `update.yml` — the upstream version sweep (`ci/sweep/sweep.py` over the
  registry's `[pkg.updates]` feeds), commits bumps straight to `main`.
- `repoclosure.yml` — nightly (05:43 UTC) + post-cascade closure check of
  the published Copr repo against Fedora 44/45 (+ Terra and the
  lionheartp bootstrap repo).
- `builder-docker.yml` — builds this repo's own CI job image and pushes
  it to `ghcr.io/halcyon-linux/base-pkgs-builder:f44` (consumed by this
  repo's build and sweep jobs).


## Layout

```
ci/packages.toml    the registry: build selection + sweep-feed config
ci/matrix.py        batch/wave build plan (validate job runs it)
ci/sweep/           the version sweeper + custom feeds
pkgs/<pkg>/         spec + local sources
repo/               consumer .repo drop-ins (all six group repos)
templates/          starting points for new specs
```

See [AGENTS.md](AGENTS.md) for the conventions before touching specs.
