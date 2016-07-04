%global _enable_debug_package 0
%global debug_package %{nil}
%global __os_install_post /usr/lib/rpm/brp-compress %{nil}

Name:           sdcc-nonfree
Version:        3.6.0
Release:        1%{?dist}
Summary:        Small Device C Compiler - nonfree files
Group:          Applications/Engineering
License:        Redistributable but use for Microchip devices only
URL:            http://sdcc.sourceforge.net/
Source0:        http://downloads.sourceforge.net/sdcc/sdcc-src-%{version}.tar.bz2
Source1:        README.fedora

BuildRequires:  bison
BuildRequires:  boost-devel
BuildRequires:  flex
Buildrequires:  gputils sdcc
Requires:       sdcc

%description
Files derived from Microchip files which are licensed for
use for Microchip devices only. Files used for compiling code for
14 and 16 bit PIC processors. The sdcc --use-non-free flag must
be used to access these files during compilation and linking.


%package devel
Summary:        Small Device C Compiler - nonfree source files
Group:          Applications/Engineering
BuildArch:      noarch
Requires:       sdcc

%description devel
Source files for 14 and 16 bit PIC processor libraries. Theses files are
derived from Microchip files which are licensed for use for Microchip devices
only. These files are only required if you want to modify or examine the 
libraries.

%prep
%setup -q -n sdcc-%{version}
find -name '*.{c,h,cc}' -exec chmod -x '{}' \;
find -name '*.sh' -exec chmod +x '{}' \;

# Disable brp-strip-static-archive for now because it errors trying to
# strip foreign binaries.
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's#/usr/lib/rpm.*/brp-strip-static-archive .*##g')


%build
./configure
make Q= -C device/non-free/lib CC=/usr/libexec/sdcc/sdcc installdir=../build

%install
make install Q= -C device/non-free/include \
prefix=$RPM_BUILD_ROOT/usr
make install Q= -C device/non-free/lib CC=/usr/libexec/sdcc/sdcc prefix=$RPM_BUILD_ROOT/usr
find $RPM_BUILD_ROOT%{_datadir}/sdcc/non-free/lib/src -name \*.a -exec rm -f '{}' \;
rm -rf $RPM_BUILD_ROOT%{_datadir}/sdcc/non-free/lib/src/pic16/libdev/.deps
find $RPM_BUILD_ROOT%{_datadir}/sdcc/non-free/ -name \.checkdevices | xargs rm -rf


%files 
%defattr(-,root,root,-)
%{_datadir}/sdcc/non-free
%exclude %{_datadir}/sdcc/non-free/lib/src

%files devel
%defattr(-,root,root,-)
%{_datadir}/sdcc/non-free/lib/src

%changelog
* Sun Jul 03 2016 Roy Rankin <rrankin@ihug.com.au> - 3.6.0-1
- Initial nonfree specfile

