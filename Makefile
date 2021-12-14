SHELL := /bin/bash

ifeq ($(PREFIX),)
	PREFIX := /srv/salt/salt
endif

all:
	@echo "make install - Install into DESTDIR"

install:
	[ -d $(DESTDIR)$(PREFIX) ] || mkdir -p $(DESTDIR)$(PREFIX)
	for dir in salt/_grains salt/_modules salt/_utils ; do \
		for file in `find "$$dir" -type f` ; do \
			target="$(DESTDIR)$(PREFIX)/$${file#*/}" ; \
			install --mode=0644 --compare -D --verbose "$$file" "$$target" ; \
		done ; \
	done || true
