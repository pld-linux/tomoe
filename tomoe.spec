#
# Conditional build:
%bcond_without	python		# build without Python bindings
%bcond_without	ruby		# build without Ruby bindings
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Handwritten input system for Japanese and Chinese
Summary(pl.UTF-8):	System wprowadzania pisma ręcznego dla japońskiego i chińskiego
Name:		tomoe
Version:	0.6.0
Release:	22
License:	LGPL v2+
Group:		Libraries
Source0:	http://downloads.sourceforge.net/tomoe/%{name}-%{version}.tar.gz
# Source0-md5:	0e51e88d097085e101bf722fc04808ed
Patch0:		%{name}-multiarch-conflict.patch
Patch1:		%{name}-bz502662.patch
Patch2:		%{name}-svn-libs.patch
Patch3:		%{name}-glib2.32.patch
Patch4:		%{name}-ruby.patch
Patch5:		%{name}-format.patch
Patch6:		am.patch
URL:		http://tomoe.sourceforge.jp/
BuildRequires:	apr-util-devel
BuildRequires:	autoconf >= 2.57
BuildRequires:	automake
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.4.0
BuildRequires:	gtk-doc >= 1.4
BuildRequires:	hyperestraier-devel
BuildRequires:	intltool >= 0.35.0
BuildRequires:	libtool
BuildRequires:	libxslt-progs
BuildRequires:	mysql-devel
BuildRequires:	pakchois-devel
BuildRequires:	perl-XML-Parser
BuildRequires:	pkgconfig
BuildRequires:	python
BuildRequires:	subversion-devel
%if %{with python}
BuildRequires:	python-devel
BuildRequires:	python-pygobject-devel
BuildRequires:	python-pygtk-devel >= 2:2.0
%endif
%if %{with ruby}
BuildRequires:	ruby-glib2-devel
%endif
Requires:	glib2 >= 1:2.4.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A program which does Japanese and Chinese handwriting recognition.

%description -l pl.UTF-8
Program rozpoznający japońskie i chińskie pismo ręczne.

%package devel
Summary:	Header files for tomoe library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki tomoe
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.4.0

%description devel
The tomoe-devel package includes the header files for the tomoe
package. Install this package if you want to develop programs which
use tomoe.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe biblioteki tomoe. Należy go
zainstalować, aby rozwijać programy wykorzystujące tomoe.

%package static
Summary:	Tomoe static library
Summary(pl.UTF-8):	Statyczna biblioteka tomoe
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Tomoe static library.

%description static -l pl.UTF-8
Statyczna biblioteka tomoe.

%package hyperestraier
Summary:	Hyper Estraier dictionary support for tomoe
Summary(pl.UTF-8):	Obsługa słowników Hyper Estraiera dla tomoe
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description hyperestraier
Hyper Estraier dictionary support for tomoe.

%description hyperestraier -l pl.UTF-8
Obsługa słowników Hyper Estraiera dla tomoe.

%package mysql
Summary:	MySQL dictionary support for tomoe
Summary(pl.UTF-8):	Obsługa słowników MySQL dla tomoe
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description mysql
MySQL dictionary support for tomoe.

%description mysql -l pl.UTF-8
Obsługa słowników MySQL dla tomoe.

%package svn
Summary:	Subversion dictionary support for tomoe
Summary(pl.UTF-8):	Obsługa słowników Subversion dla tomoe
Group:		Libraries
Requires:	%{name} = %{version}-%{release}

%description svn
Subversion dictionary support for tomoe.

%description svn -l pl.UTF-8
Obsługa słowników Subversion dla tomoe.

%package -n python-tomoe
Summary:	Tomoe bindings for Python
Summary(pl.UTF-8):	Wiązania tomoe dla Pythona
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-tomoe
Tomoe bindings for Python.

%description -n python-tomoe -l pl.UTF-8
Wiązania tomoe dla Pythona.

%package -n python-tomoe-devel
Summary:	Development files for Tomoe Python binding
Summary(pl.UTF-8):	Pliki programistyczne wiązań Pythona do Tomoe
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	python-tomoe = %{version}-%{release}
Requires:	python-pygobject-devel

%description -n python-tomoe-devel
Development files for Tomoe Python binding.

%description -n python-tomoe-devel -l pl.UTF-8
Pliki programistyczne wiązań Pythona do Tomoe.

%package -n ruby-tomoe
Summary:	Tomoe bindings for Ruby
Summary(pl.UTF-8):	Wiązania tomoe dla języka Ruby
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}
Requires:	ruby-glib2

%description -n ruby-tomoe
Tomoe bindings for Ruby.

%description -n ruby-tomoe -l pl.UTF-8
Wiązania tomoe dla języka Ruby.

%package -n ruby-tomoe-devel
Summary:	Header file for Ruby/Tomoe library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki Ruby/Tomoe
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}
Requires:	ruby-glib2-devel
Requires:	ruby-tomoe = %{version}-%{release}

%description -n ruby-tomoe-devel
Header file for Ruby/Tomoe library.

%description -n ruby-tomoe-devel -l pl.UTF-8
Plik nagłówkowy biblioteki Ruby/Tomoe.

%prep
%setup -q
%patch0 -p0
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%{__sed} -i -e 's|#!/usr/bin/env ruby|#!/usr/bin/ruby|' data/xml2est.rb

%build
%{__gtkdocize}
%{__libtoolize}
%{__aclocal} -I macros
%{__autoconf}
%{__automake}
export CFLAGS="%{rpmcflags} -I/usr/include/apr-util"
%configure \
	UNZIP=/usr/bin/unzip \
	%{!?with_static_libs:--disable-static} \
	%{?with_ruby:--with-ruby-bindingdir=%{ruby_vendorarchdir}} \
	%{?with_ruby:--with-ruby-libdir=%{ruby_vendorlibdir}} \
	--enable-gtk-doc \
	--with-html-dir=%{_gtkdocdir} \
	--with-svn-lib=%{_libdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/tomoe/dict

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/tomoe/module/{dict,recognizer}/*.{a,la}
%{__rm} $RPM_BUILD_ROOT%{py_sitedir}/tomoe.{a,la}
%{?with_ruby:%{__rm} $RPM_BUILD_ROOT%{ruby_vendorarchdir}/tomoe.{a,la}}

%if %{without ruby}
%{__rm} $RPM_BUILD_ROOT%{_datadir}/tomoe/xml2est.rb
%endif

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS NEWS README TODO data/kanjidic*.html
%dir %{_sysconfdir}/tomoe
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/tomoe/config
%attr(755,root,root) %{_libdir}/libtomoe.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtomoe.so.0
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
%{_datadir}/tomoe/recognizer/handwriting-*.xml
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

%if %{with python}
%files -n python-tomoe
%defattr(644,root,root,755)
%attr(755,root,root) %{py_sitedir}/tomoe.so

%files -n python-tomoe-devel
%defattr(644,root,root,755)
%dir %{_datadir}/tomoe/python
%{_datadir}/tomoe/python/tomoe.defs
%{_pkgconfigdir}/pytomoe.pc
%endif

%if %{with ruby}
%files -n ruby-tomoe
%defattr(644,root,root,755)
%attr(755,root,root) %{_datadir}/tomoe/xml2est.rb
%attr(755,root,root) %{ruby_vendorarchdir}/tomoe.so
%{ruby_vendorlibdir}/tomoe.rb

%files -n ruby-tomoe-devel
%defattr(644,root,root,755)
%{ruby_vendorarchdir}/rbtomoe.h
%endif
