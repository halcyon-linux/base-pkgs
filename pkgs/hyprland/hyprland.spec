Name:           hyprland
Version:        0.56.2
Release:        3%{?dist}
%define debug_package %{nil}
Summary:        Dynamic tiling Wayland compositor that doesn't sacrifice on its looks

# hyprland: BSD-3-Clause
# subprojects/hyprland-protocols: BSD-3-Clause
# subproject/udis86: BSD-2-Clause
# protocols/ext-workspace-unstable-v1.xml: HPND-sell-variant
# protocols/wlr-foreign-toplevel-management-unstable-v1.xml: HPND-sell-variant
# protocols/wlr-layer-shell-unstable-v1.xml: HPND-sell-variant
# protocols/idle.xml: LGPL-2.1-or-later
License:        BSD-3-Clause AND BSD-2-Clause AND HPND-sell-variant AND LGPL-2.1-or-later
URL:            https://github.com/hyprwm/Hyprland
# upstream's official release asset: the full source tree with every
# submodule checked out and src/version.h.in pre-filled by upstream CI with
# the tag's real git metadata (commit hash, branch, tag, commit count).
# hyprpm reads that metadata at runtime to re-fetch the exact source, so
# the release asset — not a commit archive — is what keeps hyprpm working.
Source0:        %{url}/releases/download/v%{version}/source-v%{version}.tar.gz
Source4:        macros.hyprland

BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  meson
# CMakeLists pins glaze 7.2.0 via FetchContent when the buildroot's glaze
# is newer, and FetchContent clones with git
BuildRequires:  git-core
BuildRequires:  muParser-devel
BuildRequires:  glaze-static
BuildRequires:  pkgconfig(aquamarine)
BuildRequires:  pkgconfig(cairo)
BuildRequires:  pkgconfig(egl)
BuildRequires:  pkgconfig(gbm)
BuildRequires:  pkgconfig(gio-2.0)
BuildRequires:  pkgconfig(glesv2)
BuildRequires:  pkgconfig(glslang)
BuildRequires:  pkgconfig(hwdata)
BuildRequires:  pkgconfig(hyprcursor)
BuildRequires:  pkgconfig(hyprgraphics)
BuildRequires:  pkgconfig(hyprlang)
BuildRequires:  pkgconfig(hyprutils)
BuildRequires:  pkgconfig(hyprwayland-scanner)
BuildRequires:  pkgconfig(hyprwire)
BuildRequires:  pkgconfig(lcms2)
BuildRequires:  pkgconfig(libcanberra)
BuildRequires:  pkgconfig(libdisplay-info)
BuildRequires:  pkgconfig(libdrm)
BuildRequires:  pkgconfig(libeis-1.0)
BuildRequires:  pkgconfig(libinput) >= 1.28
BuildRequires:  pkgconfig(libliftoff)
BuildRequires:  pkgconfig(libseat)
BuildRequires:  pkgconfig(libudev)
BuildRequires:  pkgconfig(lua)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pangocairo)
BuildRequires:  pkgconfig(pixman-1)
BuildRequires:  pkgconfig(re2)
BuildRequires:  pkgconfig(readline)
BuildRequires:  pkgconfig(sdbus-c++)
BuildRequires:  pkgconfig(systemd)
BuildRequires:  pkgconfig(tomlplusplus)
BuildRequires:  pkgconfig(uuid)
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-protocols) >= 1.45
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(wayland-server)
BuildRequires:  pkgconfig(xcb-composite)
BuildRequires:  pkgconfig(xcb-dri3)
BuildRequires:  pkgconfig(xcb-errors)
BuildRequires:  pkgconfig(xcb-ewmh)
BuildRequires:  pkgconfig(xcb-icccm)
BuildRequires:  pkgconfig(xcb-present)
BuildRequires:  pkgconfig(xcb-render)
BuildRequires:  pkgconfig(xcb-renderutil)
BuildRequires:  pkgconfig(xcb-res)
BuildRequires:  pkgconfig(xcb-shm)
BuildRequires:  pkgconfig(xcb-util)
BuildRequires:  pkgconfig(xcb-xfixes)
BuildRequires:  pkgconfig(xcb-xinput)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  pkgconfig(xcursor)
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xwayland)

%if 0%{?rhel} == 10
BuildRequires:  gcc-toolset-15
BuildRequires:  gcc-toolset-15-gcc-c++
BuildRequires:  gcc-toolset-15-annobin-plugin-gcc
%endif

# udis86 is packaged in Fedora, but the copy bundled here is actually a
# modified fork.
Provides:       bundled(udis86) = 1.7.2^1.5336633

Requires:       xorg-x11-server-Xwayland%{?_isa}
Requires:       aquamarine%{?_isa} >= 0.9.2
Requires:       hyprcursor%{?_isa} >= 0.1.13
Requires:       hyprgraphics%{?_isa} >= 0.1.6
Requires:       hyprlang%{?_isa} >= 0.6.3
Requires:       hyprutils%{?_isa} >= 0.8.4

Obsoletes:      hyprland-nvidia < 1:0.32.3-2
Provides:       hyprland-nvidia = %{version}-%{release}
Obsoletes:      hyprland-legacyrenderer < 0.49.0
# the retired main-branch snapshot package — replaced by this stable build
Obsoletes:      hyprland-git

# Used in the default configuration
Recommends:     kitty
Recommends:     wofi
Recommends:     playerctl
Recommends:     brightnessctl
Recommends:     hyprland-guiutils
# Lack of graphical drivers may hurt the common use case
Recommends:     mesa-dri-drivers
# Logind needs polkit to create a graphical session
Recommends:     polkit
# https://wiki.hyprland.org/Useful-Utilities/Systemd-start
Recommends:     %{name}-uwsm
# hyprpm (shipped here) refuses to run without cmake, cpio, pkg-config, git,
# g++ and gcc, and `hyprpm update` configures the full Hyprland source tree;
# -devel carries that whole toolchain, so pull it in by default
Recommends:     %{name}-devel = %{version}-%{release}

Recommends:     (qt5-qtwayland if qt5-qtbase-gui)
Recommends:     (qt6-qtwayland if qt6-qtbase-gui)

%description
Hyprland is a dynamic tiling Wayland compositor that doesn't sacrifice
on its looks. It supports multiple layouts, fancy effects, has a
very flexible IPC model allowing for a lot of customization, a powerful
plugin system and more.

%package        uwsm
Summary:        Files for a uwsm-managed session
Requires:       uwsm
%description    uwsm
Files for a uwsm-managed session.

%package        devel
Summary:        Header and protocol files for %{name}
License:        BSD-3-Clause
Requires:       %{name}%{?_isa} = %{version}-%{release}
# hyprpm's headers build is a full cmake configure of the Hyprland source
# followed by make installheaders, so -devel carries the whole plugin
# toolchain: everything the configure step finds via pkg-config plus the
# build tools hyprpm itself checks for (cpio, cmake, pkg-config, gcc, g++)
Requires:       cpio
Requires:       cmake
Requires:       make
Requires:       gcc-c++
Requires:       meson
Requires:       ninja-build
Requires:       pkgconf-pkg-config
Requires:       git-core
Requires:       glaze-static
Requires:       muParser-devel
Requires:       pkgconfig(aquamarine)
Requires:       pkgconfig(cairo)
Requires:       pkgconfig(egl)
Requires:       pkgconfig(gbm)
Requires:       pkgconfig(gio-2.0)
Requires:       pkgconfig(glesv2)
Requires:       pkgconfig(glslang)
Requires:       pkgconfig(hwdata)
Requires:       pkgconfig(hyprcursor)
Requires:       pkgconfig(hyprgraphics)
Requires:       pkgconfig(hyprlang)
Requires:       pkgconfig(hyprutils)
Requires:       pkgconfig(hyprwayland-scanner)
Requires:       pkgconfig(hyprwire)
Requires:       pkgconfig(lcms2)
Requires:       pkgconfig(libcanberra)
Requires:       pkgconfig(libdisplay-info)
Requires:       pkgconfig(libdrm)
Requires:       pkgconfig(libeis-1.0)
Requires:       pkgconfig(libinput) >= 1.28
Requires:       pkgconfig(libliftoff)
Requires:       pkgconfig(libseat)
Requires:       pkgconfig(libudev)
Requires:       pkgconfig(lua)
Requires:       pkgconfig(pango)
Requires:       pkgconfig(pangocairo)
Requires:       pkgconfig(pixman-1)
Requires:       pkgconfig(re2)
Requires:       pkgconfig(readline)
Requires:       pkgconfig(sdbus-c++)
Requires:       pkgconfig(systemd)
Requires:       pkgconfig(tomlplusplus)
Requires:       pkgconfig(uuid)
Requires:       pkgconfig(wayland-client)
Requires:       pkgconfig(wayland-protocols) >= 1.45
Requires:       pkgconfig(wayland-scanner)
Requires:       pkgconfig(wayland-server)
Requires:       pkgconfig(xcb)
Requires:       pkgconfig(xcb-composite)
Requires:       pkgconfig(xcb-dri3)
Requires:       pkgconfig(xcb-errors)
Requires:       pkgconfig(xcb-ewmh)
Requires:       pkgconfig(xcb-icccm)
Requires:       pkgconfig(xcb-present)
Requires:       pkgconfig(xcb-render)
Requires:       pkgconfig(xcb-renderutil)
Requires:       pkgconfig(xcb-res)
Requires:       pkgconfig(xcb-shm)
Requires:       pkgconfig(xcb-util)
Requires:       pkgconfig(xcb-xfixes)
Requires:       pkgconfig(xcb-xinput)
Requires:       pkgconfig(xcursor)
Requires:       pkgconfig(xkbcommon)
Requires:       pkgconfig(xwayland)
Obsoletes:      hyprland-nvidia-devel < 1:0.32.3-2
Provides:       hyprland-nvidia-devel = %{version}-%{release}
Obsoletes:      hyprland-legacyrenderer-devel < 0.49.0
Obsoletes:      hyprland-git-devel

%description    devel
%{summary}.


%prep
%autosetup -n hyprland-source -N
# Fedora names it lua.pc . The correct version is ensured in the BuildRequires section
sed -i 's/lua55/lua/g' CMakeLists.txt

cp -p subprojects/hyprland-protocols/LICENSE LICENSE-hyprland-protocols
cp -p subprojects/udis86/LICENSE LICENSE-udis86

sed -i \
  -e "s|@@HYPRLAND_VERSION@@|%{version}|g" \
  %{SOURCE4}


%build

%if 0%{?rhel} == 10
source /usr/lib/gcc-toolset/15-env.source
%endif

%cmake \
    -GNinja \
    -DCMAKE_BUILD_TYPE=Release \
    -DNO_TESTS=TRUE \
    -DBUILD_TESTING=FALSE
%cmake_build


%install

%if 0%{?rhel} == 10
source /usr/lib/gcc-toolset/15-env.source
%endif

%cmake_install
install -Dpm644 %{SOURCE4} -t %{buildroot}%{_rpmconfigdir}/macros.d

# The session target list file: rpm rejects an empty %files -f list, so the
# always-present session desktop entry anchors it, and newer trees that
# install hyprland-session.target append their claim below.
touch hyprland-session.files
echo '%{_datadir}/wayland-sessions/hyprland.desktop' >> hyprland-session.files
if [[ -f %{buildroot}%{_libdir}/systemd/user/hyprland-session.target ]]; then
    mkdir -p %{buildroot}%{_userunitdir}
    mv %{buildroot}%{_libdir}/systemd/user/hyprland-session.target \
        %{buildroot}%{_userunitdir}/hyprland-session.target
    echo '%{_userunitdir}/hyprland-session.target' >> hyprland-session.files
fi

# upstream's lowercase compat name for the binary is created as an absolute
# symlink; rpm's file check rejects absolute symlinks inside one package —
# recreate it relative (same directory)
ln -sf Hyprland %{buildroot}%{_bindir}/hyprland

%files -f hyprland-session.files
%license LICENSE LICENSE-udis86 LICENSE-hyprland-protocols
%{_bindir}/[Hh]yprland
%{_bindir}/hyprctl
%{_bindir}/hyprpm
%{_bindir}/start-hyprland
%{_datadir}/hypr/
%{_datadir}/xdg-desktop-portal/hyprland-portals.conf
%{_mandir}/man1/hyprctl.1*
%{_mandir}/man1/Hyprland.1*
%{bash_completions_dir}/hypr*
%{fish_completions_dir}/hypr*.fish
%{zsh_completions_dir}/_hypr*

%files uwsm
%{_datadir}/wayland-sessions/hyprland-uwsm.desktop

%files devel
%{_datadir}/pkgconfig/hyprland.pc
%{_includedir}/hyprland/
%{_rpmconfigdir}/macros.d/macros.hyprland


%changelog
* Tue Oct 27 2026 halcyon-linux <aahsnr041@proton.me> - 0.56.2-3
- recommend hyprland-devel from the main package so `hyprpm update` finds
  its toolchain (cmake, cpio, pkg-config, git, g++, gcc, make and every
  build dependency of the headers configure) on a default install
* Tue Oct 27 2026 ahsan <aahsnr041@proton.me> - 0.56.2-2
- make the hyprland-session.target claim conditional (generated %files list):
  the v0.56.2 release tree predates the target that main-branch snapshots
  install under lib64/systemd/user, so the unconditional move failed the
  first Copr build of the stable track
* Tue Oct 27 2026 ahsan <aahsnr041@proton.me> - 0.56.2-1
- switch to stable release tracking: build upstream's official source-v
  release asset (submodules bundled, git metadata pre-baked in version.h.in)
  instead of main-branch snapshots, renaming hyprland-git to hyprland
  (obsoleted) — the release asset is what keeps hyprpm update working, since
  hyprpm re-fetches the exact commit the binary reports
- ship the full hyprpm toolchain in -devel (cmake, make, meson, ninja and
  every pkgconfig dependency the headers build needs) so hyprpm update
  works out of the box on consumers
* Sun Sep 27 2026 ahsan <aahsnr041@proton.me> - 0.56.2^64.git9a1ea29-2
- fix the Copr check-files failures: claim hyprland-session.target (upstream
  CMake installs it under lib64/systemd/user, which systemd never searches on
  Fedora — moved to the user unit dir) and make the lowercase hyprland
  compat symlink relative (rpm rejects absolute symlinks inside one package)
* Sun Sep 27 2026 halcyon-autoupdate <aahsnr041@proton.me> - 0.56.2^64.git9a1ea29-1
- switch to hyprland-git snapshot tracking main branch
* Wed Sep 23 2026 halcyon-autobump <aahsnr041@proton.me>
- converted to an explicit Release and changelog for the anda build
