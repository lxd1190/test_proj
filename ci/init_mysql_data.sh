#!/usr/bin/env bash
# Run tests

echo $DIR, `pwd`

echo "create database metis"
echo "show databases"|mysql -h127.0.0.1 -uroot
