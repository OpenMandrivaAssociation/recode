%define	major 0
%define libname %mklibname %{name} %{major}
%define develname %mklibname %{name} -d

Summary:	GNU recode
Name:		recode
Version:	3.6
Release:	26
Group:		Text tools
License:	GPL
URL:		http://recode.progiciels-bpi.ca/
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
BuildRequires:	gettext-devel
BuildRequires:	texinfo

%description
The GNU recode utility converts files between various character sets.

%package -n	%{libname}
Summary:	Shared GNU recode library
Group:          System/Libraries

%description -n	%{libname}
The GNU recode utility converts files between various character sets.

This package provides the shared recode library.

%package -n	%{develname}
Summary:	Development files for the %{libname} library
Group:		Development/C
Obsoletes:	%{name}-devel
Provides:	%{name}-devel
Provides:	lib%{name}-devel
Requires:	%{libname} = %{version}
Obsoletes:	%{mklibname %{name} 0 -d}

%description -n	%{develname}
Development files for the %{libname} library

%prep

%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p1
%patch3 -p1

%build
rm -f acinclude.m4
libtoolize --install --copy --force --automake
aclocal -I m4
autoconf
autoheader
automake --add-missing --copy

%configure2_5x \
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
%defattr(-,root,root)
%doc BACKLOG COPYING INSTALL NEWS README
%doc THANKS doc
%{_bindir}/*
%{_mandir}/man1/*
%{_infodir}/*

%files -n %{libname}
%defattr(0644,root,root,755)
%attr(0755,root,root) %{_libdir}/lib*.so.*

%files -n %{develname}
%defattr(0644,root,root,755)
%doc contrib
%{_libdir}/*.so
%{_libdir}/*.a
%{_includedir}/*.h


%changelog
* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 3.6-20mdv2011.0
+ Revision: 669414
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 3.6-19mdv2011.0
+ Revision: 607346
- rebuild

* Sun Mar 14 2010 Oden Eriksson <oeriksson@mandriva.com> 3.6-18mdv2010.1
+ Revision: 519065
- rebuild

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.6-17mdv2010.0
+ Revision: 426903
- rebuild

* Mon Dec 22 2008 Oden Eriksson <oeriksson@mandriva.com> 3.6-16mdv2009.1
+ Revision: 317141
- fix build with -Werror=format-security (P1)

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 3.6-15mdv2009.0
+ Revision: 265633
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - do not call ldconfig in %%post/%%postun, it is now handled by filetriggers

* Thu Apr 17 2008 Oden Eriksson <oeriksson@mandriva.com> 3.6-14mdv2009.0
+ Revision: 195239
- new debian patch
- fix devel naming

* Wed Mar 05 2008 Oden Eriksson <oeriksson@mandriva.com> 3.6-13mdv2008.1
+ Revision: 179430
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Thu Oct 12 2006 Oden Eriksson <oeriksson@mandriva.com>
+ 2006-10-11 13:02:29 (63479)
- bunzip patches

* Thu Oct 12 2006 Oden Eriksson <oeriksson@mandriva.com>
+ 2006-10-11 12:59:19 (63478)
Import recode

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 3.6-11mdk
- Rebuild

* Wed Jan 05 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 3.6-10mdk
- fix deps

* Sat Jan 01 2005 Christiaan Welvaart <cjw@daneel.dyndns.org> 3.6-9mdk
- add BuildRequires: automake1.4

* Wed Dec 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 3.6-8mdk
- revert latest "lib64 fixes"

* Wed Dec 29 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 3.6-7mdk
- lib64 fixes

* Tue May 11 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 3.6-6mdk
- use the debian patch instead, (fixing utf8 conversion + php anti
  symbol clash, translations, etc.)
- use --without-included-gettext and fix deps
- add -D_REENTRANT to CFLAGS

* Tue May 11 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 3.6-5mdk
- include the patch from fedora, (fixing utf8 conversion + php anti 
  symbol clash)
- merge static-devel sub package into the devel sub package
- libifiction
- misc spec file fixes

