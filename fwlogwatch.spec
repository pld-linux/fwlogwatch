Summary:	Firewall log analyzer, report generator and realtime response agent
Summary(pl.UTF-8):	Analizator logów firewalla, generator raportów i agent natychmiastowej odpowiedzi
Name:		fwlogwatch
Version:	1.1
Release:	1
License:	GPL
Group:		Applications/System
Source0:	http://www.kybs.de/boris/sw/%{name}-%{version}.tar.bz2
# Source0-md5:	266974c417a7b973d3e54b64f95e9536
Source1:	%{name}.init
Source2:	%{name}.sysconfig
URL:		http://fwlogwatch.inside-security.de/
BuildRequires:	flex
BuildRequires:	m4
BuildRequires:	zlib-devel
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
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

%description -l pl.UTF-8
fwlogwatch produkuje sumaryczne raporty w formacie tekstowym oraz HTML
z informacjami dostarczanymi przez logi ipchains, netfilter/iptables,
ipfilter, Cisco IOS oraz Cisco PIX. fwlogwatch ma wiele opcji
pozwalających znajdować określone wzorce w próbach połączeń. Na
podstawie tych danych może generować raporty o incydentach i wysyłać
je na adres abuse lub do centrów koordynacji CERT. Może on również
pracować jako daemon i informować o anomaliach oraz podejmować kroki
zapobiegawcze.

%prep
%setup -q

%build
%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -Wall" \
	LDFLAGS="%{rpmldflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{rc.d/init.d,sysconfig},%{_sysconfdir}} \
	$RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8}

%{__make} install install-config \
	INSTALL_DIR="$RPM_BUILD_ROOT%{_usr}" \
	CONF_DIR="$RPM_BUILD_ROOT%{_sysconfdir}"

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/%{name}
install %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add %{name}
%service %{name} restart

%preun
if [ "$1" = "0" ]; then
	%service %{name} stop
	/sbin/chkconfig --del %{name}
fi

%files
%defattr(644,root,root,755)
%doc contrib/fw* AUTHORS CREDITS ChangeLog README
%attr(700,root,root) %dir %{_sysconfdir}
%attr(600,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*
%attr(755,root,root) %{_sbindir}/*
%attr(754,root,root) /etc/rc.d/init.d/%{name}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/%{name}
%{_mandir}/man?/*
