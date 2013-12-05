%define shortname arc
%global commit 75dcf4876a6d80f1b3787d8e909f98139c5dc48f
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Summary: Autotest RPC Client
Name: python-arc
Version: 0.5.0
Release: 1%{?dist}
License: GPLv2
Group: Development/Libraries
URL: http://github.com/autotest/arc
BuildArch: noarch
Source0: https://github.com/autotest/%{shortname}/archive/%{commit}/%{shortname}-%{version}-%{shortcommit}.tar.gz
BuildRequires: python2-devel, python-docutils, python-sphinx
Requires: python, python-pygments

%description
Arc is the Autotest RPC Client. It provides libraries and tools that interact
with an Autotest RPC Server. It allows one to send test jobs, add test hosts,
query available tests, etc.

%prep
%setup -q -n %{shortname}-%{commit}

%build
%{__python} setup.py build
%{__python} setup.py build_doc
%{__mv} build/sphinx/html api
%{__python} man/manpage-writer man/arcli.rst man/build/arcli.1

%install
%{__python} setup.py install --root %{buildroot} --skip-build
%{__mkdir} -p %{buildroot}%{_mandir}/man1
%{__install} -m 0644 man/build/arcli.1 %{buildroot}%{_mandir}/man1/arcli.1

%files
%config(noreplace) %{_sysconfdir}/arc.conf
%doc README.md LICENSE api
%{python_sitelib}/arc
%{python_sitelib}/arc-*.egg-info
%{_mandir}/man1/arcli.1.gz
%{_bindir}/arcli

%changelog
* Thu Sep 19 2013 Cleber Rosa <cleber@redhat.com> - 0.5.0-1
- Updated to version 0.5.0
- Change Source0 to reflect the project's new source code location
- Add API documentation to its own sub directory

* Sat Sep 14 2013 Cleber Rosa <cleber@redhat.com> - 0.4.0-1
- Updated to version 0.4.0
- Package now includes man page and API docs

* Thu Jul 25 2013 Cleber Rosa <cleber@redhat.com> - 0.3.0-1
- Updated to version 0.3.0

* Thu Jul 25 2013 Cleber Rosa <cleber@redhat.com> - 0.2.0-2
- Followed suggestions from Fedora package review

* Thu Jul 18 2013 Cleber Rosa <cleber@redhat.com> - 0.2.0-1
- Updated to version 0.2.0

* Tue Feb 19 2013 Cleber Rosa <cleber@redhat.com> - 0.0.2-2
- Replaced python commands for respective macros
- Add python as a build time requirement

* Tue Feb 19 2013 Cleber <cleber@redhat.com> - 0.0.2-1
- Updated to version 0.0.2

* Tue Oct 16 2012 Cleber Rosa <cleber@redhat.com> - python-arc.0.0.0-1
- Initial build.

