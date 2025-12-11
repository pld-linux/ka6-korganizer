#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.12.0
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		korganizer
Summary:	korganizer
Name:		ka6-%{kaname}
Version:	25.12.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	a082fa888905a4e436f95eeeafe85946
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel
BuildRequires:	Qt6Gui-devel
BuildRequires:	Qt6Test-devel
BuildRequires:	Qt6UiTools-devel
BuildRequires:	Qt6Widgets-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	ka6-akonadi-calendar-devel >= %{kdeappsver}
BuildRequires:	ka6-akonadi-contacts-devel >= %{kdeappsver}
BuildRequires:	ka6-akonadi-devel >= %{kdeappsver}
BuildRequires:	ka6-akonadi-mime-devel >= %{kdeappsver}
BuildRequires:	ka6-akonadi-search-devel >= %{kdeappsver}
BuildRequires:	ka6-calendarsupport-devel >= %{kdeappsver}
BuildRequires:	ka6-eventviews-devel >= %{kdeappsver}
BuildRequires:	ka6-incidenceeditor-devel >= %{kdeappsver}
BuildRequires:	ka6-kcalutils-devel >= %{kdeappsver}
BuildRequires:	ka6-kidentitymanagement-devel >= %{kdeappsver}
BuildRequires:	ka6-kldap-devel >= %{kdeappsver}
BuildRequires:	ka6-kmailtransport-devel >= %{kdeappsver}
BuildRequires:	ka6-kmime-devel >= %{kdeappsver}
BuildRequires:	ka6-kontactinterface-devel >= %{kdeappsver}
BuildRequires:	ka6-kpimtextedit-devel >= %{kdeappsver}
BuildRequires:	ka6-libkdepim-devel >= %{kdeappsver}
BuildRequires:	ka6-pimcommon-devel >= %{kdeappsver}
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kcmutils-devel >= %{kframever}
BuildRequires:	kf6-kcodecs-devel >= %{kframever}
BuildRequires:	kf6-kcompletion-devel >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kconfigwidgets-devel >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-kcrash-devel >= %{kframever}
BuildRequires:	kf6-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf6-kdoctools-devel >= %{kframever}
BuildRequires:	kf6-kholidays-devel >= %{kframever}
BuildRequires:	kf6-kiconthemes-devel >= %{kframever}
BuildRequires:	kf6-kitemviews-devel >= %{kframever}
BuildRequires:	kf6-kjobwidgets-devel >= %{kframever}
BuildRequires:	kf6-knewstuff-devel >= %{kframever}
BuildRequires:	kf6-knotifications-devel >= %{kframever}
BuildRequires:	kf6-kparts-devel >= %{kframever}
BuildRequires:	kf6-kservice-devel >= %{kframever}
BuildRequires:	kf6-kwidgetsaddons-devel >= %{kframever}
BuildRequires:	kf6-kwindowsystem-devel >= %{kframever}
BuildRequires:	kf6-kxmlgui-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	phonon-qt6-devel
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
ExcludeArch:	x32 i686
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
KOrganizer is an easy to use personal information manager (PIM). You
can write journal entries, schedule appointments, events, and to-dos.
KOrganizer will remind you about pending tasks, and help you keep your
schedule.

%description -l pl.UTF-8
KOrganizer jest łatwym w użyciu programem do zarządzania informacją
osobistą (PIM). Możesz dodawać wpisy do dziennika, planować spotkania,
i listę zadań do zrobienia. KOrganizer przypomni Ci o sprawach do
załatwienia i pomoże Ci trzymać się planu.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_desktop_database_post

%postun
/sbin/ldconfig
%update_desktop_database_postun

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/korganizer
%ghost %{_libdir}/libkorganizer_core.so.6
%{_libdir}/libkorganizer_core.so.*.*
%ghost %{_libdir}/libkorganizer_interfaces.so.6
%{_libdir}/libkorganizer_interfaces.so.*.*
%ghost %{_libdir}/libkorganizerprivate.so.6
%{_libdir}/libkorganizerprivate.so.*.*
%{_libdir}/qt6/plugins/korganizerpart.so
%{_desktopdir}/korganizer-import.desktop
%{_desktopdir}/org.kde.korganizer.desktop
%{_datadir}/config.kcfg/korganizer.kcfg
%{_datadir}/dbus-1/interfaces/org.kde.Korganizer.Calendar.xml
%{_datadir}/dbus-1/interfaces/org.kde.korganizer.Korganizer.xml
%{_iconsdir}/hicolor/*x*/apps/*.png
%{_iconsdir}/hicolor/scalable/apps/*.svg*
%{_datadir}/korganizer
%{_datadir}/metainfo/org.kde.korganizer.appdata.xml
%{_datadir}/qlogging-categories6/korganizer.categories
%{_datadir}/qlogging-categories6/korganizer.renamecategories
%{_desktopdir}/korganizer-view.desktop
%{_datadir}/dbus-1/services/org.kde.korganizer.service
%dir %{_libdir}/qt6/plugins/pim6/kcms/korganizer
%{_libdir}/qt6/plugins/pim6/kcms/korganizer/korganizer_configcolorsandfonts.so
%{_libdir}/qt6/plugins/pim6/kcms/korganizer/korganizer_configfreebusy.so
%{_libdir}/qt6/plugins/pim6/kcms/korganizer/korganizer_configgroupscheduling.so
%{_libdir}/qt6/plugins/pim6/kcms/korganizer/korganizer_configmain.so
%{_libdir}/qt6/plugins/pim6/kcms/korganizer/korganizer_configplugins.so
%{_libdir}/qt6/plugins/pim6/kcms/korganizer/korganizer_configtime.so
%{_libdir}/qt6/plugins/pim6/kcms/korganizer/korganizer_configviews.so
%{_libdir}/qt6/plugins/pim6/kcms/korganizer/korganizer_userfeedback.so
%dir %{_libdir}/qt6/plugins/pim6/kcms/summary
%{_libdir}/qt6/plugins/pim6/kcms/summary/kcmapptsummary.so
%{_libdir}/qt6/plugins/pim6/kcms/summary/kcmsdsummary.so
%{_libdir}/qt6/plugins/pim6/kcms/summary/kcmtodosummary.so
%{_libdir}/qt6/plugins/pim6/kontact/kontact_journalplugin.so
%{_libdir}/qt6/plugins/pim6/kontact/kontact_korganizerplugin.so
%{_libdir}/qt6/plugins/pim6/kontact/kontact_specialdatesplugin.so
%{_libdir}/qt6/plugins/pim6/kontact/kontact_todoplugin.so
%dir %{_libdir}/qt6/plugins/pim6/korganizer
%{_libdir}/qt6/plugins/pim6/korganizer/datenums.so
%{_libdir}/qt6/plugins/pim6/korganizer/lunarphases.so
%{_libdir}/qt6/plugins/pim6/korganizer/picoftheday.so
%{_libdir}/qt6/plugins/pim6/korganizer/thisdayinhistory.so
%{_iconsdir}/hicolor/scalable/status/*.svg
