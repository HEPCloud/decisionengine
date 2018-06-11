# SoftRelTools GNUmakefile for NovaRunControl C++ unittest directory 

# Build the unittest library
LIB = lib$(PACKAGE)unittest

# Compile all the .cpp files in this directory into the library
LIBCPPFILES = $(wildcard *.cpp)

# Build the package unittest binaries
TBINS = $(basename $(wildcard *.cc))

# Use the "simple binary" rules to generate the unittest binaries
SIMPLEBINS = $(TBINS)

# Link the binaries with the current package library and the
# unittest library
BINLIBS += -l$(PACKAGE) -l$(PACKAGE)unittest -lErrorHandlerMessages -lErrorHandler -lboost_unit_test_framework-mt -lNovaTimingUtilities

# Run each of the unit tests in this directory
UNITTESTS = $(TBINS)

################################
include SoftRelTools/arch_spec_boost.mk
include SoftRelTools/qt.mk
include SoftRelTools/standard.mk
include SoftRelTools/arch_spec_rcclient.mk
include SoftRelTools/arch_spec_mf_shared.mk
include SoftRelTools/arch_spec_mfextensions.mk
