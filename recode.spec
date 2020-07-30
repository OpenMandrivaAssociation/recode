%define major 3
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d
%define _disable_rebuild_configure 1
%define _disable_lto 1
%ifnarch riscv64
%global optflags %{optflags} -D_REENTRANT -fPIC --rtlib=compiler-rt
%endif

Summary:	GNU recode
Name:		recode
Version:	3.7.7
Release:	1
Group:		Text tools
License:	GPLv2
Url:		https://github.com/rrthomas/recode
Source0:	https://github.com/rrthomas/recode/releases/download/v%{version}/%{name}-%{version}.tar.gz
Patch0:		recode-3.7-check-for-__builtin_mul_overflow_p.patch
BuildRequires:	libtool
BuildRequires:	flex
BuildRequires:	texinfo
BuildRequires:	gettext-devel
BuildRequires:	pkgconfig(python)
BuildRequires:	help2man
BuildRequires:	perl-Locale-gettext

%description
The GNU recode utility converts files between various character sets.

%package -n %{libname}
Summary:	Shared GNU recode library
Group:		System/Libraries

%description -n %{libname}
This package provides the shared recode library.

%package -n %{devname}
Summary:	Development files for the %{libname} library
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
Development files for the %{libname} library.

%prep
%autosetup -p1

%build
export CFLAGS="%{optflags} -D_REENTRANT -fPIC"
autoreconf -fiv

%configure \
	--disable-static \
	--without-included-gettext

%make_build -j1

%install
%make_install

%find_lang %{name}

# house cleansing
rm -f %{buildroot}%{_infodir}/dir

# we don't want these
find %{buildroot} -name '*.la' -delete

%files -f %{name}.lang
%doc COPYING INSTALL NEWS README
%{_bindir}/*
%{_mandir}/man1/*
%{_infodir}/*

%files -n %{libname}
%{_libdir}/librecode.so.%{major}*

%files -n %{devname}
%doc contrib
%{_libdir}/librecode.so
%{_includedir}/*.h
