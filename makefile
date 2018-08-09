test:
	pwd
	ls
	export PYTHONPATH=$PYTHONPATH:`pwd`/app
	pylint --rcfile=`pwd`/pylint.conf ./app/dao
	pyline --rcfile=`pwd`/pylint.conf ./app/service
	sh `pwd`/ci/run_tests.sh