#
# spec file for package cobbler-tftp
#
# Copyright (c) 2024 SUSE LLC
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

%define pythons python3
%{?sle15_python_module_pythons}
Name:           cobbler-tftp
Version:        %{version}
Release:        0
Summary:        The TFTP server daemon for Cobbler
License:        GPL-2.0-or-later
URL:            https://github.com/cobbler/cobbler-tftp
Source0:        %{name}-%{version}.tar.gz

%if 0%{?suse_version}
BuildRequires:  python-rpm-macros
BuildRequires:  systemd-rpm-macros
%endif

BuildRequires:  fdupes
BuildRequires:  git
BuildRequires:  %{python_module pip}
BuildRequires:  %{python_module setuptools}
BuildRequires:  %{python_module setuptools_scm}
BuildRequires:  %{python_module wheel}
BuildRequires:  %{python_module fbtftp}
BuildRequires:  %{python_module python-daemon}
BuildRequires:  %{python_module PyYAML}
BuildRequires:  %{python_module click}
BuildRequires:  %{python_module importlib-metadata}
BuildRequires:  %{python_module importlib-resources}
BuildRequires:  %{python_module schema}

Requires:       python3-fbtftp
Requires:       python3-python-daemon
Requires:       python3-PyYAML
Requires:       python3-click
Requires:       python3-importlib-metadata
Requires:       python3-importlib-resources
Requires:       python3-schema
BuildArch:      noarch

%description
Cobbler-TFTP is a lightweight CLI application written in Python that serves as a stateless TFTP server.
It seamlessly integrates with Cobbler to generate and serve boot configuration files dynamically to managed machines.

%prep
%autosetup

%build
cp -r %{_sourcedir}/cobbler-tftp-%{version}/.git %{_builddir}/cobbler-tftp-%{version}
%python_exec -m setuptools_scm --force-write-version-files
%pyproject_wheel

%install
%pyproject_install
%python_expand PYTHONPATH=%{buildroot}%{$python_sitelib} %{buildroot}%{_bindir}/cobbler-tftp setup --systemd-dir=%{_unitdir} --install-prefix=%{buildroot}
%fdupes %{buildroot}%{_prefix}

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

