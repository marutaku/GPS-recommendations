#!/bin/bash
echo "==========RESTART=========="
uwsgi --stop uwsgi.pid
uwsgi --ini myapp.ini &
wait $!
echo $?
echo "=======RESTART FINISH======"

