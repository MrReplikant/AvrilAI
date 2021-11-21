#!/usr/bin/env bash
set -e
cd "$(dirname "${0}")"
BASE_DIR="$(pwd)"
PACKAGES=(aria2 git unzip wget)

pip_install () {
	if [ ! -d "./venv" ]; then
		# Some distros have venv built into python so this isn't always needed.
		if is_command 'apt-get'; then
			apt-get install python3-venv
		fi
		#WARNING: Changing to --copies for colab users, not optimal way to do this
		python3 -m venv --copies ./venv
	fi
	commit_hash=$(git log --pretty=format:'%h' -n 1)
	echo "You are using https://github.com/cloveranon/Clover-Edition/commit/${commit_hash}"
	source "${BASE_DIR}/venv/bin/activate"
	pip install --upgrade pip setuptools
	pip --no-cache-dir install -r "${BASE_DIR}/requirements/requirements.txt"

	echo "Would you like to install Nvidia CUDA support (~4.5gb) or just use your CPU (~800mb, but much slower)?"
	select yn in "Nvidia CUDA" "CPU only"; do
		case $yn in
			"Nvidia CUDA" ) pip install -r "${BASE_DIR}/requirements/cuda_requirements.txt"; break;;
			"CPU only" ) pip install -r "${BASE_DIR}/requirements/cpu_requirements.txt"; break;;
		esac
	done
}

is_command() {
	command -v "${@}" > /dev/null
}

system_package_install() {
	#why is this list duplicated?
	PACKAGES=(aria2 git unzip wget)
	if is_command 'apt-get'; then
		sudo apt-get install ${PACKAGES[@]}
	elif is_command 'brew'; then
		brew install ${PACKAGES[@]}
	elif is_command 'yum'; then
		sudo yum install ${PACKAGES[@]}
	elif is_command 'dnf'; then
		sudo dnf install ${PACKAGES[@]}
	elif is_command 'pacman'; then
		sudo pacman -S ${PACKAGES[@]}
	elif is_command 'apk'; then
		sudo apk --update add ${PACKAGES[@]}
	else
		echo "You do not seem to be using a supported package manager."
		echo "Please make sure ${PACKAGES[@]} are installed then press [ENTER]"
		read NOT_USED
	fi
}

install_aid () {
#	version_check
	#the order of this may be wrong, changing it back to original for now
	pip_install
	system_package_install
}

install_aid
