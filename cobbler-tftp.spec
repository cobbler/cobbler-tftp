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

%if 0%{?suse_version} > 1500
%bcond_without libalternatives
%else
%bcond_with libalternatives
%endif

%define python_package_name cobbler_tftp

%{?sle15_python_module_pythons}
Name:           cobbler-tftp
Version:        0.0.0+git.1705312236.c60217f
Release:        0
Summary:        The TFTP server daemon for Cobbler
License:        GPL-2.0-or-later
URL:            https://github.com/cobbler/cobbler-tftp
Source0:        %{name}-%{version}.tar.gz

%if 0%{?suse_version}
BuildRequires:  python-rpm-macros
%endif

BuildRequires:  fdupes
BuildRequires:  git
BuildRequires:  %{python_module pip}
BuildRequires:  %{python_module setuptools}
BuildRequires:  %{python_module setuptools_scm}
BuildRequires:  %{python_module wheel}

Requires:       python3-fbtftp
Requires:       python3-python-daemon
Requires:       python3-PyYAML
Requires:       python3-click
Requires:       python3-importlib-metadata
Requires:       python3-importlib-resources
Requires:       python3-schema
%if %{with libalternatives}
Requires:       alts
BuildRequires:  alts
%else
Requires(post):   update-alternatives
Requires(postun): update-alternatives
%endif
BuildArch:      noarch
%python_subpackages

%description
Cobbler-TFTP is a lightweight CLI application written in Python that serves as a stateless TFTP server.
It seamlessly integrates with Cobbler to generate and serve boot configuration files dynamically to managed machines.

%prep
%autosetup

%build
cp -r %{_sourcedir}/cobbler-tftp-%{version}/.git %{_builddir}/cobbler-tftp-%{version}
%pyproject_wheel

%install
%pyproject_install
%python_clone -a %{buildroot}%{_bindir}/cobbler-tftp
%python_expand %fdupes %{buildroot}%{$python_sitelib}

%pre
%python_libalternatives_reset_alternative cobbler-tftp

%post
%python_install_alternative cobbler-tftp

%postun
%python_uninstall_alternative cobbler-tftp

%files %{python_files}
%license LICENSE
%doc README.md
%python_alternative %{_bindir}/cobbler-tftp
%{_bindir}/cobbler-tftp-%{python_bin_suffix}
%{python_sitelib}/%{python_package_name}
%{python_sitelib}/%{python_package_name}-*.dist-info

%changelog

