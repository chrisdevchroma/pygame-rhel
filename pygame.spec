%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           pygame
Version:        1.7.1
Release:        4%{?dist}
Summary:        Python modules for writing games
Group:          Development/Languages
License:        LGPL
URL:            http://www.pygame.org/
Patch0:         %{name}-%{version}-config.patch
Patch1:         %{name}-%{version}-64bit.patch
Source0:        http://pygame.org/ftp/%{name}-%{version}release.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  python-devel python-numeric
BuildRequires:  SDL_ttf-devel SDL_image-devel SDL_mixer-devel
Requires:       python-numeric
Obsoletes:      python-pygame < 1.7.1
Provides:       python-pygame = %{version}-%{release}

%description
Pygame is a set of Python modules designed for writing games. It is
written on top of the excellent SDL library. This allows you to create
fully featured games and multimedia programs in the python language.
Pygame is highly portable and runs on nearly every platform and
operating system.

%package devel
Summary:        Files needed for developing programs which use pygame
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       SDL_ttf-devel SDL_mixer-devel
Requires:       python-devel

%description devel
This package contains headers required to build applications that use
pygame.

%prep
%setup -q -n %{name}-%{version}release
%patch0 -p0 -b .config
%patch1 -p0 -b .64bit

# rpmlint fixes
rm -f examples/.#stars.py.1.7

# These files must be provided by pygame-nonfree(-devel) packages on a
# repository that can provide patent encumbered software.
rm -f src/ffmovie.[ch]

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%install
rm -rf %{buildroot}
%{__python} setup.py install -O1 --skip-build --root %{buildroot}

%check
# base_test fails in mock, unable to find soundcard
PYTHONPATH="%{buildroot}%{python_sitearch}" %{__python} test/base_test.py || :
PYTHONPATH="%{buildroot}%{python_sitearch}" %{__python} test/image_test.py
PYTHONPATH="%{buildroot}%{python_sitearch}" %{__python} test/rect_test.py
 
%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc docs/ readme.txt WHATSNEW
%dir %{python_sitearch}/%{name}
%{python_sitearch}/%{name}/freesansbold.ttf
%{python_sitearch}/%{name}/pygame.ico
%{python_sitearch}/%{name}/pygame_icon.*
%{python_sitearch}/%{name}/*.so*
%{python_sitearch}/%{name}/*.py
%{python_sitearch}/%{name}/*.pyc
%ghost %{python_sitearch}/%{name}/*.pyo

%files devel
%defattr(-,root,root,-)
%doc examples/
%dir %{_includedir}/python*/%{name}
%{_includedir}/python*/%{name}/*.h

%changelog
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
