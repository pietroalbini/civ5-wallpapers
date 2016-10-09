# Copyright (C) 2016 Pietro Albini <pietro@pietroalbini.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Configuration
SOURCE = civ5_wallpapers
PACKAGES_OUT = build/packages

# Executables
PYTHON = python3
GPG = gpg
TWINE = twine

.PHONY: build sign _pre-sign


# Basic packages building

build: $(PACKAGES_OUT)/*.tar.gz $(PACKAGES_OUT)/*.whl

$(PACKAGES_OUT):
	@mkdir -p $(PACKAGES_OUT)

$(PACKAGES_OUT)/*.tar.gz: $(PACKAGES_OUT) setup.py $(wildcard $(SOURCE)/*)
	@$(PYTHON) setup.py sdist -d $(PACKAGES_OUT)

build/packages/*.whl: $(PACKAGES_OUT) setup.py $(wildcard $(SOURCE)/*)
	@$(PYTHON) setup.py bdist_wheel -d $(PACKAGES_OUT)


# Packages signing

sign: _pre-sign $(addsuffix .asc,$(filter-out $(wildcard $(PACKAGES_OUT)/*.asc),$(wildcard $(PACKAGES_OUT)/*)))

_pre-sign:
	@rm -f $(PACKAGES_OUT)/*.asc

$(PACKAGES_OUT)/%.asc:
	@$(GPG) --detach --armor --sign $(PACKAGES_OUT)/$*


# Packages uploading

upload: build sign
	@$(TWINE) upload --config-file .pypirc -r upload --skip-existing $(PACKAGES_OUT)/*
