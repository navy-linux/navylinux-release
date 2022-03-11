%define debug_package %{nil}
%define product_family Navy Linux Enterprise
%define variant_titlecase Server
%define variant_lowercase server
%ifarch %{arm}
%define release_name AltArch
%define contentdir   altarch
%else
%define release_name Base
%define contentdir   navy
%endif
%ifarch ppc64le
%define tuned_profile :server
%endif
%define infra_var x86_64
%define base_release_version 8
%define full_release_version 8
%define dist_release_version 8
%define source_relase_version 8.5
%define navylinux_minor_rel 211021
%define navylinux_major_rel 8.5r1
#define beta Beta
%define dist .el%{dist_release_version}

# The anaconda scripts in %%{_libexecdir} can create false requirements
%global __requires_exclude_from %{_libexecdir}

Name:           system-release
Version:        %{navylinux_major_rel}
Release:        %{navylinux_minor_rel}
Summary:        %{product_family} release file
Group:          System Environment/Base
License:        BSD
%ifnarch %{arm}
%define pkg_name %{name}
%else
%define pkg_name navylinux-userland-release
%package -n %{pkg_name}
Summary:        %{product_family} release file
%endif
Provides:       navylinux-release = %{version}-%{release}
Provides:       navylinux-release(navylinux) = %{navylinux_major_rel}
Provides:       redhat-release = 8.5
Provides:       system-release = %{base_release_version}
Provides:       base-module(platform:el%{dist_release_version})
Provides:       navylinux-release-eula
Provides:       redhat-release-eula
Requires:       navylinux-repos(%{base_release_version})
Provides:       system-release(releasever) = 8

Source1:        85-display-manager.preset
Source2:        90-default.preset
Source3:        99-default-disable.preset

Source10:       RPM-GPG-KEY-navy-linux-official


Source100:      rootfs-expand

Source200:      LICENSE
Source201:      EULA

Source300:      navy-linux-base.repo
Source301:      navy-linux-kernel.repo
Source302:      navy-linux-extra.repo
Source303:      navy-linux-source.repo
Source304:      navy-linux-devel.repo
Source305:      navy-linux-debug.repo
Source306:      navy-linux-every.repo
Source307:      navy-linux-powertools.repo
Source308:      selr.repo


%ifarch %{arm}
%description -n %{pkg_name}
%{product_family} release files
%endif

%description
%{product_family} release files

%package -n navylinux-repos
Summary:        %{product_family} package repositories
Group:          System Environment/Base
Provides:       navylinux-repos(%{base_release_version})
Requires:       system-release = %{base_release_version}
Requires:       navylinux-gpg-keys
Conflicts:      %{name} < %{base_release_version}

%description -n navylinux-repos
%{product_family} package repository files for yum and dnf

%package -n navylinux-gpg-keys
Summary:        %{product_family} RPM keys
Group:          System Environment/Base
Conflicts:      %{name} < %{base_release_version}
BuildArch:      noarch

%description -n navylinux-gpg-keys
%{product_family} RPM signature keys

%prep
echo OK

%build
echo OK

%install
rm -rf %{buildroot}

# create skeleton
mkdir -p %{buildroot}/etc
mkdir -p %{buildroot}%{_prefix}/lib

# create /etc/system-release and /etc/redhat-release
echo "%{product_family} release %{navylinux_major_rel}-%{navylinux_minor_rel} (%{release_name}) " > %{buildroot}/etc/navylinux-release
ln -s navylinux-release %{buildroot}/etc/system-release
ln -s navylinux-release %{buildroot}/etc/redhat-release

# Create the os-release file
cat << EOF >>%{buildroot}%{_prefix}/lib/os-release
NAME="%{product_family} %{navylinux_major_rel}"
VERSION="%{navylinux_major_rel} (%{release_name})"
ID="navy"
ID_LIKE="rhel fedora"
VERSION_ID="%{base_release_version}"
PLATFORM_ID="platform:el%{dist_release_version}"
PRETTY_NAME="%{product_family} %{base_release_version} (%{release_name})"
ANSI_COLOR="0;31"
CPE_NAME="cpe:/o:navylinux:navylinux:%{base_release_version}%{?tuned_profile}"
HOME_URL="https://www.navylinux.org/"
BUG_REPORT_URL="https://git.navylinux.org/issue-tracker/general/-/issues"

NAVYLINUX_MANTISBT_PROJECT="NavyLinux-%{base_release_version}"
NAVYLINUX_MANTISBT_PROJECT_VERSION="%{base_release_version}"
REDHAT_SUPPORT_PRODUCT="navylinux"
REDHAT_SUPPORT_PRODUCT_VERSION="%{base_release_version}"

EOF
# Create the symlink for /etc/os-release
ln -s ../usr/lib/os-release %{buildroot}%{_sysconfdir}/os-release

# write cpe to /etc/system/release-cpe
echo "cpe:/o:navylinux:navylinux:%{base_release_version}" > %{buildroot}/etc/system-release-cpe

# create /etc/issue and /etc/issue.net
echo '\S' > %{buildroot}/etc/issue
echo 'Kernel \r on an \m' >> %{buildroot}/etc/issue
cp %{buildroot}/etc/issue %{buildroot}/etc/issue.net
echo >> %{buildroot}/etc/issue

# copy GPG keys
mkdir -p -m 755 %{buildroot}/etc/pki/rpm-gpg
install -m 644 %{SOURCE10} %{buildroot}/etc/pki/rpm-gpg

# copy yum repos
mkdir -p -m 755 %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE300} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE301} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE302} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE303} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE304} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE305} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE306} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE307} %{buildroot}/etc/yum.repos.d
install -m 644 %{SOURCE308} %{buildroot}/etc/yum.repos.d

# dnf for navy 8  

mkdir -p -m 755 %{buildroot}/etc/dnf/vars
echo "%{infra_var}" > %{buildroot}/etc/dnf/vars/infra
echo "%{contentdir}" >%{buildroot}/etc/dnf/vars/contentdir
echo "%{dist_release_version}" > %{buildroot}/etc/dnf/vars/releasever
echo "%{navylinux_major_rel}" > %{buildroot}/etc/dnf/vars/releaseversion

# yum for navy 7 

mkdir -p -m 755 %{buildroot}/etc/yum/vars
echo "%{infra_var}" > %{buildroot}/etc/yum/vars/infra
echo "%{contentdir}" >%{buildroot}/etc/yum/vars/contentdir
echo "%{dist_release_version}" > %{buildroot}/etc/yum/vars/releasever
echo "%{navylinux_major_rel}" > %{buildroot}/etc/yum/vars/releaseversion

%ifarch %{arm}
echo %{dist_release_version} > %{buildroot}/etc/dnf/vars/releasever
echo %{navylinux_major_rel} > %{buildroot}/etc/dnf/vars/releaseversion
# yum for navy 7
echo %{dist_release_version} > %{buildroot}/etc/yum/vars/releasever
echo %{navylinux_major_rel} > %{buildroot}/etc/yum/vars/releaseversion
%endif

# set up the dist tag macros
install -d -m 755 %{buildroot}/etc/rpm
cat >> %{buildroot}/etc/rpm/macros.dist << EOF
# dist macros.

%%navylinux_ver %{base_release_version}
%%navylinux %{base_release_version}
%%rhel %{base_release_version}
%%dist .el%{dist_release_version}
%%el%{dist_release_version} 1
EOF

# use unbranded datadir
mkdir -p -m 755 %{buildroot}/%{_datadir}/navylinux-release
ln -s navylinux-release %{buildroot}/%{_datadir}/redhat-release
install -m 644 %{SOURCE200} %{buildroot}/%{_datadir}/navylinux-release

# use unbranded docdir
mkdir -p -m 755 %{buildroot}/%{_docdir}/navylinux-release
ln -s navylinux-release %{buildroot}/%{_docdir}/redhat-release
install -m 644 %{SOURCE200} %{buildroot}/%{_docdir}/navylinux-release
install -m 644 %{SOURCE200} %{buildroot}/%{_docdir}/navylinux-release

# copy systemd presets
mkdir -p %{buildroot}/%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE1} %{buildroot}/%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE2} %{buildroot}/%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE3} %{buildroot}/%{_prefix}/lib/systemd/system-preset/

# copy EULA
install -m 644 %{SOURCE201} %{buildroot}/usr/share/redhat-release/


%ifarch %{arm} aarch64
# Install armhfp/aarch64 specific tools
install -D -m 0755 %{SOURCE100} %{buildroot}%{_bindir}/rootfs-expand
%endif


%clean
rm -rf %{buildroot}

%files -n %{pkg_name}
%defattr(0644,root,root,0755)
/etc/redhat-release
/etc/system-release
/etc/navylinux-release
%config(noreplace) /etc/os-release
%config /etc/system-release-cpe
%config(noreplace) /etc/issue
%config(noreplace) /etc/issue.net
/etc/rpm/macros.dist
%{_docdir}/redhat-release
%{_docdir}/navylinux-release/*
%{_datadir}/redhat-release
%{_datadir}/navylinux-release/*
%{_prefix}/lib/os-release
%{_prefix}/lib/systemd/system-preset/*
%ifarch %{arm} aarch64
%attr(0755,root,root) %{_bindir}/rootfs-expand
%endif

%files -n navylinux-repos
%config(noreplace) /etc/yum.repos.d/*
%config(noreplace) /etc/dnf/vars/*
%config(noreplace) /etc/yum/vars/*

%files -n navylinux-gpg-keys
/etc/pki/rpm-gpg/

