%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           pygame
Version:        1.8.0
Release:        2%{?dist}
Summary:        Python modules for writing games

Group:          Development/Languages
License:        LGPLv2+
URL:            http://www.pygame.org
Patch0:         %{name}-1.7.1-config.patch
Source0:        http://pygame.org/ftp/%{name}-%{version}release.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  python-devel numpy
BuildRequires:  SDL_ttf-devel SDL_image-devel SDL_mixer-devel
BuildRequires:  libpng-devel libjpeg-devel libX11-devel
Requires:       numpy

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
%setup -qn %{name}-%{version}release
%patch0 -p0 -b .config~

# rpmlint fixes
chmod -x examples/*py
iconv -f iso8859-1 -t utf-8 WHATSNEW > WHATSNEW.conv && mv -f WHATSNEW.conv WHATSNEW
iconv -f iso8859-1 -t utf-8 readme.txt > readme.txt.conv && mv -f readme.txt.conv readme.txt


# These files must be provided by pygame-nonfree(-devel) packages on a
# repository that does not have restrictions on providing non-free software
rm -f src/ffmovie.[ch]


%build
CFLAGS="$RPM_OPT_FLAGS" %{__python} setup.py build


%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT

# Fix permissions
chmod 755 $RPM_BUILD_ROOT%{python_sitearch}/%{name}/*.so


%check
# base_test fails in mock, unable to find soundcard
PYTHONPATH="$RPM_BUILD_ROOT%{python_sitearch}" %{__python} test/base_test.py || :
PYTHONPATH="$RPM_BUILD_ROOT%{python_sitearch}" %{__python} test/image_test.py
PYTHONPATH="$RPM_BUILD_ROOT%{python_sitearch}" %{__python} test/rect_test.py
 

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc docs/ readme.txt WHATSNEW
%dir %{python_sitearch}/%{name}
%{python_sitearch}/%{name}*

%files devel
%defattr(-,root,root,-)
%doc examples/
%dir %{_includedir}/python*/%{name}
%{_includedir}/python*/%{name}/*.h


%changelog
* Mon Aug 25 2008 Robin Norwood <robin.norwood@gmail.com> 1.8.0-2
- Change from requiring python-numeric to numpy
- rhbz#457074

* Thu May 22 2008 Christopher Stone <chris.stone@gmail.com> 1.8.0-1
- Upstream sync
- Remove Obsolets/Provides (been around since FC-4)
- Remove no longer needed 64bit patch
- Remove %%{version} macro from Patch0 definition
- Add png, jpeg, and X11 libraries to BuildRequires
- Simplify %%files section
- Fix up some rpmlint warnings

* Thu Feb 21 2008 Christopher Stone <chris.stone@gmail.com> 1.7.1-16
- Add egginfo file to %%files
- Update %%license
- Fix permissions on .so files

* Wed Feb 20 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.7.1-15
- Autorebuild for GCC 4.3

* Tue May 15 2007 Christopher Stone <chris.stone@gmail.com> 1.7.1-14
- Add one more bit to 64-bit patch

* Sat May 12 2007 Christopher Stone <chris.stone@gmail.com> 1.7.1-13
- Apply 64-bit patch for python 2.5 (bz #239899)
- Some minor spec file cleanups

* Mon Apr 23 2007 Christopher Stone <chris.stone@gmail.com> 1.7.1-12
- Revert back to version 1.7.1-9

* Mon Dec 11 2006 Christopher Stone <chris.stone@gmail.com> 1.7.1-11
- Remove all Obsolete/Provides
- Remove Requires on all devel packages

* Sun Dec 10 2006 Christopher Stone <chris.stone@gmail.som> 1.7.1-10
- Remove macosx examples
- Move header files into main package
- Move examples into examples subpackage
- python(abi) = 0:2.5

* Wed Sep 06 2006 Christopher Stone <chris.stone@gmail.com> 1.7.1-9
- No longer %%ghost pyo files. Bug #205396

* Sat Sep 02 2006 Christopher Stone <chris.stone@gmail.com> 1.7.1-8
- FC6 Rebuild

* Wed Jun 28 2006 Christopher Stone <chris.stone@gmail.com> 1.7.1-7.fc6.1
- Rebuild bump

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
