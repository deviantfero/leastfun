#!/bin/bash

function install_dependencies {
	echo "INSTALLING DEPENDENCIES"
	version="$( uname -r | grep ARCH )"

	if [ -n "$version"  ]; then
		echo ":: ARCH LINUX DETECTED"
		sh -c "sudo pacman -S python-gi python-matplotlib python-sympy"
		echo ":: DEPENDENCIES INSTALL COMPLETE"
	else
		version="$( uname -a | grep -Eo "(eneric|bian)" )"
		if [ -n "$version" ]; then
			echo ":: DEBIAN OR *BUNTU DETECTED"
			sh -c "sudo apt-get install feh python3-gi python-gobject python3-pip python-imaging python3-matplotlib python3-numpy python3-reportlab && sudo pip3 install sympy"
		else
			echo ":: ANOTHER DISTRO DETECTED:: INSTALL DEPENDENCIES FOR YOUR DISTRO"
			echo
		fi
	fi
}


usr="$(whoami)"
if [[ "$usr" != "root" ]]; then
	install_dependencies
else
	echo "don't run as sudo"
fi
