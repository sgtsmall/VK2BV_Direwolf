#
# Makefile for local scripts
#

APPS := diremenu configdirew

all : $(APPS)

   @echo " "
   @echo " Install with "
   @echo "      sudo make install"
   @echo "" 
   
diremenu : diremenu

configdirew : configdirew

INSTALLDIR := /usr/local

INSTALL=install

.PHONY: install
install : $(APPS)

    $(INSTALL) diremenu $(INSTALLDIR)/bin
    $(INSTALL) configdirew $(INSTALLDIR)/bin

