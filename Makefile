#
# Makefile for local scripts
#

APPS := diremenu diresetup direconfig direswitch direwsdr diretail.desktop YAAC.desktop

all : $(APPS)

	@echo " "
	@echo " Install with "
	@echo "      sudo make install"
	@echo ""

diremenu :

direconfig :

direswitch :

INSTALLDIR := /usr/local
SSERVICEDIR := /etc/systemd/system

INSTALL=install

.PHONY: install
install : $(APPS)

	$(INSTALL) diremenu $(INSTALLDIR)/bin
	$(INSTALL) diresetup $(INSTALLDIR)/bin
	$(INSTALL) direconfig $(INSTALLDIR)/bin
	$(INSTALL) direswitch $(INSTALLDIR)/bin
	$(INSTALL) diremenuup $(INSTALLDIR)/bin
	$(INSTALL) direwsdr $(INSTALLDIR)/bin
	$(INSTALL) -m 644 direwolf.service $(SSERVICEDIR)
	$(INSTALL) direwolf.initd /etc/init.d/direwolf
	$(INSTALL) -m 644 diretail.desktop /usr/share/applications/diretail.desktop
	$(INSTALL) YAAC.sh $(INSTALLDIR)/bin
	$(INSTALL) -m 644 YAAC.desktop /usr/share/applications/YAAC.desktop
	systemctl daemon-reload

diretail.desktop :

	@echo "Generating customized diretail.desktop ..."
	@echo '[Desktop Entry]' > $@
	@echo 'Type=Application' >> $@
ifneq ($(wildcard /usr/bin/lxterminal),)
	@echo "Exec=lxterminal -t \"Dire Tail\" -e \"tail -f $(HOME)/direwolf.output\"" >> $@
else ifneq ($(wildcard /usr/bin/lxterm),)
	@echo "Exec=lxterm -hold -title \"Dire Tail\"  -e \"tail -f $(HOME)/direwolf.output\"" >> $@
else
	@echo "Exec=xterm -hold -title \"Dire Tail\" -e \"tail -f $(HOME)/direwolf.output\"" >> $@
endif
	@echo 'Name=Dire Tail' >> $@
	@echo 'Comment=View direwolf background' >> $@
	@echo 'Icon=/usr/share/direwolf/dw-icon.png' >> $@
	@echo "Path=$(HOME)" >> $@
	@echo '#Terminal=true' >> $@
	@echo 'Categories=HamRadio' >> $@
	@echo 'Keywords=Ham Radio;APRS;Soundcard TNC;KISS;AGWPE;AX.25' >> $@

YAAC.desktop :

	@echo "Generating customized YAAC.desktop ..."
	@echo '[Desktop Entry]' > $@
	@echo 'Type=Application' >> $@
ifneq ($(wildcard /usr/bin/lxterminal),)
	@echo "Exec=lxterminal -t \"YAAC\" -e \"$(HOME)/YAAC.sh\"" >> $@
else ifneq ($(wildcard /usr/bin/lxterm),)
	@echo "Exec=lxterm -hold -title \"YAAC\"  -e \"($HOME)/YAAC.sh\"" >> $@
else
	@echo "Exec=xterm -hold -title \"YAAC\" -e \"($HOME)/YAAC.sh\"" >> $@
endif
	@echo 'Name=YAAC' >> $@
	@echo 'Comment=Yet Another APRS Client' >> $@
	@echo 'Icon=/usr/share/direwolf/dw-icon.png' >> $@
	@echo "Path=$(HOME)" >> $@
	@echo '#Terminal=true' >> $@
	@echo 'Categories=HamRadio' >> $@
	@echo 'Keywords=Ham Radio;APRS;Soundcard TNC;KISS;AGWPE;AX.25' >> $@

.PHONY: install-rpi
install-rpi : YAAC.sh
	ln -f -s $(INSTALLDIR)/bin/YAAC.sh $(HOME)/YAAC.sh
	ln -f -s /usr/share/applications/diretail.desktop ~/Desktop/diretail.desktop
	ln -f -s /usr/share/applications/YAAC.desktop ~/Desktop/YAAC.desktop

.PHONY: clean
clean :
	rm -f diretail.desktop YAAC.desktop
	git fetch --force && git reset --hard origin/master


depend : $(wildcard *.c)
	makedepend -f $(lastword $(MAKEFILE_LIST)) -- $(CFLAGS) -- $^


#
# The following is updated by "make depend"
#
# DO NOT DELETE
