openssl genrsa -out formant-lan-ca.key 4096
openssl req -x509 -new -nodes -key formant-lan-ca.key -sha256 -days 365 -out formant-lan-ca.crt
rm config.cnf | false
ip=$(hostname -I | cut -d' ' -f1)
cp config.cnf.template config.cnf
sed -i "s/IP_ADDRESS/${ip}/g" config.cnf
openssl genrsa -out server.key 4096
openssl req -new -key server.key -config config.cnf -out server.csr
openssl x509 -req -in server.csr -CA formant-lan-ca.crt -CAkey formant-lan-ca.key -CAcreateserial -out server.crt -days 365 -sha256 -extfile config.cnf -extensions req_ext
rm config.cnf