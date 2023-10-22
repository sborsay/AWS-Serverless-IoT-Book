Key words in your post "different versions of cURL" is helping.

I found a solution:

Un-install Git-2.42.0.2-64-bit (with curl 8.2.1) which is the latest version at time of try-out.
Install an older version Git-2.24.1.2-64-bit link (with curl 7.67.0)
Change names of the original certs and key to private.pem.key &  certificate.pem.crt and using the same name in curl command below:
curl --tlsv1.2 ^
--cacert AmazonRootCA1.pem ^
--key private.pem.key ^
--cert certificate.pem.crt ^
--request POST ^
--data "{\"Temperature\": 77, \"Humidity\": 88, \"Time\": 12349876}" ^
"https://<my end point>:8443/topics/outTopic?qos=1"
Response:
{"message":"OK","traceId":"cad83a13-cbee-cffc-30d5-07cc04fd9742"}

Now my mqtt test client is receiving data.
