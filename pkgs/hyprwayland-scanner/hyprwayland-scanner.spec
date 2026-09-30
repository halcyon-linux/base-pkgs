Name:           hyprwayland-scanner
Version:        0.4.6
Release:        2%{?dist}
%define debug_package %{nil}
Summary:        A Hyprland implementation of wayland-scanner, in and for C++

License:        BSD-3-Clause
URL:            https://github.com/hyprwm/hyprwayland-scanner
Source:         %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

# https://fedoraproject.org/wiki/Changes/EncourageI686LeafRemoval
ExcludeArch:    %{ix86}

BuildRequires:  cmake
BuildRequires:  cmake(pugixml)
BuildRequires:  gcc-c++

%description
%{summary}.

%package        devel
Summary:        A Hyprland implementation of wayland-scanner, in and for C++

Requires:       %{name} = %{version}-%{release}

%description    devel
%{summary}.

%prep
%autosetup -p1

%build
%cmake
%cmake_build

%install
%cmake_install

# the base/devel split: the base package carries the scanner binary (what
# desktop.yml installs by name), devel the pkgconfig/cmake metadata the
# pkgconfig() BuildRequires of the consumers resolve through
%files
%license LICENSE
%{_bindir}/%{name}

%files devel
%license LICENSE
%doc README.md
%{_libdir}/pkgconfig/%{name}.pc
%{_libdir}/cmake/%{name}/

%changelog
* Wed Sep 23 2026 halcyon-autobump <aahsnr041@proton.me>
- converted to an explicit Release and changelog for the anda build
