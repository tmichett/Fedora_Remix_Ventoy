Name:           ventoy
Version:        1.0.0
Release:        1%{?dist}
Summary:        Ventoy installation package

License:        GPLv2
BuildArch:      noarch

%description
Ventoy installation package that provides necessary files and scripts for Ventoy functionality.

%prep
# No prep needed as we're just copying files

%build
# No build needed as we're just copying files

%install
# Create necessary directories
mkdir -p %{buildroot}/opt/ventoy
mkdir -p %{buildroot}/usr/local/bin

# Copy ventoy directory to /opt
cp -r %{_sourcedir}/ventoy/* %{buildroot}/opt/ventoy/

# Copy scripts to /usr/local/bin
cp %{_sourcedir}/Ventoy.sh %{buildroot}/usr/local/bin/
cp %{_sourcedir}/Ventoy_Plugin.sh %{buildroot}/usr/local/bin/

# Make scripts executable
chmod +x %{buildroot}/usr/local/bin/Ventoy.sh
chmod +x %{buildroot}/usr/local/bin/Ventoy_Plugin.sh

%files
/opt/ventoy/
/usr/local/bin/Ventoy.sh
/usr/local/bin/Ventoy_Plugin.sh

%changelog
* %(date "+%a %b %d %Y") %{packager} - %{version}-%{release}
- Initial package build 