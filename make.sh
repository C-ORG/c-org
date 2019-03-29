#!/bin/bash

help() {
	functions=$(echo $(egrep '^\w+\(\)' ./make.sh | cut -d'(' -f1) | sed 's/ / | /g')
	cat <<-EOF
	Usage: $0 [$functions]
	EOF
}

init() {
	# add git pre-commit if not present
	if [ ! -e .git/hooks/pre-commit -a ! -L .git/hooks/pre-commit ]; then
		ln -s ./hack/hooks/pre-commit .git/hooks/pre-commit
	fi
}

[ $# -eq 0 ] && help || "$@"
