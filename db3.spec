#
# Conditional build:
%bcond_with	java		# build with java support
#
Summary:	BSD database library for C
Summary(pl.UTF-8):	Biblioteka C do obsługi baz Berkeley DB
Name:		db3
Version:	3.3.11
Release:	0.1
License:	BSD
Group:		Libraries
# alternative site (sometimes working): http://www.berkeleydb.com/
#Source0Download: http://dev.sleepycat.com/downloads/releasehistorybdb.html
Source0:	http://downloads.sleepycat.com/db-%{version}.tar.gz
# Source0-md5:	b6ae24fa55713f17a9ac3219d987722c
Source1:	%{name}.jar
# Source1-md5:	0d15818dea3099eed42b4be9950c69ad
Patch0:		%{name}-static.patch
Patch1:		%{name}-linux.patch
Patch2:		%{name}-jbj.patch
URL:		http://www.sleepycat.com/
BuildRequires:	db1-static
BuildRequires:	glibc-static
%{?with_java:BuildRequires:	java}
BuildRequires:	tcl-devel >= 8.3.4-10
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. Berkeley DB is used by many applications,
including Python and Perl, so this should be installed on all systems.

%description -l pl.UTF-8
Berkeley Database (Berkeley DB) to zestaw narzędzi programistycznych
zapewniających obsługę baz danych w aplikacjach tradycyjnych jak i
klient-serwer. Berkeley db jest używana wielu aplikacjach, w tym w
Pythonie i Perlu.

%package utils
Summary:	Command line tools for managing Berkeley DB databases
Summary(pl.UTF-8):	Narzędzia do obsługi baz Berkeley DB z linii poleceń
Group:		Applications/Databases
Requires:	%{name} = %{version}-%{release}

%description utils
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching and database
recovery. DB supports C, C++, Java and Perl APIs.

This package contains command line tools for managing Berkeley DB
databases.

%description utils -l pl.UTF-8
Berkeley Database (Berkeley DB) to zestaw narzędzi programistycznych
zapewniających obsługę baz danych w aplikacjach tradycyjnych jak i
klient-serwer. Berkeley DB obsługuje dostęp do bazy przez B-drzewa i
funkcje mieszające ze stałą lub zmienną wielkością rekordu,
transakcje, kroniki, pamięć dzieloną i odtwarzanie baz. Ma wsparcie
dla C, C++, Javy i Perla.

Ten pakiet zawiera narzędzia do obsługi baz Berkeley DB z linii
poleceń.

%package tcl
Summary:	Berkeley database library for Tcl
Summary(pl.UTF-8):	Biblioteka baz danych Berkeley dla Tcl
Group:		Development/Languages/Tcl
Requires:	%{name} = %{version}-%{release}
Requires:	tcl

%description tcl
Berkeley database library for Tcl.

%description tcl -l pl.UTF-8
Biblioteka baz danych Berkeley dla Tcl.

%package java
Summary:	Java Berkeley database library
Summary(pl.UTF-8):	Biblioteki Berkeley Database dla Javy
Group:		Libraries/Java
Requires:	%{name} = %{version}-%{release}

%description java
Java Berkeley database library.

%description java -l pl.UTF-8
Biblioteki Berkeley Database dla Javy.

%package devel
Summary:	Header files for Berkeley database library
Summary(pl.UTF-8):	Pliki nagłówkowe do biblioteki Berkeley Database
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching and database
recovery. DB supports C, C++, Java and Perl APIs.

This package contains the header files, libraries, and documentation
for building programs which use Berkeley DB.

%description devel -l pl.UTF-8
Berkeley Database (Berkeley DB) to zestaw narzędzi programistycznych
zapewniających obsługę baz danych w aplikacjach tradycyjnych jak i
klient-serwer. Berkeley DB obsługuje dostęp do bazy przez B-drzewa i
funkcje mieszające ze stałą lub zmienną wielkością rekordu,
transakcje, kroniki, pamięć dzieloną i odtwarzanie baz. Ma wsparcie
dla C, C++, Javy i Perla.

Ten pakiet zawiera pliki nagłówkowe i dokumentację do budowania
programów używających Berkeley DB.

%package static
Summary:	Static libraries for Berkeley database library
Summary(pl.UTF-8):	Statyczne biblioteki Berkeley Database
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
The Berkeley Database (Berkeley DB) is a programmatic toolkit that
provides embedded database support for both traditional and
client/server applications. Berkeley DB includes B+tree, Extended
Linear Hashing, Fixed and Variable-length record access methods,
transactions, locking, logging, shared memory caching and database
recovery. DB supports C, C++, Java and Perl APIs.

This package contains the static libraries for building programs which
use Berkeley DB.

%description static -l pl.UTF-8
Berkeley Database (Berkeley DB) to zestaw narzędzi programistycznych
zapewniających obsługę baz danych w aplikacjach tradycyjnych jak i
klient-serwer. Berkeley DB obsługuje dostęp do bazy przez B-drzewa i
funkcje mieszające ze stałą lub zmienną wielkością rekordu,
transakcje, kroniki, pamięć dzieloną i odtwarzanie baz. Ma wsparcie
dla C, C++, Javy i Perla.

Ten pakiet zawiera statyczne biblioteki do budowania programów
używających Berkeley DB.

%prep
%setup -q -n db-%{version}
%patch -P0 -p1
#%%patch1 -p1
#%%patch2 -p1

%build
cp -a build_unix build_unix.static

cd build_unix.static

CFLAGS="%{rpmcflags} -fno-rtti -fno-implicit-templates" \
CXXFLAGS="%{rpmcflags} -fno-rtti -fno-implicit-templates" \
../dist/configure \
	--prefix=%{_prefix} \
	--enable-compat185 \
	--enable-dump185 \
	--enable-shared=no \
	--enable-static=yes \
	--enable-rpc \
	--enable-cxx

%{__make} static db_dump185
#libdb_cxx.a

cd ../build_unix

CFLAGS="%{rpmcflags} -fno-rtti -fno-implicit-templates" \
CXXFLAGS="%{rpmcflags} -fno-rtti -fno-implicit-templates" \
%if %{with java}
../dist/configure \
	--prefix=%{_prefix} \
	--enable-compat185 \
	--enable-shared=yes \
	--enable-static=no \
	--enable-rpc \
	--enable-cxx \
	--enable-tcl \
	--with-tcl=/usr/lib \
	--enable-java
%else
../dist/configure \
	--prefix=%{_prefix} \
	--enable-compat185 \
	--enable-shared=yes \
	--enable-static=no \
	--enable-rpc \
	--enable-cxx \
	--enable-tcl \
	--with-tcl=/usr/lib
%endif

%{__make} library_build \
	TCFLAGS='-I$(builddir) -I%{_includedir}'

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_includedir},%{_libdir},%{_bindir}}

cd build_unix.static

%{__make} prefix=$RPM_BUILD_ROOT%{_prefix} \
	install_static \
#	install_static_cxx

install db_dump185 $RPM_BUILD_ROOT%{_bindir}

cd ../build_unix

%if %{with java}
%{__make} \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	includedir=$RPM_BUILD_ROOT%{_includedir} \
	install_include \
	install_shared \
	install_tcl \
	install_utilities \
	install_java
#	install_dynamic_cxx \
%else
%{__make} \
	prefix=$RPM_BUILD_ROOT%{_prefix} \
	includedir=$RPM_BUILD_ROOT%{_includedir} \
	install_include \
	install_shared \
	install_tcl \
	install_utilities
#	install_dynamic_cxx \
%endif

# dunno if it's needed, but I think can help...
ln -sf libdb-3.3.so $RPM_BUILD_ROOT%{_libdir}/libdb.so
ln -sf libdb-3.3.so $RPM_BUILD_ROOT%{_libdir}/libdb3.so
ln -sf libdb-3.3.a $RPM_BUILD_ROOT%{_libdir}/libdb3.a
ln -sf libdb-3.3.a $RPM_BUILD_ROOT%{_libdir}/libdb.a
ln -sf libdb-3.3.so $RPM_BUILD_ROOT%{_libdir}/libndbm.so
ln -sf libdb-3.3.a $RPM_BUILD_ROOT%{_libdir}/libndbm.a

OLDPWD=$(pwd); cd $RPM_BUILD_ROOT%{_libdir}
for i in libdb*.la; do mv $i $i.old; done
sed -e "s/old_library=''/old_library='libdb-3.3.a'/" libdb-3.3.la.old > libdb-3.3.la
#sed -e "s/old_library=''/old_library='libdb_cxx.a'/" libdb_cxx-3.3.la.old > libdb_cxx-3.3.la
rm -f libdb*.la.old
cd $OLDPWD

for i in $RPM_BUILD_ROOT%{_bindir}/db_* ; do
	mv -f $i `echo $i | sed -e 's,/db_,/db3_,'`
done

cd ..

# to remove stupid link:
rm -rf examples_java

%if %{with java}
cp -ra java/src/com/sleepycat/examples examples_java
install %{SOURCE1} $RPM_BUILD_ROOT%{_libdir}/db.jar
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	tcl -p /sbin/ldconfig
%postun	tcl -p /sbin/ldconfig

%post	java -p /sbin/ldconfig
%postun	java -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README
%attr(755,root,root) %{_libdir}/libdb-*.so

%files utils
%defattr(644,root,root,755)
%doc docs/utility/*
%attr(755,root,root) %{_bindir}/berkeley_db_svc
%attr(755,root,root) %{_bindir}/db*_archive
%attr(755,root,root) %{_bindir}/db*_checkpoint
%attr(755,root,root) %{_bindir}/db*_deadlock
%attr(755,root,root) %{_bindir}/db*_dump
%attr(755,root,root) %{_bindir}/db*_dump185
%attr(755,root,root) %{_bindir}/db*_load
%attr(755,root,root) %{_bindir}/db*_printlog
%attr(755,root,root) %{_bindir}/db*_recover
%attr(755,root,root) %{_bindir}/db*_stat
%attr(755,root,root) %{_bindir}/db*_upgrade
%attr(755,root,root) %{_bindir}/db*_verify

%files tcl
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libdb_tcl-*.so

%if %{with java}
%files java
%defattr(644,root,root,755)
%doc docs/api_java examples_java
%attr(755,root,root) %{_libdir}/libdb_java*.so
%{_libdir}/db.jar
%endif

%files devel
%defattr(644,root,root,755)
%doc docs/{api_cxx,api_c,ref,index.html,sleepycat,images} examples_{c,cxx}
%attr(755,root,root) %{_libdir}/libdb.so
%attr(755,root,root) %{_libdir}/libdb3.so
%attr(755,root,root) %{_libdir}/libndbm.so
%attr(755,root,root) %{_libdir}/libdb_tcl.so
%{_libdir}/libdb*.la
#%attr(755,root,root) %{_libdir}/libdb_cxx*.so
%{_includedir}/*

%files static
%defattr(644,root,root,755)
%{_libdir}/lib*.a
