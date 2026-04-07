#!/bin/bash

HOST="http://localhost:8001"
#HOST="https://ideal-train-wv4jxx5gv9rhvvj9-8002.app.github.dev"
# Para o caso de testar um token inválido
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NzA5MDQ4NDksImlhdCI6MTc3MDkwMzY0OX0.pkrOMTq-9a6CRj_5-t0rGsp0J3WbDz1vIq9UecZccGw"

URL_OBTAIN="$HOST/api/obtain-token/"
RESULT_OBTAIN=$(curl -X POST "$URL_OBTAIN" -H "Content-Type: application/json" -d '{"username": "chrome", "password": "S!mple@ndPruden7"}'  | jq -r '.token')
TOKEN=$RESULT_OBTAIN
echo -e "\n$TOKEN\n\n"

URL_VERIFY="$HOST/api/token/remaining-time/"
RESULT_VERIFY=```curl -X GET $URL_VERIFY -H "Authorization: Bearer $TOKEN"```
echo -e "\n$RESULT_VERIFY\n\n"

Q_SEARCH="IFFMa"
URL_SEARCH="$HOST/api/joao/search/?q=$Q_SEARCH"
RESULT_SEARCH=```curl -X GET $URL_SEARCH -H "Authorization: Bearer $TOKEN"```
echo -e "\n$RESULT_SEARCH\n\n"

Q_PASSWORD="S070b"
URL_PASSWORD="$HOST/api/judite/$Q_PASSWORD/passwd/"
RESULT_PASSWORD=```curl -X GET $URL_PASSWORD -H "Authorization: Bearer $TOKEN"```
echo -e "\n$RESULT_PASSWORD\n\n"
