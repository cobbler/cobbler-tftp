#
# spec file for package cobbler-tftp
#
# Copyright (c) 2025 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#

%define python_package_name cobbler_tftp

%if 0%{?fedora} || 0%{?rhel}
%define python_daemon_name python3-daemon
%else
%define python_daemon_name python3-python-daemon
%endif

%if 0%{?suse_version}
%{?single_pythons_311plus}
%endif

%global __python %{__python3}

Name:           cobbler-tftp
Version:        0
Release:        0
Summary:        The TFTP server daemon for Cobbler
License:        GPL-2.0-or-later
URL:            https://github.com/cobbler/cobbler-tftp
Source0:        %{name}-%{version}.tar.gz

%if 0%{?suse_version}
BuildRequires:  python-rpm-macros
BuildRequires:  systemd-rpm-macros
%endif
%if 0%{?fedora} || 0%{?rhel}
# Provides %%pyproject_wheel / %%pyproject_install, the Fedora/RHEL equivalent
# of SUSE's python-rpm-macros pyproject buildsystem macros
BuildRequires:  pyproject-rpm-macros
%endif

BuildRequires:  fdupes
BuildRequires:  git
BuildRequires:  python3-devel >= 3.11
BuildRequires:  python3-pip
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm >= 8.0.0
BuildRequires:  python3-wheel
BuildRequires:  python3-fbtftp
BuildRequires:  %{python_daemon_name}
BuildRequires:  python3-PyYAML
BuildRequires:  python3-click
BuildRequires:  python3-schema

Requires:       python3-fbtftp
Requires:       %{python_daemon_name}
Requires:       python3-PyYAML
Requires:       python3-click
Requires:       python3-schema
BuildArch:      noarch

%if 0%{?fedora} || 0%{?rhel}
# https://docs.fedoraproject.org/en-US/packaging-guidelines/Python/#Automatically-generated-dependencies
# Disable it because it trips over python3-cheetah
%{?python_disable_dependency_generator}
%endif

%description
Cobbler-TFTP is a lightweight CLI application written in Python that serves as a stateless TFTP server.
It seamlessly integrates with Cobbler to generate and serve boot configuration files dynamically to managed machines.

%prep
%autosetup -p1

%build
cp -r %{_sourcedir}/cobbler-tftp-%{version}/.git %{_builddir}/cobbler-tftp-%{version}
%if 0%{?fedora} || 0%{?rhel}
%{python3} -m setuptools_scm --force-write-version-files
%else
%python_exec -m setuptools_scm --force-write-version-files
%endif
%pyproject_wheel

%install
%pyproject_install
%if 0%{?fedora} || 0%{?rhel}
PYTHONPATH=%{buildroot}%{python3_sitelib} %{buildroot}%{_bindir}/cobbler-tftp setup --systemd-dir=%{_unitdir} --install-prefix=%{buildroot}
%else
%python_expand PYTHONPATH=%{buildroot}%{$python_sitelib} %{buildroot}%{_bindir}/cobbler-tftp setup --systemd-dir=%{_unitdir} --install-prefix=%{buildroot}
%fdupes %{buildroot}%{_prefix}
%endif

%pre
%service_add_pre cobbler-tftp.service

%post
%service_add_post cobbler-tftp.service

%preun
%service_del_preun cobbler-tftp.service

%postun
%service_del_postun cobbler-tftp.service

%files
%license LICENSE
%doc README.md
%{_bindir}/cobbler-tftp
%{python_sitelib}/%{python_package_name}
%{python_sitelib}/%{python_package_name}-*.dist-info
%config /etc/cobbler-tftp
%{_unitdir}/cobbler-tftp.service

%changelog

