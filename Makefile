#
# Makefile for local scripts
#

APPS := diremenu direconfig direswitch

all : $(APPS)

	@echo " "
	@echo " Install with "
	@echo "      sudo make install"
	@echo "" 
   
diremenu : 

direconfig : 

direswitch :

INSTALLDIR := /usr/local
SSERVIVEDIR := /lib/systemd/system

INSTALL=install

.PHONY: install
install : $(APPS)

	$(INSTALL) diremenu $(INSTALLDIR)/bin
	$(INSTALL) direconfig $(INSTALLDIR)/bin
	$(INSTALL) direswitch $(INSTALLDIR)/bin
	$(INSTALL) direwolf.service $(SSERVICEDIR)
	$(INSTALL) direwolf.initd /etc/init.d/direwolf
