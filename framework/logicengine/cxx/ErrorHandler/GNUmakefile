# SoftRelTools GNUmakefile for ErrorHandler C++ source directory 

# Generate C++ classes from XML Schema Definition files
#CSTXSD_XSD_DIR := ../../config
#CSTXSD_INC_DIR := ../include
#CSTXSD_SRC_DIR := .
#CSTXSD_INC_PREFIX := $(PACKAGE)
#CSTXSD_XSD_FILES := $(wildcard $(CSTXSD_XSD_DIR)/*.xsd)
#CSTXSD_NAMESPACE := novadaq::novaruncontrol
#CSTXSD_RUN_TAILOR_SCRIPT = yes

# Generate DDS datatype classes from IDL
#DDSIDL_IDL_DIR   := ../../config
#DDSIDL_INC_DIR   := ../include
#DDSIDL_SRC_DIR   := .
#DDSIDL_IDL_FILES := $(DDSIDL_IDL_DIR)/RunControlMessages.idl
#DDSIDL_GEN_LANG  := cpp

QT_QRC_FILES     := rc

# List the QT UI files
QT_UI_FILES := MsgAnalyzerDlg MsgBox

QT_UI_OUTPUT_DIR := ../include

QT_MOC_FILES     := MsgAnalyzerDlg MsgBox qt_rule_engine qt_log_reader ma_rcclient

# Build the package library
LIB = lib$(PACKAGE) 

# produce a shared library
#LIB_TYPE := both
LIB_TYPE := shared

# Compile all the .cpp files in this directory into the library
LIBCPPFILES = EHListener.cpp \
	      ma_boolean_andexpr.cpp \
              ma_boolean_cond.cpp \
              ma_boolean_expr.cpp \
              ma_cell.cpp \
              ma_condition.cpp \
              ma_domain_andexpr.cpp \
              ma_domain_cond.cpp \
              ma_domain_expr.cpp \
              ma_cond_test_andexpr.cpp \
              ma_cond_test_primary.cpp \
              ma_cond_test_expr.cpp \
              ma_action.cpp \
              ma_action_script.cpp \
              ma_action_mail.cpp \
              ma_action_rcmsg.cpp \
	      ma_function.cpp \
              ma_function_count.cpp \
              ma_function_countpercent.cpp \
              ma_function_is_syncd.cpp \
              ma_test_function.cpp \
              ma_tf_grp_to_number.cpp \
              ma_hitmap.cpp \
              ma_parse.cpp \
              ma_participants.cpp \
              ma_rcclient.cpp \
              ma_richmsg.cpp \
              ma_rule.cpp \
              ma_rule_engine.cpp \
              ma_utils.cpp \
              qt_rule_engine.cpp \
              qt_log_reader.cpp \
              MsgAnalyzerDlg.cpp \
              MsgBox.cpp \
              NodeInfo.cpp 

# Build the package binaries
BINS = $(basename $(wildcard *.cc))

# Use the "simple binary" rules to generate the binaries
SIMPLEBINS = $(BINS)

# Link the binaries with the libraries defined in the *.mk files
BINLIBS += -l$(PACKAGE) -lErrorHandlerMessages -lNovaTimingUtilities

# Build Doxygen documentation
#DOXYGEN_CONFIG_FILE = ../../config/doxygen_cxx.config
#DOXYGEN_OUT_DIR = $(docdir)/$(PACKAGE)/cxx
#DOXYGEN_PREREQ = $(LIBCPPFILES)

################################
include SoftRelTools/arch_spec_boost.mk
include SoftRelTools/qt.mk
include SoftRelTools/arch_spec_rcclient.mk
include SoftRelTools/arch_spec_mf_shared.mk
include SoftRelTools/arch_spec_mfextensions.mk
include SoftRelTools/standard.mk
include SoftRelTools/arch_spec_rms.mk