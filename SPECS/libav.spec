#globals for libav-11.4-20160223-0069d45.tar.xz
%global gitdate 20160223
%global gitversion 0069d45
%global snapshot %{gitdate}-%{gitversion}
%global gver .%{gitdate}git%{gitversion}

Name:           libav
Version:        11.4
Release: 	1%{?gver}%{?dist}
Summary:        Cross-platform solution to record, convert and stream audio/video
Group:          Productivity/Multimedia/Video/Editors and Convertors
Url:            http://libav.org
Source:         libav-%{version}-%{snapshot}.tar.xz
Source1:	libav-snapshot.sh
License:        GPL-2.0+
BuildRequires:	yasm-devel
BuildRequires:	make
BuildRequires:  pkgconfig
BuildRequires:	git
BuildRequires:	openssl-devel
BuildRequires:	libva-devel >= 0.31.0
BuildRequires:	libvdpau-devel
BuildRequires:  zlib-devel
BuildRequires: 	frei0r-devel
BuildRequires:  gnutls-devel
BuildRequires:	libbs2b-devel
BuildRequires: 	libcdio-paranoia-devel
BuildRequires:  libdc1394-devel
BuildRequires: 	faac-devel
BuildRequires:	fdk-aac-devel
BuildRequires:  freetype-devel
BuildRequires:  gsm-devel
BuildRequires:	ilbc-devel
BuildRequires:  lame-devel >= 3.98.3
BuildRequires: 	opencore-amr-devel vo-amrwbenc-devel
BuildRequires:	opencv-devel
BuildRequires:  openjpeg-devel
BuildRequires:  opus-devel
BuildRequires:	pulseaudio-libs-devel
BuildRequires:	librtmp-devel
BuildRequires:  schroedinger-devel
BuildRequires:  speex-devel
BuildRequires:  libtheora-devel
BuildRequires:	twolame-devel
BuildRequires:	vo-aacenc
BuildRequires:  libvorbis-devel
BuildRequires:	x264-devel >= 0.0.0-0.31
BuildRequires:	x265-devel
BuildRequires:  xvidcore-devel
BuildRequires:	libXext-devel
BuildRequires:	libXfixes-devel
Requires:       libav-libs = %{version}-%{release}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
Libav is a complete, cross-platform solution to record, convert and stream audio and video. It includes libavcodec - the leading audio/video codec library.

%package        libs
Summary:        Libraries for libav

%description    libs
This package contains the libraries for libav.

%package devel
Summary:        Cross-platform to record, convert, stream media files - Devel package
Group:          Development/Libraries/Other
Requires:       libav = %{version}-%{release}


%description devel
Libav is a complete, cross-platform solution to record, convert and stream audio and video.

%prep
%setup -n libav

./configure \
	--prefix=/usr \
	--libdir=%{_libdir}/libav  \
	--shlibdir=%{_libdir}/libav  \
	--enable-debug \
	--enable-shared \
	--enable-openssl \
	--enable-nonfree \
	--enable-gpl \
	--enable-version3 \
	--enable-vdpau \
	--enable-vaapi \
	--enable-bzlib \
	--enable-frei0r \
	--enable-gnutls \
	--enable-libbs2b \
	--enable-libcdio \
	--enable-libdc1394 \
	--enable-libfaac \
	--enable-libfdk-aac \
	--enable-libfdk-aac \
	--enable-libfreetype \
	--enable-libgsm \
	--enable-libilbc \
	--enable-libmp3lame \
	--enable-libopencore-amrnb \
	--enable-libopencore-amrwb \
	--enable-libopencv \
	--enable-libopenjpeg \
	--enable-libopus \
	--enable-libpulse \
	--enable-librtmp \
	--enable-libschroedinger \
	--enable-libspeex \
	--enable-libtheora \
	--enable-libtwolame \
	--enable-libvo-aacenc \
	--enable-libvo-aacenc \
	--enable-libvo-amrwbenc \
	--enable-libvorbis \
	--enable-libx264 \
	--enable-libx265 \
	--enable-libxvid \
	--enable-x11grab

%build
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{_bindir}/avconv
%{_bindir}/avprobe
%{_datadir}/avconv/libvpx-1080p.avpreset
%{_datadir}/avconv/libvpx-1080p50_60.avpreset
%{_datadir}/avconv/libvpx-360p.avpreset
%{_datadir}/avconv/libvpx-720p.avpreset
%{_datadir}/avconv/libvpx-720p50_60.avpreset
%{_datadir}/avconv/libx264-baseline.avpreset
%{_datadir}/avconv/libx264-fast.avpreset
%{_datadir}/avconv/libx264-fast_firstpass.avpreset
%{_datadir}/avconv/libx264-faster.avpreset
%{_datadir}/avconv/libx264-faster_firstpass.avpreset
%{_datadir}/avconv/libx264-ipod320.avpreset
%{_datadir}/avconv/libx264-ipod640.avpreset
%{_datadir}/avconv/libx264-lossless_fast.avpreset
%{_datadir}/avconv/libx264-lossless_max.avpreset
%{_datadir}/avconv/libx264-lossless_medium.avpreset
%{_datadir}/avconv/libx264-lossless_slow.avpreset
%{_datadir}/avconv/libx264-lossless_slower.avpreset
%{_datadir}/avconv/libx264-lossless_ultrafast.avpreset
%{_datadir}/avconv/libx264-main.avpreset
%{_datadir}/avconv/libx264-medium.avpreset
%{_datadir}/avconv/libx264-medium_firstpass.avpreset
%{_datadir}/avconv/libx264-placebo.avpreset
%{_datadir}/avconv/libx264-placebo_firstpass.avpreset
%{_datadir}/avconv/libx264-slow.avpreset
%{_datadir}/avconv/libx264-slow_firstpass.avpreset
%{_datadir}/avconv/libx264-slower.avpreset
%{_datadir}/avconv/libx264-slower_firstpass.avpreset
%{_datadir}/avconv/libx264-superfast.avpreset
%{_datadir}/avconv/libx264-superfast_firstpass.avpreset
%{_datadir}/avconv/libx264-ultrafast.avpreset
%{_datadir}/avconv/libx264-ultrafast_firstpass.avpreset
%{_datadir}/avconv/libx264-veryfast.avpreset
%{_datadir}/avconv/libx264-veryfast_firstpass.avpreset
%{_datadir}/avconv/libx264-veryslow.avpreset
%{_datadir}/avconv/libx264-veryslow_firstpass.avpreset
%{_mandir}/man1/avconv.1.gz
%{_mandir}/man1/avprobe.1.gz

%files libs
%{_libdir}/libav/libavcodec.so
%{_libdir}/libav/libavcodec.so.56
%{_libdir}/libav/libavcodec.so.56.1.0
%{_libdir}/libav/libavdevice.so
%{_libdir}/libav/libavdevice.so.55
%{_libdir}/libav/libavdevice.so.55.0.0
%{_libdir}/libav/libavfilter.so
%{_libdir}/libav/libavfilter.so.5
%{_libdir}/libav/libavfilter.so.5.0.0
%{_libdir}/libav/libavformat.so
%{_libdir}/libav/libavformat.so.56
%{_libdir}/libav/libavformat.so.56.1.0
%{_libdir}/libav/libavresample.so
%{_libdir}/libav/libavresample.so.2
%{_libdir}/libav/libavresample.so.2.1.0
%{_libdir}/libav/libavutil.so
%{_libdir}/libav/libavutil.so.54
%{_libdir}/libav/libavutil.so.54.3.0
%{_libdir}/libav/libswscale.so
%{_libdir}/libav/libswscale.so.3
%{_libdir}/libav/libswscale.so.3.0.0

%files devel
%{_libdir}/libav/pkgconfig/libavcodec.pc
%{_libdir}/libav/pkgconfig/libavdevice.pc
%{_libdir}/libav/pkgconfig/libavfilter.pc
%{_libdir}/libav/pkgconfig/libavformat.pc
%{_libdir}/libav/pkgconfig/libavresample.pc
%{_libdir}/libav/pkgconfig/libavutil.pc
%{_libdir}/libav/pkgconfig/libswscale.pc
%{_libdir}/libav/libav*.a
%{_libdir}/libav/libswscale.a
%{_includedir}/libavcodec/
%{_includedir}/libavdevice/
%{_includedir}/libavfilter/
%{_includedir}/libavformat/
%{_includedir}/libavresample/
%{_includedir}/libavutil/
%{_includedir}/libswscale/


%changelog
* Mon Feb 22 2016 David Vasquez <davidjeremias82[AT]gmail [DOT] com> - 11.4-20160223-0069d45-1
- Initial package of libav 11.4-20160223-0069d45
