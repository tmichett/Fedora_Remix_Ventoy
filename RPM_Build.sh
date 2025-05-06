#!/bin/bash

cp -avR rpmbuild ~
rpmbuild -ba ~/rpmbuild/SPECS/ventoy.spec
