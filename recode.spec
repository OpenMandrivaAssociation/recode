%define	major 0
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d
%define _disable_rebuild_configure 1
%define _disable_lto 1

Summary:	GNU recode
Name:		recode
Version:	3.7
Release:	1
Group:		Text tools
License:	GPLv2
Url:		https://github.com/rrthomas/recode
Source0:	https://github.com/rrthomas/recode/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildRequires:	flex
BuildRequires:	texinfo
BuildRequires:	gettext-devel

%description
The GNU recode utility converts files between various character sets.

%package -n	%{libname}
Summary:	Shared GNU recode library
Group:          System/Libraries

%description -n	%{libname}
This package provides the shared recode library.

%package -n	%{devname}
Summary:	Development files for the %{libname} library
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n	%{devname}
Development files for the %{libname} library.

%prep
%setup -q

%build
export CFLAGS="%{optflags} -D_REENTRANT -fPIC"
%configure \
	--disable-static \
	--without-included-gettext

# no -recheck hack
touch *

%make_build

%install
%make_install

%find_lang %{name}

# house cleansing
rm -f %{buildroot}%{_infodir}/dir

%files -f %{name}.lang
%doc BACKLOG COPYING INSTALL NEWS README
%doc THANKS doc
%{_bindir}/*
%{_mandir}/man1/*
%{_infodir}/*

%files -n %{libname}
%{_libdir}/librecode.so.%{major}*

%files -n %{devname}
%doc contrib
%{_libdir}/librecode.so
%{_includedir}/*.h

