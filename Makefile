#
# Makefile for local scripts
#

APPS := diremenu direconf direswit

all : $(APPS)

	@echo " "
	@echo " Install with "
	@echo "      sudo make install"
	@echo "" 
   
diremenu : 

direconf : 

direswit :

INSTALLDIR := /usr/local

INSTALL=install

.PHONY: install
install : $(APPS)

	$(INSTALL) diremenu $(INSTALLDIR)/bin
	$(INSTALL) direconf $(INSTALLDIR)/bin
	$(INSTALL) direswit $(INSTALLDIR)/bin

