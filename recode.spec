%define	major 0
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

Summary:	GNU recode
Name:		recode
Version:	3.6
Release:	32
Group:		Text tools
License:	GPLv2
Url:		http://recode.progiciels-bpi.ca/
Source0:	ftp://prep.ai.mit.edu:/pub/gnu/recode/recode-%{version}.tar.bz2
# OE: taken from debian, but symbol clash fix originates from here:
# http://www.pybliographer.org/help/recode.patch
# recode and mysql symbols collided and made php crash, this patch
# fixes this.
Patch0:		recode_3.6-15.diff
Patch1:		recode-3.6-format_not_a_string_literal_and_no_format_arguments.diff
Patch2:		recode-automake.patch
Patch3:		recode-flex-m4.patch
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
%apply_patches

rm -f acinclude.m4
autoreconf -fi

%build
# http://clang.debian.net/status.php?version=3.3&key=UNDEF_REF
# fail with clang
export CC="gcc"
%configure \
	--disable-static \
	--without-included-gettext

# no -recheck hack
touch *

%make CFLAGS="%{optflags} -D_REENTRANT -fPIC"

%install
%makeinstall_std

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

