%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           pygame
Version:        1.7.1
Release:        10%{?dist}
Summary:        Python modules for writing games

Group:          Development/Languages
License:        LGPL
URL:            http://www.pygame.org
Patch0:         %{name}-%{version}-config.patch
Patch1:         %{name}-%{version}-64bit.patch
Source0:        http://pygame.org/ftp/%{name}-%{version}release.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel
BuildRequires:  SDL_ttf-devel SDL_image-devel SDL_mixer-devel python-numeric
Requires:       SDL_ttf-devel SDL_image-devel SDL_mixer-devel python-numeric

# Obsolete/Provide old package names
Obsoletes:      pygame-devel <= %{version}
Provides:       pygame-devel = %{version}-%{release}
Obsoletes:      python-pygame-devel <= %{version}
Provides:       python-pygame-devel = %{version}-%{release}
Obsoletes:      python-pygame <= %{version}
Provides:       python-pygame = %{version}-%{release}
Obsoletes:      python-pygame-doc <= %{version}
Provides:       python-pygame-doc = %{version}-%{release}

%description
Pygame is a set of Python modules designed for writing games. It is
written on top of the excellent SDL library. This allows you to create
fully featured games and multimedia programs in the python language.
Pygame is highly portable and runs on nearly every platform and
operating system.

%package examples
Summary:        Example code for using pygame
Group:          Documentation
Requires:       %{name} = %{version}-%{release}

%description examples
%{summary}.


%prep
%setup -q -n %{name}-%{version}release
%patch0 -p0 -b .config
%patch1 -p0 -b .64bit

# rpmlint fixes
rm -f examples/.#stars.py.1.7

# remove macosx stuff
rm -fr examples/macosx

# These files must be provided by pygame-nonfree(-devel) packages on a
# repository that does not have restrictions on providing non-free software
rm -f src/ffmovie.[ch]


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


%check
# base_test fails in mock, unable to find soundcard
PYTHONPATH="$RPM_BUILD_ROOT%{python_sitearch}" %{__python} test/base_test.py || :
PYTHONPATH="$RPM_BUILD_ROOT%{python_sitearch}" %{__python} test/image_test.py
PYTHONPATH="$RPM_BUILD_ROOT%{python_sitearch}" %{__python} test/rect_test.py

 
%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc docs readme.txt WHATSNEW
%{python_sitearch}/%{name}
%{_includedir}/python*/%{name}

%files examples
%defattr(-,root,root,-)
%doc examples/*


%changelog
* Sun Dec 10 2006 Christopher Stone <chris.stone@gmail.som> 1.7.1-10
- Remove macosx examples
- Move header files into main package
- Move examples into examples subpackage
- python(abi) = 0:2.5

* Wed Sep 06 2006 Christopher Stone <chris.stone@gmail.com> 1.7.1-9
- No longer %%ghost pyo files. Bug #205396

* Sat Sep 02 2006 Christopher Stone <chris.stone@gmail.com> 1.7.1-8
- FC6 Rebuild

* Wed May 03 2006 Christopher Stone <chris.stone@gmail.com> 1.7.1-7
- Fix Obsolete/Provides of python-pygame-doc

* Wed Apr 26 2006 Christopher Stone <chris.stone@gmail.com> 1.7.1-6
- Bump release for new build on devel

* Wed Apr 26 2006 Christopher Stone <chris.stone@gmail.com> 1.7.1-5
- Add Obsolete/Provides tags for python-pygame-docs
- Add Obsolete/Provides tags for python-pygame-devel to devel package
- Hopefully this fixes Bugzilla bug #189991

* Fri Apr 21 2006 Christopher Stone <chris.stone@gmail.com> 1.7.1-4
- Add Requires to -devel package
- Remove ffmovie.h from -devel package since it requires smpeg-devel

* Fri Apr 21 2006 Christopher Stone <chris.stone@gmail.com> 1.7.1-3
- Obsolete linva python-pygame package
- Added Provides for python-pygame
- Fix equal sign in devel requires

* Thu Apr 20 2006 Christopher Stone <chris.stone@gmail.com> 1.7.1-2
- Added a patch to clean up some warnings on 64 bit compiles

* Tue Apr 18 2006 Christopher Stone <chris.stone@gmail.com> 1.7.1-1
- Initial RPM release
