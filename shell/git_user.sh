#!/bin/bash

function echo_git_user() {
    for file in `ls $1`; do
        if [ -d $1"/"$file ]; then
            if [ -d $1"/"$file"/.git" ]; then
                echo $1"/"$file
                cd $1"/"$file
                git config --list | grep user | tail -n 2 -
                cd ..
            else
                echo_git_user $1"/"$file
            fi
        fi
    done
}

echo_git_user $1
