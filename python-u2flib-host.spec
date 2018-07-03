#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Python 2 based U2F host library
Summary(pl.UTF-8):	Biblioteka hosta U2F dla Pythona 2
Name:		python-u2flib-host
Version:	3.0.2
Release:	2
License:	BSD
Group:		Libraries/Python
Source0:	https://developers.yubico.com/python-u2flib-host/Releases/%{name}-%{version}.tar.gz
# Source0-md5:	f22297ce5aa5f14527b5c4b416b7f85b
URL:		https://developers.yubico.com/python-u2flib-host/
BuildRequires:	asciidoc
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-modules >= 1:2.7
BuildRequires:	python-setuptools
%if %{with tests}
BuildRequires:	python-cryptography >= 1.0
BuildRequires:	python-hidapi >= 0.7.99
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.3
BuildRequires:	python3-setuptools
%if %{with tests}
BuildRequires:	python3-cryptography >= 1.0
BuildRequires:	python3-hidapi >= 0.7.99
%endif
%endif
Requires:	python-hidapi >= 0.7.99
Requires:	python-modules >= 1:2.7
Requires:	python-requests
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# man pages common for both python versions
%define		_duplicate_files_terminate_build	0

%description
Provides library functionality for communicating with a U2F device
over USB.

Two executables are provided, u2f-register and u2f-authenticate, which
support the register and authenticate commands of U2F as defined in
the FIDO specifications
(<http://fidoalliance.org/specifications/download>).

%description -l pl.UTF-8
Pakiet zawiera bibliotekę funkcji do komunikowania się z urządzeniami
U2F po USB.

Dołączone są dwa programy: u2f-register oraz u2f-authenticate,
obsługujące polecenia U2F register i authenticate, zdefiniowane w
specyfikacji FIDO
(<http://fidoalliance.org/specifications/download>).

%package -n python3-u2flib-host
Summary:	Python 3 based U2F host library
Summary(pl.UTF-8):	Biblioteka hosta U2F dla Pythona 3
Group:		Libraries/Python
Requires:	python3-hidapi >= 0.7.99
Requires:	python3-modules >= 1:3.3
Requires:	python3-requests

%description -n python3-u2flib-host
Provides library functionality for communicating with a U2F device
over USB.

Two executables are provided, u2f-register and u2f-authenticate, which
support the register and authenticate commands of U2F as defined in
the FIDO specifications
(<http://fidoalliance.org/specifications/download>).

%description -n python3-u2flib-host -l pl.UTF-8
Pakiet zawiera bibliotekę funkcji do komunikowania się z urządzeniami
U2F po USB.

Dołączone są dwa programy: u2f-register oraz u2f-authenticate,
obsługujące polecenia U2F register i authenticate, zdefiniowane w
specyfikacji FIDO
(<http://fidoalliance.org/specifications/download>).

%prep
%setup -q

%build
%if %{with python2}
%py_build

%if %{with tests}
%{__python} -m unittest discover -s test
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
%{__python3} -m unittest discover -s test
%endif
%endif

cd man
for f in *.adoc ; do
	a2x -f manpage $f
done

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

for f in u2f-authenticate u2f-register ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/${f} $RPM_BUILD_ROOT%{_bindir}/${f}-2
done

%py_postclean
%endif

%if %{with python3}
%py3_install

for f in u2f-authenticate u2f-register ; do
	%{__mv} $RPM_BUILD_ROOT%{_bindir}/${f} $RPM_BUILD_ROOT%{_bindir}/${f}-3
done
%endif

install -d $RPM_BUILD_ROOT%{_mandir}/man1
cp -p man/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc COPYING ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/u2f-authenticate-2
%attr(755,root,root) %{_bindir}/u2f-register-2
%{py_sitescriptdir}/u2flib_host
%{py_sitescriptdir}/python_u2flib_host-%{version}-py*.egg-info
%{_mandir}/man1/u2f-authenticate.1*
%{_mandir}/man1/u2f-register.1*
%endif

%if %{with python3}
%files -n python3-u2flib-host
%defattr(644,root,root,755)
%doc COPYING ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/u2f-authenticate-3
%attr(755,root,root) %{_bindir}/u2f-register-3
%{py3_sitescriptdir}/u2flib_host
%{py3_sitescriptdir}/python_u2flib_host-%{version}-py*.egg-info
%{_mandir}/man1/u2f-authenticate.1*
%{_mandir}/man1/u2f-register.1*
%endif
