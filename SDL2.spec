Name:           SDL2
Version:        2.0.5
Release:        7%{?dist}
Summary:        A cross-platform multimedia library

License:        zlib and MIT
URL:            http://www.libsdl.org/
Source0:        http://www.libsdl.org/release/%{name}-%{version}.tar.gz
Source1:        SDL_config.h

Patch0:         multilib.patch
# https://hg.libsdl.org/SDL/rev/5184186d4366
Patch1:         %{name}-2.0.5-ppc.patch
# https://hg.libsdl.org/SDL/rev/fbf9b0e3589a
Patch2:         %{name}-2.0.5-null-deref.patch

BuildRequires:  alsa-lib-devel
BuildRequires:  audiofile-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGLES-devel
BuildRequires:  libXext-devel
BuildRequires:  libX11-devel
BuildRequires:  libXi-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXrender-devel
BuildRequires:  libXScrnSaver-devel
BuildRequires:  libusb-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXcursor-devel
BuildRequires:  systemd-devel
# PulseAudio
BuildRequires:  pkgconfig(libpulse-simple)
# D-Bus
BuildRequires:  pkgconfig(dbus-1)
# IBus
BuildRequires:  pkgconfig(ibus-1.0)
%if 0%{?fedora} || 0%{?rhel} > 7
# Wayland
BuildRequires:  pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-egl)
BuildRequires:  pkgconfig(wayland-cursor)
BuildRequires:  pkgconfig(wayland-protocols)
BuildRequires:  pkgconfig(wayland-scanner)
BuildRequires:  pkgconfig(xkbcommon)
%endif

%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device.

%package devel
Summary:        Files needed to develop Simple DirectMedia Layer applications
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       mesa-libEGL-devel%{?_isa}
Requires:       mesa-libGLES-devel%{?_isa}
Requires:       libX11-devel%{?_isa}

%description devel
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device. This
package provides the libraries, include files, and other resources needed for
developing SDL applications.

%package static
Summary:	Static libraries for SDL2

%description static
Static libraries for SDL2.

%prep
%autosetup -p1
# Compilation without ESD
sed -i -e 's/.*AM_PATH_ESD.*//' configure.in
sed -i -e 's/\r//g' TODO.txt README.txt WhatsNew.txt BUGS.txt COPYING.txt CREDITS.txt README-SDL.txt

%build
%configure \
    --enable-sdl-dlopen \
    --disable-arts \
    --disable-esd \
    --disable-nas \
    --enable-pulseaudio-shared \
    --enable-alsa \
%if 0%{?fedora} || 0%{?rhel} > 7
    --enable-video-wayland \
%endif
    --disable-rpath
make %{?_smp_mflags}

%install
%make_install

# Rename SDL_config.h to SDL_config-<arch>.h to avoid file conflicts on
# multilib systems and install SDL_config.h wrapper
mv %{buildroot}%{_includedir}/SDL2/SDL_config.h %{buildroot}%{_includedir}/SDL2/SDL_config-%{_arch}.h
install -p -m 644 %{SOURCE1} %{buildroot}%{_includedir}/SDL2/SDL_config.h

# remove libtool .la file
rm -f %{buildroot}%{_libdir}/*.la
# remove static .a file
# rm -f %{buildroot}%{_libdir}/*.a

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%license COPYING.txt
%doc BUGS.txt CREDITS.txt README-SDL.txt
%{_libdir}/lib*.so.*

%files devel
%doc README.txt TODO.txt WhatsNew.txt
%{_bindir}/*-config
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/sdl2.pc
%{_libdir}/cmake/SDL2/
%{_includedir}/SDL2
%{_datadir}/aclocal/*

%files static
%license COPYING.txt
%{_libdir}/lib*.a

%changelog
* Sun Sep 03 2017 Jajauma's Packages <jajauma@yandex.ru> - 2.0.5-7
- Skip Wayland on RHEL7

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Jan 27 2017 Igor Gnatenko <ignatenko@redhat.com> - 2.0.5-3
- Fix NULL dereference (RHBZ #1416945)

* Wed Oct 26 2016 Dan Horák <dan[at]danny.cz> - 2.0.5-2
- fix FTBFS on ppc64/ppc64le

* Thu Oct 20 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.5-1
- Update to 2.0.5 (RHBZ #1387238)

* Mon Sep 05 2016 Kalev Lember <klember@redhat.com> - 2.0.4-9
- Backport Wayland fixes from upstream

* Sun Aug 14 2016 Igor Gnatenko <ignatenko@redhat.com> - 2.0.4-8
- Fix whitespaces in CMake file (RHBZ #1366868)

* Sun Jul 10 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.4-7
- Remove useless Requirements from -devel subpkg

* Sun Jul 10 2016 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.4-6
- Add ibus support

* Sun Jul 10 2016 Joseph Mullally <jwmullally@gmail.com> - 2.0.4-5
- fix Wayland dynamic symbol loading (bz1354155)

* Thu Feb 25 2016 Tom Callaway <spot@fedoraproject.org> - 2.0.4-4
- enable static subpackage (bz1253930)

* Fri Feb  5 2016 Tom Callaway <spot@fedoraproject.org> - 2.0.4-3
- fix compile against latest wayland

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.4-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Jan 04 2016 Tom Callaway <spot@fedoraproject.org> - 2.0.4-1
- update to 2.0.4

* Fri Sep 04 2015 Michal Toman <mtoman@fedoraproject.org> - 2.0.3-7
- Add support for MIPS architecture to SDL_config.h

* Tue Jun 16 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun  2 2015 Tom Callaway <spot@fedoraproject.org> - 2.0.3-5
- remove code preventing builds with ancient gcc

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Wed Jun 11 2014 Karsten Hopp <karsten@redhat.com> 2.0.3-3
- fix filename of SDL_config.h for ppc64le

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 19 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.3-1
- 2.0.3 upstream release

* Sat Mar 08 2014 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.2-1
- 2.0.2 upstream release
- Enable wayland backend

* Tue Dec 10 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.1-2
- Add libXinerama, libudev, libXcursor support (RHBZ #1039702)

* Thu Oct 24 2013 Tom Callaway <spot@fedoraproject.org> - 2.0.1-1
- update to 2.0.1

* Sat Aug 24 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-3
- Fix multilib issues

* Tue Aug 13 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-2
- SDL2 is released. Announce:
- http://lists.libsdl.org/pipermail/sdl-libsdl.org/2013-August/089854.html

* Sat Aug 10 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-1.rc4
- Update to latest SDL2 (08.08.2013)

* Tue Jul 30 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-1.rc3
- Fix Licenses
- some cleanups in spec

* Tue Jul 30 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-1.rc2
- Delete -static package
- Fix License tag
- Fix end-of-line in documents
- Remove all spike-nails EL-specify (if someone will want to do - 'patches are welcome')
- Change Release tag to .rcX%%{?dist} (maintainer has changed released tarballs)

* Mon Jul 29 2013 Igor Gnatenko <i.gnatenko.brain@gmail.com> - 2.0.0-1.rc1
- Some fixes in spec and cleanup

* Mon Jul 29 2013 Jon Ciesla <limburgher@gmail.com> - 2.0.0-1
- Ported from SDL 1.2.15-10
