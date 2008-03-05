%define	major 0
%define libname	%mklibname %{name} %{major}

Summary:	GNU recode
Name:		recode
Version:	3.6
Release:	%mkrel 13
Group:		Text tools
License:	GPL
URL:		http://recode.progiciels-bpi.ca/
Source0:	ftp://prep.ai.mit.edu:/pub/gnu/recode/recode-%{version}.tar.bz2
# OE: taken from debian, but symbol clash fix originates from here:
# http://www.pybliographer.org/help/recode.patch
# recode and mysql symbols collided and made php crash, this patch
# fixes this.
Patch0:		recode_3.6-10.diff
BuildRequires:	flex
BuildRequires:	gettext-devel
BuildRequires:	automake1.4
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
The GNU recode utility converts files between various character sets.

%package -n	%{libname}
Summary:	Shared GNU recode library
Group:          System/Libraries

%description -n	%{libname}
The GNU recode utility converts files between various character sets.

This package provides the shared recode library.

%package -n	%{libname}-devel
Summary:	Development files for the %{libname} library
Group:		Development/C
Obsoletes:	%{name}-devel
Provides:	%{name}-devel
Provides:	lib%{name}-devel
Requires:	%{libname} = %{version}-%{release}

%description -n	%{libname}-devel
Development files for the %{libname} library

%prep

%setup -q
%patch0 -p1

%build

%configure2_5x \
     --without-included-gettext

# no -recheck hack
touch *

%make CFLAGS="%{optflags} -D_REENTRANT -fPIC"

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%makeinstall_std

%find_lang %{name}

# house cleansing
rm -f %{buildroot}%{_infodir}/dir

%post
%_install_info %{name}.info

%postun
%_remove_install_info %{name}.info

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%post -n %{libname}-devel -p /sbin/ldconfig

%postun -n %{libname}-devel -p /sbin/ldconfig

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc BACKLOG COPYING INSTALL NEWS README
%doc THANKS doc
%{_bindir}/*
%{_mandir}/man1/*
%{_infodir}/*

%files -n %{libname}
%defattr(0644,root,root,755)
%attr(0755,root,root) %{_libdir}/lib*.so.*

%files -n %{libname}-devel
%defattr(0644,root,root,755)
%doc contrib
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la
%{_includedir}/*.h

