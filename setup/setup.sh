#!/usr/bin/env bash

create(){
    echo "BOT_TOKEN = " >> ../.env
    if ! command -v virtualenv &> /dev/null
    then
        echo -e "\n'virtualenv' could not be found, installing:\n----------"
        pip3 install virtualenv   
    fi

    if [[ "$?" -eq 0 ]]
    then
        echo "----------"
        virtualenv ../venv

        echo -e "\n----------\nCompleted! Now just activate the environment.\n"
    else
        echo -e "\nSomething doesn't seem right. Check and try again."
        exit
}

create