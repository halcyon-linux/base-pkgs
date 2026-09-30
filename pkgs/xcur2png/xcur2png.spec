# Ported from LionHeartP/hyprlandRPM (the hyprland-stack bootstrap Copr).
# nwg-look shells out to xcur2png for cursor-preview extraction, and Fedora
# ships no package for it (the nwg-shell Coprs note it as an unmet
# recommendation) — packaged here so the require resolves from this repo.
#
# Patch: upstream's alpha un-premultiply divides by 256 instead of 255;
# the fix is eworm's own (upstream-merged), carried in the reference repo.
#
# The source is 2020-era K&R-style C (`extern dry_run;` etc.) — Fedora 44's
# GCC treats implicit int as a hard error, so the modern-C porting macro
# (the reference spec carries it for exactly this reason) relaxes the
# errors instead of patching the vintage declarations.
%global build_type_safety_c 0

Name:           xcur2png
Version:        0.7.1
Release:        2%{?dist}
%define debug_package %{nil}
Summary:        Convert X cursors to PNG images

License:        GPL-3.0-or-later
URL:            https://github.com/eworm-de/xcur2png
Source:         %{url}/archive/%{version}/%{name}-%{version}.tar.gz
Patch:          0001-fix-wrong-math.patch

BuildRequires:  gcc
BuildRequires:  pkgconfig(libpng)
BuildRequires:  pkgconfig(xcursor)

%description
xcur2png is a program which let you take PNG image from X cursor, and
generate config-file which is reusable by xcursorgen. To put it simply, it
is converter from X cursor to PNG image.

%prep
%autosetup -p1

%build
%configure
%make_build

%install
%make_install

%files
%license COPYING
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.*

%changelog
* Thu Oct 01 2026 halcyon-autobump <aahsnr041@proton.me>
- converted to an explicit Release and changelog for the anda build
