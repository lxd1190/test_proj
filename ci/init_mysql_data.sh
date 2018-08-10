#!/usr/bin/env bash
# Run tests

DB_CONTEXT='mysql -h127.0.0.1 -uroot'
echo $DIR, `pwd`

echo "create database metis"|${DB_CONTEXT}
echo "show databases"|${DB_CONTEXT}
