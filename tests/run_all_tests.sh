#!/bin/bash

# Runs unit tests in testapp/tests.py with all settings file configurations (see testproject/settings/*)
settings_modules=(
    'default_config'
    'test_request_black_and_whitelist'
    'test_hostname_blacklist'
    'test_port_black_and_whitelist'
    'test_ip_black_and_whitelist'
)
sum_retval=0

for module_name in "${settings_modules[@]}"
do
    echo "===================================================="
    echo "Running tests with settings module: $module_name"
    echo "===================================================="
    DJANGO_SETTINGS_MODULE="testproject.settings.$module_name" python manage.py test
    let sum_retval+="$?"
done

evaluate_tests () {
    if [ $1 -eq 0 ]
    then
        echo "All test runs passed"
        return 0
    else
        echo "$1 test runs failed"
        return 1
    fi
}

evaluate_tests $sum_retval
