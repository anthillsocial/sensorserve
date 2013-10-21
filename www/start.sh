#!/usr/bin/env bash
#Kill all processes open on port 4000
netstat -tulnap 2>/dev/null | grep 4000 | awk {'print $7'} | awk -F/ {'print $1'} | xargs -I {} kill -9 {}
node server.js
