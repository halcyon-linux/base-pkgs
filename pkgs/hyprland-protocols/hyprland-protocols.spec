Name:           hyprland-protocols
Version:	0.8.0
Release:        2%{?dist}
%define debug_package %{nil}
Summary:        Wayland protocol extensions for Hyprland
BuildArch:      noarch

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprland-protocols
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  gcc

%description
%{summary}.

%package        devel
Summary:        Wayland protocol extensions for Hyprland

Requires:       %{name} = %{version}-%{release}

%description    devel
%{summary}.


%prep
%autosetup -p1


%build
# upstream switched from meson to cmake at v0.7.1 (the tarball carries
# CMakeLists.txt; it installs the protocol XMLs and the pkg-config file)
%cmake
%cmake_build


%install
%cmake_install


# the base/devel split: the base package carries the protocol XMLs (what
# desktop.yml installs by name), devel the pkgconfig file the pkgconfig()
# BuildRequires of the consumers resolve through
%files
%license LICENSE
%{_datadir}/%{name}/

%files devel
%license LICENSE
%doc README.md
%{_datadir}/pkgconfig/%{name}.pc


%changelog
* Mon Oct 19 2026 halcyon-linux <aahsnr041@proton.me> - 0.8.0-2
- add the gcc BuildRequires: upstream changed CMakeLists.txt from
  LANGUAGES NONE to LANGUAGES C at 0.8.0, so CMake now looks for a C compiler
* Wed Sep 23 2026 halcyon-autobump <aahsnr041@proton.me>
- converted to an explicit Release and changelog for the anda build
