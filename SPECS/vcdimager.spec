Summary: VideoCD (pre-)mastering and ripping tool
Name: vcdimager
Version: 0.7.24
Release: 8%{?dist}
License: GPLv2+
Group: Applications/Multimedia
URL: http://www.gnu.org/software/vcdimager/
Source: ftp://ftp.gnu.org/pub/gnu/vcdimager/vcdimager-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
Requires: %{name}-libs = %{version}-%{release}
Requires(post): info
Requires(preun): info
BuildRequires: libcdio-devel >= 0.72
BuildRequires: libxml2-devel >= 2.3.8
BuildRequires: zlib-devel
BuildRequires: pkgconfig >= 0.9
BuildRequires: popt-devel

%description
VCDImager allows you to create VideoCD BIN/CUE CD images from MPEG
files. These can be burned with cdrdao or any other program capable of
burning BIN/CUE files.

Also included is VCDRip which does the reverse operation, that is to
rip MPEG streams from images or burned VideoCDs and to show
information about a VideoCD.

%package libs
Summary:        Libraries for %{name}
Group:          System Environment/Libraries
Requires:       %{name} = %{version}-%{release}
# Introduced in F-9 to solve multilibs transition
Obsoletes:      vcdimager < 0.7.23-8

%description libs
The %{name}-libs package contains shared libraries for %{name}.

%package devel
Summary: Header files and library for VCDImager
Group: Development/Libraries
Requires: %{name}-libs = %{version}-%{release}
Requires: pkgconfig
Requires: libcdio-devel

%description devel
VCDImager allows you to create VideoCD BIN/CUE CD images from mpeg
files which can be burned with cdrdao or any other program capable of
burning BIN/CUE files.

This package contains the header files and a library to develop
applications that will use VCDImager.


%prep
%setup -q


%build
%configure --disable-static --disable-dependency-tracking
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install INSTALL="install -p"
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'

# Sometimes this file gets created... but we don't want it!
rm -f %{buildroot}%{_infodir}/dir


%clean
rm -rf %{buildroot}


%post libs -p /sbin/ldconfig

%post
for infofile in vcdxrip.info vcdimager.info vcd-info.info; do
  /sbin/install-info %{_infodir}/${infofile} %{_infodir}/dir 2>/dev/null || :
done

%preun
if [ $1 -eq 0 ]; then
  for infofile in vcdxrip.info vcdimager.info vcd-info.info; do
    /sbin/install-info --delete %{_infodir}/${infofile} %{_infodir}/dir \
      2>/dev/null || :
  done
fi

%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS BUGS ChangeLog* COPYING FAQ NEWS README THANKS TODO
%doc frontends/xml/videocd.dtd
%{_bindir}/*
%{_infodir}/vcdxrip.info*
%{_infodir}/vcdimager.info*
%{_infodir}/vcd-info.info*
%{_mandir}/man1/*

%files libs
%defattr(-,root,root,-)
%{_libdir}/libvcdinfo.so.*

%files devel
%defattr(-,root,root,-)
%doc HACKING
%{_includedir}/libvcd/
%{_libdir}/libvcdinfo.so
%{_libdir}/pkgconfig/libvcdinfo.pc


%changelog
* Mon Sep 01 2014 Sérgio Basto <sergio@serjux.com> - 0.7.24-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Feb 21 2014 Nicolas Chauvet <kwizart@gmail.com> - 0.7.24-7
- Rebuilt

* Wed Jan 30 2013 Nicolas Chauvet <kwizart@gmail.com> - 0.7.24-6
- Rebuilt for new libcdio

* Wed May 02 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.7.24-5
- Remove static statement in the devel sub-package - rfbz#2312

* Tue Apr 17 2012 Matthias Saou <matthias@saou.eu> 0.7.24-4
- Minor spec file cleanups.

* Wed Jan 25 2012 Nicolas Chauvet <kwizart@gmail.com> - 0.7.24-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Nov 23 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.7.24-2
- Rebuilt for libcdio update

* Thu Jun 09 2011 Nicolas Chauvet <kwizart@gmail.com> - 0.7.24-1
- Update to 0.7.24

* Sun Jan 24 2010 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.7.23-13
- Rebuild for libcdio

* Wed Nov 25 2009 Nicolas Chauvet <kwizart@fedoraproject.org> - 0.7.23-11
- Rebuild for F-12

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 0.7.23-10
- rebuild for new F11 features

* Thu Jan 15 2009 kwizart < kwizart at gmail.com > - 0.7.23-9
- Rebuild for libcdio 

* Thu Sep  4 2008 kwizart < kwizart at gmail.com > - 0.7.23-8
- Fix URL
- vcdimager-devel Requires libcdio-devel
- Split libs (multilibs compliance)

* Sat Aug 09 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> 0.7.23-7
- merge a few bits from livna spec

* Fri May 16 2008 Matthias Saou <http://freshrpms.net/> 0.7.23-6
- Rebuild for Fedora 9.
- Add missing ldconfig calls and scriplet info requirements.

* Sun Sep 24 2006 Matthias Saou <http://freshrpms.net/> 0.7.23-5
- Rebuild against new libcdio.

* Fri Mar 17 2006 Matthias Saou <http://freshrpms.net/> 0.7.23-4
- Release bump to drop the disttag number in FC5 build.

* Fri Jan 13 2006 Matthias Saou <http://freshrpms.net/> 0.7.23-3
- Silence install-info scriplets.

* Sat Jul 30 2005 Matthias Saou <http://freshrpms.net/> 0.7.23-2
- Rebuild against new libcdio.

* Tue Jul 12 2005 Matthias Saou <http://freshrpms.net/> 0.7.23-1
- Update to 0.7.23.
- Update libcdio-devel requirement to >= 0.72.
- Change source location from vcdimager.org to gnu.org for this release...

* Tue Jun 28 2005 Matthias Saou <http://freshrpms.net/> 0.7.22-2
- Prevent scriplets from failing if the info calls return an error.

* Tue May 17 2005 Matthias Saou <http://freshrpms.net/> 0.7.22-1
- Update to 0.7.22.

* Sun Apr 17 2005 Matthias Saou <http://freshrpms.net/> 0.7.21-1
- Update to 0.7.21 at last.
- Split off new -devel package.
- Added libcdio build requirement.
- Update Source URL, it's not "UNSTABLE" anymore.
- Remove vcddump.info and add vcd-info.info. Remove .gz from scriplets.

* Mon Aug 30 2004 Matthias Saou <http://freshrpms.net/> 0.7.14-4
- Added missing install-info calls.

* Mon May 24 2004 Matthias Saou <http://freshrpms.net/> 0.7.14-3
- Tried and update to 0.7.20, but the looping libcd* deps are a problem.
- Rebuild for Fedora Core 2.

* Fri Nov  7 2003 Matthias Saou <http://freshrpms.net/> 0.7.14-2
- Rebuild for Fedora Core 1.

* Fri May  2 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.7.14.
- Remove infodir/dir, thanks to Florin Andrei.
- Updated URL/Source.

* Mon Mar 31 2003 Matthias Saou <http://freshrpms.net/>
- Rebuilt for Red Hat Linux 9.

* Fri Feb 28 2003 Matthias Saou <http://freshrpms.net/>
- Update to 0.7.13.
- Removed the now unnecessary libxml fix.

* Tue Jan 14 2003 Matthias Saou <http://freshrpms.net/>
- Fix xmlversion.h include path in configure since xml is disabled otherwise,
  thanks to Rudolf Kastl for spotting the problem.

* Fri Jan  3 2003 Matthias Saou <http://freshrpms.net/>
- Let's try the 1 year old 0.7 development branch!

* Mon Dec  9 2002 Matthias Saou <http://freshrpms.net/>
- Spec file cleanup.

* Sat Jan 20 2001 Herbert Valerio Riedel <hvr@gnu.org>
- added THANKS file as doc

* Thu Jan  4 2001 Herbert Valerio Riedel <hvr@gnu.org>
- fixed removal of info pages on updating packages

* Sat Dec 23 2000 Herbert Valerio Riedel <hvr@gnu.org>
- added vcdrip
- removed glib dependancy

* Sat Aug 26 2000 Herbert Valerio Riedel <hvr@gnu.org>
- spec file improvements

* Mon Aug 14 2000 Herbert Valerio Riedel <hvr@gnu.org>
- first spec file

