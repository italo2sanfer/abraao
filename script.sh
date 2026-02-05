#!/bin/bash

Q_SEARCH="IFFMa"
Q_PASSWORD="S070b"
URL_OBTAIN='http://localhost:8001/api/obtain-token/'
URL_SEARCH="http://localhost:8001/api/joao/search/?q=$Q_SEARCH"
URL_PASSWORD="http://localhost:8001/api/judite/$Q_PASSWORD/passwd/"
TOKEN=$(curl -X POST $URL_OBTAIN -H "Content-Type: application/json" -d '{"username": "italo2sanfer", "password": "!Obediencia8"}' | jq -r '.token')
RESULT_SEARCH=```curl -X GET $URL_SEARCH -H "Authorization: Bearer $TOKEN"```
RESULT_PASSWORD=```curl -X GET $URL_PASSWORD -H "Authorization: Bearer $TOKEN"```

echo -e "\n$RESULT_SEARCH\n\n$RESULT_PASSWORD\n\n$TOKEN\n\n"