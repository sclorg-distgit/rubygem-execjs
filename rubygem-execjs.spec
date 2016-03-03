%{?scl:%scl_package rubygem-%{gem_name}}
%{!?scl:%global pkg_name %{name}}

# Generated from execjs-1.4.0.gem by gem2rpm -*- rpm-spec -*-
%global gem_name execjs

# Fallback to rh-nodejs4 rh-nodejs4-scldevel is probably not available in
# the buildroot.
%{!?scl_nodejs:%global scl_nodejs rh-nodejs4}
%{!?scl_prefix_nodejs:%global scl_prefix_nodejs %{scl_nodejs}-}

Summary: Run JavaScript code from Ruby
Name: %{?scl_prefix}rubygem-%{gem_name}
Version: 2.2.0
Release: 4%{?dist}
Group: Development/Languages
# Public Domain: %%{gem_libdir}/execjs/support/json2.js
License: MIT and Public Domain
URL: https://github.com/sstephenson/execjs
Source0: http://rubygems.org/gems/%{gem_name}-%{version}.gem
# git clone https://github.com/sstephenson/execjs.git && cd execjs
# git checkout v2.2.0 && tar czf execjs-2.2.0-tests.tgz test/
Source1: %{gem_name}-%{version}-tests.tgz

Requires: %{?scl_prefix_ruby}ruby(release)
Requires: %{?scl_prefix_ruby}ruby(rubygems)
Requires: %{?scl_prefix_ruby}ruby
BuildRequires: %{?scl_prefix_ruby}ruby(release)
BuildRequires: %{?scl_prefix_ruby}rubygems-devel
BuildRequires: %{?scl_prefix_ruby}rubygem(minitest)
BuildArch: noarch
Provides: %{?scl_prefix}rubygem(%{gem_name}) = %{version}

BuildRequires: %{?scl_prefix_nodejs}nodejs

%description
ExecJS lets you run JavaScript code from Ruby. It automatically picks the
best runtime available to evaluate your JavaScript program, then returns
the result to you as a Ruby object.

%package doc
Summary: Documentation for %{pkg_name}
Group: Documentation
Requires: %{?scl_prefix}%{pkg_name} = %{version}-%{release}
BuildArch: noarch

%description doc
Documentation for %{pkg_name}

%prep
%setup -n %{pkg_name}-%{version} -q -c -T
%{?scl:scl enable %{scl} %{scl_nodejs} - << \EOF}
%gem_install -n %{SOURCE0}
%{?scl:EOF}

%build

%install
mkdir -p %{buildroot}%{gem_dir}
cp -a .%{gem_dir}/* \
        %{buildroot}%{gem_dir}/

%check
pushd .%{gem_instdir}
tar xzf %{SOURCE1}
# disable test that needs internet connection
sed -i '/def test_coffeescript/,/^  end$/ s/^/#/' test/test_execjs.rb
export LANG=en_US.utf8
%{?scl:scl enable %{scl} %{scl_nodejs} - << \EOF}
ruby -Ilib -e 'Dir.glob "./test/**/test_*.rb", &method(:require)'
%{?scl:EOF}
popd

%files
%dir %{gem_instdir}
%doc %{gem_instdir}/LICENSE
%{gem_libdir}
%exclude %{gem_cache}
%{gem_spec}

%files doc
%doc %{gem_docdir}
%doc %{gem_instdir}/README.md

%changelog
* Wed Feb 24 2016 Pavel Valena <pvalena@redhat.com> - 2.2.0-4
- Rebuilt for rh-ror42

* Mon Jan 26 2015 Josef Stribny <jstribny@redhat.com> - 2.2.0-1
- Update to 2.2.0

* Mon Feb 17 2014 Josef Stribny <jstribny@redhat.com> - 1.4.0-7
- Depend on scldevel(v8) virtual provide

* Tue Nov 26 2013 Josef Stribny <jstribny@redhat.com> - 1.4.0-6
- Use v8 scl macro

* Wed Jun 12 2013 Josef Stribny <jstribny@redhat.com> - 1.4.0-5
- Rebuild for https://fedoraproject.org/wiki/Features/Ruby_2.0.0

* Thu Jul 26 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.4.0-4
- Reimported from Fedora.

* Sat Jul 21 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jul 12 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.4.0-2
- Removed the duplicated "git checkout" in comment.
- BR: rubygem(therubyracer) for tests, don't use deprecated js.

* Wed Jun 13 2012 Bohuslav Kabrda <bkabrda@redhat.com> - 1.4.0-1
- Initial package
