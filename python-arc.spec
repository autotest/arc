%define shortname arc
%global commit 6a362442cc0cb05fef73ea6e4b157035ed097dc8
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Summary: Autotest RPC Client
Name: python-arc
Version: 0.2.0
Release: 2%{?dist}
License: GPLv2
Group: Development/Libraries
URL: http://github.com/clebergnu/arc
BuildArch: noarch
Source0: https://github.com/clebergnu/%{shortname}/archive/%{commit}/%{shortname}-%{version}-%{shortcommit}.tar.gz
BuildRequires: python2-devel
Requires: python

%description
Arc is the Autotest RPC Client. It provides libraries and tools that interact
with an Autotest RPC Server. It allows one to send test jobs, add test hosts,
query available tests, etc.

%prep
%setup -q -n %{shortname}-%{commit}
rm -rf %{buildroot}%{python_sitelib}/arc-*.egg-info

%build
%{__python} setup.py build

%install
%{__python} setup.py install --root %{buildroot} --skip-build

%files
%config(noreplace) %{_sysconfdir}/arc.conf
%doc README.md
%{python_sitelib}/arc
%{python_sitelib}/arc-*.egg-info
%{_bindir}/arcli

%changelog
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

