test:
	pwd
	ls
	pylint --rcfile=`pwd`/pylint.conf dao
	pyline --rcfile=`pwd`/pylint.conf service
	sh `pwd`/ci/run_tests.sh