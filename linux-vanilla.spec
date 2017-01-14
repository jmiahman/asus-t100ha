%global debug_package %{nil}
%global kernel_rc -rc3

Name:		linux-vanilla
Version:	4.10.0
Release:	1%{?dist}
Summary:	The Linux kernel

Group:		System Environment/Kernel		
License:	GPLv2 and Redistributable
URL:		http://ftp.kernel.org
Source0:	https://www.kernel.org/pub/linux/kernel/v4.x/testing/linux-%{version}%{kernel_rc}.tar.xz	

#Source1:	kernelconfig.armhf
#Source2:	kernelconfig.x86
Source3:	kernelconfig.x86_64

# Patches for t100ha
Patch0001: 0001-hid-input-Add-Asus-T100-T100HA-specific-keys.patch
Patch0002: 0002-ASoC-rt5645-add-support-for-RT5648.patch
Patch0003: 0003-ASoc-rt5645-add-ACPI-ID-10EC3270.patch
Patch0004: 0004-ASoC-Intel-cht_bsw_rt5645-add-Baytrail-MCLK-support.patch
Patch0005: 0005-ASoC-Intel-Atom-add-machine-driver-for-baytrail-rt56.patch
Patch0006: 0006-ASoC-Intel-add-support-for-ALC3270-codec.patch
Patch0007: 0007-ASoC-Intel-cht_bsw_rt5645-harden-ACPI-device-detecti.patch
Patch0008: 0008-ASoC-rt5645-fix-error-handling-for-gpio-detection.patch
Patch0009: 0009-ASoC-Intel-cht-bsw-rt5645-add-quirks-for-SSP0-AIF1-A.patch
Patch0010: 0010-drm-i915-Workaround-VLV-CHV-DSI-scanline-counter-har.patch
Patch0011: 0011-Bluetooth-hci_bcm-Add-BCM2E72-ACPI-ID.patch
Patch0012: 0012-input-ASUS-T100-touchpad-multitouch-driver.patch

#BuildRequires:	
#Requires:	

%description
The Linux kernel %{version}

%prep
#rm -rf %{buildroot}
%autosetup -p1 -n linux-%{version}%{kernel_rc}

mkdir -p %{buildroot}/build
%ifarch armv7l armv5el
%__cp %{SOURCE1} .config
%endif

%ifarch i386 i486 i586 i686
%__cp %{SOURCE2} .config
%endif

%ifarch x86_64
%__cp -f %{SOURCE3} .config
%endif

%build
%make_build silentoldconfig
%make_build KBUILD_BUILD_VERSION=%{version}-%{release}-Unity

mkdir -p %{buildroot}/usr/src/linux-headers-%{version}
%__cp -f %{SOURCE3} %{buildroot}/usr/src/linux-headers-%{version}/.config

%install
%__cp -f %{SOURCE3} %{buildroot}/.config
mkdir -p %{buildroot}/boot 
mkdir -p %{buildroot}/lib/modules
make -j1 modules_install firmware_install install \
INSTALL_MOD_STRIP=1 \
INSTALL_MOD_PATH=%{buildroot} \
INSTALL_PATH=%{buildroot}/boot \

rm -rf %{buildroot}/lib/modules/%{version}%{kernel_rc}/build 
rm -rf %{buildroot}/lib/modules/%{version}%{kernel_rc}/source
rm -rf %{buildroot}/lib/firmware

mkdir -p %{buildroot}/usr/share/kernel/unity/
install -D include/config/kernel.release \
%{buildroot}/usr/share/kernel/unity/kernel.release

# /boot
install -d $RPM_BUILD_ROOT/boot
mv $RPM_BUILD_ROOT/.config $RPM_BUILD_ROOT/boot/config-%{version}%{kernel_rc}
dracut -f $RPM_BUILD_ROOT/boot/initramfs-%{version}%{kernel_rc}.img %{version}%{kernel_rc}

%files
%doc
/boot/*%{version}%{kernel_rc}
/boot/initramfs-%{version}%{kernel_rc}.img
/lib/modules/%{version}%{kernel_rc}/
/usr/share/kernel/

%changelog
