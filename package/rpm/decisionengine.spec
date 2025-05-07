# SPDX-FileCopyrightText: 2017 Fermi Research Alliance, LLC
# SPDX-License-Identifier: Apache-2.0

# RPM package for HEPCloud DEcisionengine pre-requisites

# Disable shebang mangling (see GHI#436)
%undefine __brp_mangle_shebangs

# python3 == python3.9
%global python3_pkgversion 3

# Versions use semantic versioning (M.m.p)
# Release Candidates NVR format
# define release 0.1.rc1
# Official Release NVR format
# define release 2

%define auto_version %(FULLVER=$(git describe --tag | sed 's/-/_/g');  GVER=$(sed 's/.*_\\\([[:digit:]].*\\\)_/dev\\\1+/g' <<< ${FULLVER}); VER=${FULLVER//_*}; echo ${VER%.*}.$((${VER##*.}+1)).${GVER})
%define auto_release 1

%define version __HCDE_RPM_VERSION__
%define release __HCDE_RPM_RELEASE__

%define decisionengine_home %{_sharedstatedir}/decisionengine
#%define systemddir %{_prefix}/lib/systemd/system
%define src_de_base decisionengine
%define src_de_package %{src_de_base}/package

Name:           decisionengine
Version:        %{version}
Release:        %{release}%{?dist}
Summary:        HEPCloud DecisionEngine
License:        Apache-2.0
URL:            https://hepcloud.github.io/
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
Prefix:         %{_prefix}
Vendor:         Fermilab <None>

Source:         hepcloud.tar.gz

BuildRequires: python%{python3_pkgversion} >= 3.9
BuildRequires: python%{python3_pkgversion}-devel
BuildRequires: systemd
BuildRequires: git
BuildRequires: make
BuildRequires: openssl-devel
BuildRequires: gcc
BuildRequires: gcc-c++
BuildRequires: swig
#BuildRequires: python3-setuptools python3-wheel rpm-build

%description
The HEPCloud DecisionEngine provides a simple way to access the Grid, Cloud and HPC
resources through a dynamic HTCondor pool of grid-submitted resources.
It allows resource scheduling for disparate resource providers, including those
which may have a cost or a restricted allocation of cycles.

HEPCloud DecisionEngine is installed via PIP.
These RPMs provide all the pre-requisites and necessary setup.

Code documentation, release notes and install instructions are on github.io:
https://hepcloud.github.io/

#shadow-utils systemd python3.9dist(pip) python3.9dist(setuptools) python3.9dist(wheel) gcc gcc-c++ make python3.9-devel podman glideinwms-vofrontend-core glideinwms-vofrontend-glidein glideinwms-vofrontend-httpd glideinwms-vofrontend-libs glideinwms-userschedd glideinwms-usercollector


%package deps
Summary: The HEPCloud Decision Engine dependencies.
Requires: python%{python3_pkgversion} >= 3.9
# These were form the python packaging
Requires: shadow-utils
Requires: systemd
#Requires: python3.9dist(pip)
#Requires: python3.9dist(setuptools)
#Requires: python3.9dist(wheel)
# end form the python packaging
Requires: postgresql
Requires: postgresql-server
Requires: postgresql-devel
Requires: httpd
Requires: python3-cryptography
Requires: python3-pip
Requires: python3-jsonnet
Requires: gettext
# iptables-nft added to avoid podman pulling iptables-legacy (incompatible w/ EL9 kernels)
Requires: iptables-nft
Requires: podman
# For pip install git+https ...
Requires: git
# To add back if jsonnet RPM not available - Required to build jsonnet (make, g++, and Python.h) (TODO: put in pip a build for jsonnet)
#Requires: make
#Requires: gcc-c++
#Requires: python3-devel
Requires(post): /usr/sbin/useradd
%description deps
This subpackage includes all the RPM dependency for the HEPCloud Decision Engine Framework.


%package modules-deps
Summary: The HEPCloud Decision Engine Modules dependencies.
Requires: python%{python3_pkgversion} >= 3.9
Requires: decisionengine-deps = %{version}-%{release}
Requires: glideinwms-vofrontend-libs
Requires: glideinwms-vofrontend-glidein
Requires: glideinwms-vofrontend-core
Requires(post): /usr/sbin/usermod
%description modules-deps
This subpackage includes all the RPM dependency for the HEPCloud Decision Engine Modules.


%package standalone
Summary: The HEPCloud Decision Engine Modules dependencies and Web server
Requires: decisionengine-modules-deps = %{version}-%{release}
Requires: glideinwms-vofrontend-httpd
%description standalone
This package installs the RPM requirements and the Web server.


%package onenode
Summary: The HEPCloud Decision Engine Framework and Modules dependencies, and extra-services.
Requires: decisionengine-standalone = %{version}-%{release}
# These may actually be on another host
Requires: glideinwms-userschedd
Requires: glideinwms-usercollector
%description onenode
This subpackage includes all the RPM dependencies for the HEPCloud Decision Engine Framework and Modules
the Web server for the staged files, and the HTCondor CM and AP to manage the virtual cluster.


%prep
# Empty for now
%setup -q -n hepcloud
# Apply the patches here if any
#%patch -P 0 -p1


%build
#cp %{SOURCE7} .
#chmod 700 chksum.sh

%install
rm -rf $RPM_BUILD_ROOT

# Set the Python version
%global __python %{__python3}

# TODO: Check if some of the following are needed
# seems never used
# %define py_ver %(python -c "import sys; v=sys.version_info[:2]; print '%d.%d'%v")

# From http://fedoraproject.org/wiki/Packaging:Python
# Assuming python3_sitelib and python3_sitearch are defined, not supporting RHEL < 7 or old FC
# Define python_sitelib

# Create some directories, install config files, systemd and the binary wrapper
install -d $RPM_BUILD_ROOT%{decisionengine_home}
install -d $RPM_BUILD_ROOT%{decisionengine_home}/passwords.d
install -d $RPM_BUILD_ROOT%{decisionengine_home}/tokens.d
install -d $RPM_BUILD_ROOT%{_sysconfdir}/decisionengine
install -d $RPM_BUILD_ROOT%{_sysconfdir}/decisionengine/config.d
install -d $RPM_BUILD_ROOT%{_localstatedir}/log/decisionengine
install -m 0644 %{src_de_base}/config/decision_engine.jsonnet $RPM_BUILD_ROOT%{_sysconfdir}/decisionengine/
install -D -m 0644 %{src_de_package}/systemd/decisionengine.service $RPM_BUILD_ROOT%{_unitdir}/decisionengine.service
install -D -m 0644 %{src_de_package}/systemd/decisionengine_sysconfig $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/decisionengine
install -D -m 0755 %{src_de_package}/rpm/decisionengine-wrapper.sh $RPM_BUILD_ROOT%{_bindir}/decisionengine-wrapper.sh
install -D -m 0755 %{src_de_package}/rpm/decisionengine-install-python.sh $RPM_BUILD_ROOT%{_bindir}/decisionengine-install-python
# Add links to the wrapper script for all decisionengine binaries
pushd $RPM_BUILD_ROOT%{_bindir}
%{__ln_s} -f decisionengine-wrapper.sh decisionengine
%{__ln_s} -f decisionengine-wrapper.sh de-client
%{__ln_s} -f decisionengine-wrapper.sh de-logparser
%{__ln_s} -f decisionengine-wrapper.sh de-query-tool
%{__ln_s} -f decisionengine-wrapper.sh de-reaper
popd

%clean
rm -rf $RPM_BUILD_ROOT


%pre deps
# Add the "decisionengine" user and group if they do not exist
getent group decisionengine >/dev/null || groupadd -r decisionengine
getent passwd decisionengine >/dev/null || \
       useradd -r -g decisionengine -d %{decisionengine_home} \
	-c "HEPCloud Decision Engine user" -s /sbin/nologin decisionengine
# If the decisionengine user already exists make sure it is part of decisionengine group
usermod --append --groups decisionengine decisionengine >/dev/null

%pre modules-deps
# make sure decisionengine is part of glidein group
# glidein defined in glideinwms-vofrontend-glidein requirement
usermod --append --groups glidein decisionengine >/dev/null

%post deps
# make sure our home area makes sense since we have a dynamic id
chown decisionengine:decisionengine %{decisionengine_home}
chmod 750 %{decisionengine_home}
# If the decisionengine user already exists make sure it is part of
# the decisionengine group
usermod --append --groups decisionengine decisionengine >/dev/null
# Change the ownership of log and lock dir if they already exist
if [ -d %{_localstatedir}/log/decisionengine ]; then
    chown -R decisionengine:decisionengine %{_localstatedir}/log/decisionengine
fi
# Failsafe for container without systemd
systemctl daemon-reload || true


%postun deps
# Failsafe for container without systemd
systemctl daemon-reload || true


%files deps
%defattr(-,decisionengine,decisionengine,-)
%dir %{decisionengine_home}
%dir %attr(700, decisionengine, decisionengine) %{decisionengine_home}/passwords.d
%dir %attr(700, decisionengine, decisionengine) %{decisionengine_home}/tokens.d
%dir %{_sysconfdir}/decisionengine
%dir %{_sysconfdir}/decisionengine/config.d
%config(noreplace) %{_sysconfdir}/decisionengine/decision_engine.jsonnet
%attr(-, root, root) %{_unitdir}/decisionengine.service
%attr(-, root, root) %config(noreplace) %{_sysconfdir}/sysconfig/decisionengine
%attr(-, root, root) %{_bindir}/decisionengine-wrapper.sh
%attr(-, root, root) %{_bindir}/decisionengine
%attr(-, root, root) %{_bindir}/de-client
%attr(-, root, root) %{_bindir}/de-logparser
%attr(-, root, root) %{_bindir}/de-query-tool
%attr(-, root, root) %{_bindir}/de-reaper
%attr(-, root, root) %{_bindir}/decisionengine-install-python

# add all files in config.d
%attr(-, decisionengine, decisionengine) %dir %{_localstatedir}/log/decisionengine

%files modules-deps

%files standalone

%files onenode

%changelog
* Wed Mar 12 2025 Marco Mambelli <marcom@fnal.gov> - 2.0.5
- Decision Engine 2.0.5
