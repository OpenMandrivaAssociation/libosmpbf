%define devname %mklibname osmpbf -s -d

Name: libosmpbf
Version: 1.3.3
Release: 2
Source0: https://github.com/scrosby/OSM-binary/archive/v%{version}.tar.gz
Summary: Library for writing OpenStreetMap PBF files
URL: https://github.com/scrosby/OSM-binary
License: GPLv3
Group: System/Libraries
BuildRequires: cmake ninja
BuildRequires: pkgconfig(zlib)
BuildRequires: pkgconfig(protobuf)
BuildRequires: pkgconfig(protobuf-lite)
# --- for Java bindings ---
BuildRequires: ant
BuildRequires: java-1.8.0-openjdk-devel
BuildRequires: protobuf-java protobuf-java-util
Patch0:	osmpbf-protobuf-java-path.patch

%description
Library for writing OpenStreetMap PBF files

%package java
Summary: Java library for writing OpenStreetMap PBF files
Group: System/Libraries
Requires: protobuf-java

%description java
Java library for writing OpenStreetMap PBF files

%package -n %{libname}
Summary: Library for writing OpenStreetMap PBF files
Group: System/Libraries

%description -n %{libname}
Library for writing OpenStreetMap PBF files

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C

%description -n %{devname}
Development files (Headers etc.) for %{name}.

Library for writing OpenStreetMap PBF files

%prep
%setup -qn OSM-binary-%{version}
%apply_patches
export CXXFLAGS="%{optflags} -I$(pwd)/build/src"
%cmake -G Ninja
mkdir -p src
ln -s . src/osmpbf

%build
%ninja -C build

# For Java bindings
ant

%install
%ninja_install -C build
%if "%{_lib}" != "lib"
mv %{buildroot}%{_prefix}/lib %{buildroot}%{_libdir}
%endif

# For Java bindings
mkdir -p %{buildroot}%{_datadir}/java/
cp osmpbf.jar %{buildroot}%{_datadir}/java/

%files
%{_bindir}/*

%files java
%{_datadir}/java/*.jar

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.a
