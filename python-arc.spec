%define shortname arc
%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Summary: Autotest RPC Client
Name: python-arc
Version: 0.0.2
Release: 1%{?dist}
License: GPLv2
Group: Development/Libraries
URL: http://autotest.github.com
BuildArch: noarch
#Source0: %{name}-%{version}.tar.gz
Source0: %{shortname}-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
Requires: python >= 2.7

%description
Arc is the Autotest RPC Client, a library and command line API for controlling an Autotest RPC Server.

It allows one to send test jobs, add machine hosts, etc.

%prep
%setup -q -n %{shortname}-%{version}

%build
python setup.py build

%install
rm -rf %{buildroot}
python setup.py install --root %{buildroot} --skip-build
rm -rf %{buildroot}%{python_sitelib}/arc-*.egg-info

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/arc.conf
%{python_sitelib}/arc
%{_bindir}/arcli
%doc


%changelog
* Tue Feb 19 2013 Cleber <cleber@redhat.com> - 0.0.2-1
- Updated to version 0.0.2

* Tue Oct 16 2012 Cleber Rosa <cleber@redhat.com> - python-arc.0.0.0-1
- Initial build.

