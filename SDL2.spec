Name:           SDL2
Version:        2.0.0
Release:        1.rc3%{?dist}
Summary:        A cross-platform multimedia library
Group:          System Environment/Libraries
URL:            http://www.libsdl.org/
License:        zlib and MIT
Source0:        http://www.libsdl.org/tmp/release/%{name}-%{version}.tar.gz

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
BuildRequires:  dbus-devel
BuildRequires:  libXScrnSaver-devel
BuildRequires:  libusb-devel
BuildRequires:  pulseaudio-libs-devel

%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device.

%package devel
Summary:    Files needed to develop Simple DirectMedia Layer applications
Group:      Development/Libraries
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   alsa-lib-devel
Requires:   mesa-libGL-devel
Requires:   mesa-libGLU-devel
Requires:   mesa-libEGL-devel
Requires:   mesa-libGLES-devel
Requires:   libX11-devel
Requires:   libXi-devel
Requires:   libXext-devel
Requires:   libXrandr-devel
Requires:   libXrender-devel
Requires:   libXScrnSaver-devel

%description devel
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device. This
package provides the libraries, include files, and other resources needed for
developing SDL applications.

%prep
%setup -q
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
    --disable-rpath
make %{?_smp_mflags}

%install
%make_install

# remove libtool .la file
rm -f %{buildroot}%{_libdir}/*.la
# remove static .a file
rm -f %{buildroot}%{_libdir}/*.a

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%doc BUGS.txt CREDITS.txt COPYING.txt README-SDL.txt
%{_libdir}/lib*.so.*

%files devel
%doc README.txt TODO.txt WhatsNew.txt
%{_bindir}/*-config
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/sdl2.pc
%{_includedir}/SDL2
%{_datadir}/aclocal/*

%changelog
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
