#!/bin/bash
echo "{ \"username\": \"test\",\"password\": \"test\", \"host\": \"test\", \"database\":\"waterfall\"}"  > src/db/sql_config.json
py.test