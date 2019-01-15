#%define version __DECISIONENGINE_RPM_VERSION__
#%define release __DECISIONENGINE_RPM_RELEASE__
%define version 0.3.7
%define release 2

%define de_user decisionengine
%define de_group decisionengine

%define de_confdir %{_sysconfdir}/decisionengine
%define de_channel_confdir %{_sysconfdir}/decisionengine/config.d
%define de_logdir %{_localstatedir}/log/decisionengine
%define de_lockdir %{_localstatedir}/lock/decisionengine
%define systemddir %{_prefix}/lib/systemd/system

%define le_builddir %{_builddir}/decisionengine/framework/logicengine/cxx/build

# From http://fedoraproject.org/wiki/Packaging:Python
# Define python_sitelib
%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

%define de_python_sitelib $RPM_BUILD_ROOT%{python_sitelib}

Name:           decisionengine
Version:        %{version}
Release:        %{release}
Summary:        The HEPCloud Decision Engine Framework

Group:          System Environment/Daemons
License:        Fermitools Software Legal Information (Modified BSD License)
URL:            http://hepcloud.fnal.gov

Source0:        decisionengine.tar.gz

BuildArch:      x86_64
BuildRequires:  cmake
#BuildRequires:  cmake numpy numpy-f2py python-pandas
BuildRequires:  boost-python boost-regex boost-system
#Requires:       numpy >= 1.7.1
#Requires:       numpy-f2py >= 1.7.1
#Requires:       python-pandas >= 0.17.1
Requires:       boost-python >= 1.53.0
Requires:       boost-regex >= 1.53.0
Requires:       boost-system >= 1.53.0
Requires(post): /sbin/service
Requires(post): /usr/sbin/useradd


%description
The Decision Engine is a critical component of the HEPCloud Facility. It
provides the functionality of resource scheduling for disparate resource
providers, including those which may have a cost or a restricted allocation
of cycles.

%package testcase
Summary:        The HEPCloud Decision Engine Test Case
Group:          System Environment/Daemons
Requires:       decisionengine = %{version}-%{release}

%description testcase
The testcase used to try out the Decision Engine.


#%package standard-library
#Summary:        The HEPCloud Decision Engine Modules in Standard Library
#Group:          System Environment/Daemons
#Requires:       decisionengine = %{version}-%{release}

#%description standard-library
#The modules in the Decision Engine Standard Library.


%prep
%setup -q -n decisionengine


%build
pwd
mkdir %{le_builddir}
cd %{le_builddir}
cmake ..
make
[ -e ../../RE.so ] && rm ../../RE.so
[ -e ../../libLogicEngine.so ] && rm ../../libLogicEngine.so
cp ErrorHandler/RE.so ../..
cp ErrorHandler/libLogicEngine.so ../..


%install
rm -rf $RPM_BUILD_ROOT

# Create the system directories
install -d $RPM_BUILD_ROOT%{_sbindir}
install -d $RPM_BUILD_ROOT%{_bindir}
install -d $RPM_BUILD_ROOT%{_initddir}
install -d $RPM_BUILD_ROOT%{de_confdir}
install -d $RPM_BUILD_ROOT%{de_channel_confdir}
install -d $RPM_BUILD_ROOT%{de_logdir}
install -d $RPM_BUILD_ROOT%{de_lockdir}
install -d $RPM_BUILD_ROOT%{systemddir}
install -d $RPM_BUILD_ROOT%{python_sitelib}

# Copy files in place
cp -r ../decisionengine $RPM_BUILD_ROOT%{python_sitelib}

mkdir -p $RPM_BUILD_ROOT%{de_confdir}/config.d
install -m 0644 build/packaging/rpm/decision_engine_template.conf $RPM_BUILD_ROOT%{de_confdir}/decision_engine.conf
install -m 0644 build/packaging/rpm/decisionengine.service $RPM_BUILD_ROOT%{systemddir}/decision-engine.service
install -m 0644 build/packaging/rpm/decisionengine_initd_template $RPM_BUILD_ROOT%{_initrddir}/decision-engine
install -m 0755 build/packaging/rpm/decisionengine_initd_template $RPM_BUILD_ROOT%{_sbindir}/decision-engine

# BUILDING testcase RPM: Uncomment following 1 line
#install -m 0644 framework/tests/etc/decisionengine/config.d/channelA.conf $RPM_BUILD_ROOT%{de_channel_confdir}

# Remove unwanted files
rm $RPM_BUILD_ROOT%{python_sitelib}/decisionengine/README.md
rm -Rf $RPM_BUILD_ROOT%{python_sitelib}/decisionengine/tests
rm -Rf $RPM_BUILD_ROOT%{python_sitelib}/decisionengine/build
rm -Rf $RPM_BUILD_ROOT%{python_sitelib}/decisionengine/framework/tests
rm -Rf $RPM_BUILD_ROOT%{python_sitelib}/decisionengine/framework/logicengine/cxx
rm -Rf $RPM_BUILD_ROOT%{python_sitelib}/decisionengine/framework/logicengine/tests
# BUILDING testcase RPM: Comment following line
rm -Rf $RPM_BUILD_ROOT%{python_sitelib}/decisionengine/testcases

%files
%{python_sitelib}/decisionengine/framework/configmanager
%{python_sitelib}/decisionengine/framework/dataspace
%{python_sitelib}/decisionengine/framework/engine
%{python_sitelib}/decisionengine/framework/logicengine
%{python_sitelib}/decisionengine/framework/modules
%{python_sitelib}/decisionengine/framework/taskmanager
%{python_sitelib}/decisionengine/framework/util
%{python_sitelib}/decisionengine/framework/__init__.py
%{python_sitelib}/decisionengine/framework/__init__.pyo
%{python_sitelib}/decisionengine/framework/__init__.pyc
%{python_sitelib}/decisionengine/__init__.py
%{python_sitelib}/decisionengine/__init__.pyo
%{python_sitelib}/decisionengine/__init__.pyc
%{python_sitelib}/decisionengine/LICENSE.txt
%{de_confdir}/config.d

%{systemddir}/decision-engine.service
%{_initrddir}/decision-engine
%{_sbindir}/decision-engine
%attr(-, %{de_user}, %{de_group}) %{de_logdir}
%attr(-, %{de_user}, %{de_group}) %{de_lockdir}
%config(noreplace) %{de_confdir}/decision_engine.conf


# BUILDING testcase RPM: Uncomment following 3 lines
#%files testcase
#%{python_sitelib}/decisionengine/testcases
#%config(noreplace) %{de_channel_confdir}/channelA.conf


#%files standard-library
#%{python_sitelib}/decisionengine/modules


%pre
# Add the "decisionengine" user and group if they do not exist
getent group %{de_group} >/dev/null ||
    groupadd -r  %{de_group}
getent passwd  %{de_user} >/dev/null || \
    useradd -r -g  %{de_user} -d /var/lib/decisionengine \
    -c "Decision Engine user" -s /sbin/nologin -m %{de_user}
# If the decisionengine user already exists make sure it is part of
# the decisionengine group
usermod --append --groups  %{de_group}  %{de_user} >/dev/null


%post
# $1 = 1 - Installation
# $1 = 2 - Upgrade
/sbin/chkconfig --add decision-engine
if [ ! -e /usr/bin/de-client ]; then
   ln -s %{python_sitelib}/decisionengine/framework/engine/de_client.py /usr/bin/de-client
fi
if [ ! -e /usr/sbin/decisionengine ]; then
   ln -s %{python_sitelib}/decisionengine/framework/engine/DecisionEngine.py /usr/sbin/decisionengine
fi

# Change the ownership of log and lock dir if they already exist
if [ -d %{de_logdir} ]; then
    chown -R %{de_user}.%{de_group} %{de_logdir}
fi
if [ -d %{de_lockdir} ]; then
    chown -R %{de_user}.%{de_group} %{de_lockdir}
fi


%preun
# $1 = 0 - Action is uninstall
# $1 = 1 - Action is upgrade

if [ "$1" = "0" ] ; then
    /sbin/chkconfig --del decision-engine
fi


%changelog
* Tue Jan 15 2019 Parag Mhashilkar <parag@fnal.gov> - 0.3.7-2
- Remove dependency on python-pandas and numpy rpms as we get latest from pip

* Mon Jan 14 2019 Parag Mhashilkar <parag@fnal.gov> - 0.3.7-1
- Add ability to select columns in de-client query

* Wed Dec 19 2018 Parag Mhashilkar <parag@fnal.gov> - 0.3.6-0.1
- Several bug fixes and updates to de_client

* Wed Dec 5 2018 Parag Mhashilkar <parag@fnal.gov> - 0.3.5-0.2
- Several bug fixes

* Wed Dec 5 2018 Parag Mhashilkar <parag@fnal.gov> - 0.3.5-0.1
- Several bug fixes

* Mon Dec 3 2018 Parag Mhashilkar <parag@fnal.gov> - 0.3.4-0.1
- Several bug fixes

* Wed Oct 24 2018 Parag Mhashilkar <parag@fnal.gov> - 0.3.3-0.1
- Bug fixes related to SourceProxy

* Tue Jun 12 2018 Parag Mhashilkar <parag@fnal.gov> - 0.3.2-0.1
- Test release that includes source proxy and other new features
- Also, first release since the framework code split from main codebase

* Tue Dec 12 2017 Parag Mhashilkar <parag@fnal.gov> - 0.3.1-0.1
- Minor bug fixes

* Mon Nov 13 2017 Parag Mhashilkar <parag@fnal.gov> - 0.3-0.1
- Decision Engine v0.3
- Includes fixes made during the demo

* Thu Nov 02 2017 Parag Mhashilkar <parag@fnal.gov> - 0.2-0.1
- Decision Engine v0.2 for the demo
- RPM work in progress

* Fri Sep 15 2017 Parag Mhashilkar <parag@fnal.gov> - 0.1-0.2
- Decision Engine v0.1 work in progress
- Added packaging for modules

* Mon May 01 2017 Parag Mhashilkar <parag@fnal.gov> - 0.1-0.1
- Decision Engine v0.1
- RPM work in progress
