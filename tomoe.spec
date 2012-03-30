#
# Conditional build:
%bcond_without	python		# build without python bindings
%bcond_with	ruby		# build with ruby bindings
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Handwritten input system for Japanese and Chinese
Name:		tomoe
Version:	0.6.0
Release:	3
License:	LGPL v2+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/tomoe/%{name}-%{version}.tar.gz
# Source0-md5:	0e51e88d097085e101bf722fc04808ed
Patch0:		%{name}-multiarch-conflict.patch
Patch1:		%{name}-bz502662.patch
Patch2:		%{name}-svn-libs.patch
URL:		http://tomoe.sourceforge.jp/
BuildRequires:	gettext
BuildRequires:	glib2-devel
BuildRequires:	gtk-doc
BuildRequires:	intltool
BuildRequires:	libtool
BuildRequires:	perl(XML::Parser)
BuildRequires:	python
%if %{with python}
BuildRequires:	python-devel
BuildRequires:	python-pygobject-devel
BuildRequires:	python-pygtk-devel
%endif
%if %{with ruby}
BuildRequires:	ruby-gnome2-devel
%endif
BuildRequires:	apr-util-devel
BuildRequires:	hyperestraier-devel
BuildRequires:	mysql-devel
BuildRequires:	pakchois-devel
BuildRequires:	subversion-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A program which does Japanese handwriting recognition.

%package devel
Summary:	Tomoe development files
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The tomoe-devel package includes the header files for the tomoe
package. Install this package if you want to develop programs which
use tomoe.

%package static
Summary:	Tomoe static library
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Tomoe static library.

%package hyperestraier
Summary:	Hyper Estraier dictionary support for tomoe
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description hyperestraier
Hyper Estraier dictionary support for tomoe.

%package mysql
Summary:	Mysql dictionary support for tomoe
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description mysql
Mysql dictionary support for tomoe.

%package svn
Summary:	Subversion dictionary support for tomoe
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description svn
Subversion dictionary support for tomoe.

%package -n python-tomoe
Summary:	Tomoe bindings for python
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n python-tomoe
Tomoe bindings for python.

%package -n ruby-tomoe
Summary:	Tomoe bindings for ruby
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n ruby-tomoe
Tomoe bindings for ruby.

%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p1

%{__sed} 's|#!/usr/bin/env ruby|#!/usr/bin/ruby|' data/xml2est.rb

%build
%{__libtoolize}
%{__aclocal} -I macros
%{__autoconf}
%{__automake}
export CFLAGS="%{rpmcflags} -I/usr/include/apr-util"
%configure \
	%{!?with_static_libs:--disable-static} \
	--with-svn-lib=%{_libdir} \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/tomoe/module/{dict,recognizer}/*.{a,la}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/tomoe.{a,la}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README TODO data/kanjidic*.html
%dir %{_sysconfdir}/tomoe
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/tomoe/config
%attr(755,root,root) %{_libdir}/libtomoe.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtomoe.so.[0-9]
%dir %{_libdir}/tomoe
%dir %{_libdir}/tomoe/module
%dir %{_libdir}/tomoe/module/dict
%attr(755,root,root) %{_libdir}/tomoe/module/dict/unihan.so
%attr(755,root,root) %{_libdir}/tomoe/module/dict/xml.so
%dir %{_libdir}/tomoe/module/recognizer
%attr(755,root,root) %{_libdir}/tomoe/module/recognizer/simple.so
%dir %{_datadir}/tomoe
%dir %{_datadir}/tomoe/dict
%dir %{_datadir}/tomoe/recognizer
%{_datadir}/tomoe/recognizer/*.xml
%{_datadir}/tomoe/dict.dtd

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtomoe.so
%{_includedir}/tomoe
%{_pkgconfigdir}/tomoe.pc
%{_gtkdocdir}/tomoe

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libtomoe.a
%endif

%files hyperestraier
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/tomoe/module/dict/est.so

%files mysql
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/tomoe/module/dict/mysql.so

%files svn
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/tomoe/module/dict/svn.so

%if %{with ruby}
%files -n ruby-tomoe
%defattr(644,root,root,755)
%{ruby_archdir}
%{_libdir}/ruby/site_ruby/1.8/tomoe.rb
%{_libdir}/ruby/site_ruby/1.8/*-linux/*
%attr(755,root,root) %{_datadir}/tomoe/xml2est.rb
%endif

%if %{with python}
%files -n python-tomoe
%defattr(644,root,root,755)
%{_pkgconfigdir}/pytomoe.pc
%attr(755,root,root) %{py_sitedir}/tomoe.so
%{_datadir}/tomoe/python
%endif
