Summary:	Firewall log analyzer, report generator and realtime response agent
Summary(pl):	Analizator logów firewalla, generator raportów i agent natychmiastowej odpowiedzi
Name:		fwlogwatch
Version:	1.0
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://www.kybs.de/boris/sw/%{name}-%{version}.tar.bz2
# Source0-md5:	a0aa323568862e23fdbc6473ce6a01b5
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://fwlogwatch.inside-security.de/
BuildRequires:	flex
BuildRequires:	zlib-devel
BuildRequires:	m4
Prereq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sysconfdir		/etc/%{name}

%description
fwlogwatch produces ipchains, netfilter/iptables, ipfilter, Cisco IOS
and Cisco PIX log summary reports in text and HTML form and has a lot
of options to find and display relevant patterns in connection
attempts. With the data found it can also generate customizable
incident reports from a template and send them to abuse contacts at
offending sites or CERT coordination centers. Finally, it can also run
as daemon and report anomalies or start countermeasures.

%description -l pl
fwlogwatch produkuje sumaryczne raporty w formacie tekstowym oraz HTML
z informacjami dostarczanymi przez logi ipchains, netfilter/iptables,
ipfilter, Cisco IOS oraz Cisco PIX. fwlogwatch ma wiele opcji
pozwalaj±cych znajdowaæ okre¶lone wzorce w próbach po³±czeñ. Na
podstawie tych danych mo¿e generowaæ raporty o incydentach i wysy³aæ
je na adres abuse lub do centrów koordynacji CERT. Mo¿e on równie¿
pracowaæ jako daemon i informowaæ o anomaliach oraz podejmowaæ kroki
zapobiegawcze.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" OPT="%{rpmcflags}" LDFLAGS="%{rpmldflags}" \
	SYSCONFDIR="%{_sysconfdir}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},%{_sysconfdir}} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8}

%{__make} install install-config \
	DESTDIR=$RPM_BUILD_ROOT \
	SYSCONFDIR="%{_sysconfdir}" \
	PREFIX="%{_prefix}" \
	MANDIR="%{_mandir}" \
	INSTALL_DIR="$RPM_BUILD_ROOT/usr" \
	CONF_DIR="$RPM_BUILD_ROOT/etc/fwlogwatch"

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
if [ -f %{_var}/lock/subsys/%{name} ]; then
	/etc/rc.d/init.d/%{name} restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/%{name} start\" to start %{name} daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f %{_var}/lock/subsys/%{name} ]; then
		/etc/rc.d/init.d/%{name} stop 1>&2
	fi
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc contrib/fw* AUTHORS CREDITS ChangeLog README
%attr(700,root,root) %dir %{_sysconfdir}
%attr(600,root,root) %config(noreplace) %verify(not size mtime md5) %{_sysconfdir}/*.*
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not size mtime md5) /etc/sysconfig/%{name}
%{_mandir}/man?/*
