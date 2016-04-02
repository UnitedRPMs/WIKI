%define             fontdir %{_datadir}/fonts/%{name}
%define             catalogue %{_sysconfdir}/X11/fontpath.d

Name:               zvbi
Version:            0.2.35
Release:            1%{?dist}
Summary:            Raw VBI, Teletext and Closed Caption decoding library
Group:              System Environment/Libraries
# See NEWS for a full breakdown of licensing.
License:            LGPLv2+ and GPLv2+ and BSD
URL:                http://zapping.sourceforge.net/ZVBI/index.html
Source0:            http://downloads.sourceforge.net/zapping/%{name}-%{version}.tar.bz2
Patch0:             %{name}-0.2.24-tvfonts.patch
Patch1:             %{name}-0.2.25-openfix.patch

BuildRequires:      doxygen
BuildRequires:      fontconfig
BuildRequires:      gettext >= 0.16.1
BuildRequires:      libpng-devel
BuildRequires:      libICE-devel
BuildRequires:      xorg-x11-font-utils
BuildRequires:      systemd-units

Requires(post):     systemd-units
Requires(preun):    systemd-units
Requires(postun):   systemd-units


%description
ZVBI provides functions to capture and decode VBI data. The vertical blanking
interval (VBI) is an interval in a television signal that temporarily suspends
transmission of the signal for the electron gun to move back up to the first
line of the television screen to trace the next screen field. The vertical
blanking interval can be used to carry data, since anything sent during the VBI
would naturally not be displayed; various test signals, closed captioning, and
other digital data can be sent during this time period.


%package devel
Summary:            Development files for zvbi
Group:              Development/Libraries
Requires:           %{name} = %{version}-%{release}
Requires:           pkgconfig

%description devel
Development files for zvbi


%package fonts
Summary:            Fonts from zvbi converted to X11
Group:              User Interface/X
Requires(post):     fontconfig
Requires(postun):   fontconfig
BuildArch:	    noarch
Obsoletes:          xawtv-tv-fonts < 3.95
Provides:           xawtv-tv-fonts >= 3.95

%description fonts
Fonts from zvbi converted for use with X11


%prep
%setup -q
%patch0 -p1
%patch1 -p1

# Fix character encodings
iconv -f iso8859-1 README -t utf8 > README.conv && /bin/mv -f README.conv README

# systemd service file
cat >zvbid.service <<EOF
[Unit]
Description=Proxy Sharing V4L VBI Device Between Applications
After=syslog.target

[Service]
Type=forking
ExecStart=%{_sbindir}/zvbid

[Install]
WantedBy=multi-user.target

EOF


%build
# Note: We don't do --enable-static=no because static libs are needed to build
# x11font during compile time to convert zvbi fonts into x11 fonts. x11font
# is thrown away and not installed as it's not useful for anything else
%configure --disable-rpath --enable-v4l --enable-dvb --enable-proxy
make %{?_smp_mflags}

# Generate fonts, fonts.alias and fonts.dir
pushd contrib
./x11font
for font in *.bdf
do
    bdftopcf $font | gzip -9 -c > ${font%.bdf}.pcf.gz
done
mkfontdir -x .bdf .
cat >fonts.alias <<EOF
teletext   -ets-teletext-medium-r-normal--*-200-75-75-c-120-iso10646-1
EOF
popd


%install
mkdir -p %{buildroot}%{fontdir}
make install DESTDIR=%{buildroot}

%find_lang %{name}

mkdir -p %{buildroot}%{_unitdir}
install -m644 zvbid.service %{buildroot}%{_unitdir}
rm -rf %{buildroot}%{_initrddir}

install -pm0644 contrib/*.pcf.gz %{buildroot}%{fontdir}
install -pm0644 contrib/fonts.* %{buildroot}%{fontdir}
touch %{buildroot}%{fontdir}/fonts.cache-1

mkdir -p %{buildroot}%{catalogue}
ln -sf %{fontdir} %{buildroot}%{catalogue}/%{name}


%post
/sbin/ldconfig
%systemd_post zvbid.service


%preun
%systemd_preun zvbid.service


%postun
/sbin/ldconfig
%systemd_postun_with_restart zvbid.service


%post fonts
fc-cache -f %{_datadir}/fonts/%{name} || :


%postun fonts
if [ "$1" = "0" ]; then
    fc-cache -f %{_datadir}/fonts || :
fi


%files -f %{name}.lang
%{_bindir}/%{name}*
%{_sbindir}/zvbid
%{_unitdir}/zvbid.service
%{_libdir}/*.so.*
%{_mandir}/man1/*
%exclude %{_libdir}/*.a
%exclude %{_libdir}/*.la
%doc AUTHORS BUGS ChangeLog COPYING COPYING.LIB NEWS README TODO


%files devel
%{_includedir}/libzvbi.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/%{name}-0.2.pc


%files fonts
%dir %{_datadir}/fonts/%{name}
%{fontdir}/*.gz
%{fontdir}/fonts.dir
%{fontdir}/fonts.alias
%{catalogue}/%{name}
%ghost %{fontdir}/fonts.cache-1


%changelog
* Sun Feb 14 2016 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.2.35-1
- Update to 0.2.35

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.33-20
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.33-19
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Aug 18 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.33-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.33-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.33-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.33-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Mon Sep 24 2012 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.2.33-14
- new systemd-rpm macros (#850382)
- drop sysv triggerun migration

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.33-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.33-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 06 2011 Hans de Goede <hdegoede@redhat.com> - 0.2.33-11
- Fix build with libpng-1.5

* Tue Dec 06 2011 Adam Jackson <ajax@redhat.com> - 0.2.33-10
- Rebuild for new libpng

* Fri Sep 23 2011 Tom Callaway <spot@fedoraproject.org> - 0.2.33-9
- add missing triggerun for systemd migration

* Tue Sep  6 2011 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.2.33-8
- Drop chkconfig stuff completely

* Wed Aug 17 2011 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.2.33-7
- Migration from SysV to Systemd init system (#730154)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.33-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Feb 21 2010 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.2.33-5
- add patch to fix compiling under rawhide (#564991)
- make fonts subpackage arch independent

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.33-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Mar 25 2009 Dmitry Butskoy <Dmitry@Butskoy.name> - 0.2.33-3
- Rebuilt for #491975

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.33-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Nov 14 2008 Subhodip Biswas <subhodip@fedoraproject.org > - 0.2.33-1
- Package update .
* Sun Sep 21 2008 Ville Skyttä <ville.skytta at iki.fi> - 0.2.30-2
- Fix Patch0:/%%patch mismatch.

* Wed Mar 05 2008 Ian Chapman <packages[AT]amiga-hardware.com> 0.2.30-1
- Update to 0.2.30
- Updated license field due to license change GPLv2+ -> LGPLv2+
- Dropped encoding fixes for ChangeLog. No longer needed.

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.2.26-3
- Autorebuild for GCC 4.3

* Sun Jan 06 2008 Ian Chapman <packages[AT]amiga-hardware.com> 0.2.26-2
- Release bump

* Sun Jan 06 2008 Ian Chapman <packages[AT]amiga-hardware.com> 0.2.26-1
- Upgrade to 0.2.26

* Wed Aug 22 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.2.25-2
- Release bump for F8 mass rebuild
- License change due to new guidelines
- Use fontpath.d for F8+
- Added patch to fix compilation with open() macro on F8+

* Sun May 27 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.2.25-1
- Upgrade to 0.2.25

* Tue Mar 13 2007 Ian Chapman <packages[AT]amiga-hardware.com> 0.2.24-1
- Upgrade to 0.2.24
- Convert README and ChangeLog to UTF-8
- Added patch for x11font to generate more font sizes useful for other
  applications such as xawtv (courtesy of Dmitry Butskoy)
- Fonts sub-rpm now obsoletes and provides xawtv-tv-fonts
- Split font generation and font installation into separate sections
- Various other minor changes to the spec
- Added xfs support for the fonts

* Fri Sep 01 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.2.22-2
- Minor spec cleanups

* Tue Aug 29 2006 Ian Chapman <packages[AT]amiga-hardware.com> 0.2.22-1
- Initial release
