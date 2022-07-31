#  Adjusted for AWS CLI Version 2, Stephen Borsay
#  Changed 1000 iterations to 5

#!/bin/bash

mqtttopic='<Insert-Your-MQTT-Topic-Here>'
iterations=10
wait=5
region='<Insert-Your-AWS-Region-Here>'
profile='default'  

for (( i = 1; i <= $iterations; i++)) {

  #CURRENT_TS=`date +%s`
  #DEVICE="P0"$((1 + $RANDOM % 5))
  #FLOW=$(( 60 + $RANDOM % 40 ))
  #TEMP=$(( 15 + $RANDOM % 20 ))
  #HUMIDITY=$(( 50 + $RANDOM % 40 ))
  #VIBRATION=$(( 100 + $RANDOM % 40 ))
  temperature=$(( 15 + $RANDOM % 20 ))
  humidity=$(( 50 + $RANDOM % 40 ))

  # 3% chance of throwing an anomalous temperature reading
  if [ $(($RANDOM % 100)) -gt 97 ]
  then
    echo "Temperature out of range"
    TEMP=$(($TEMP*6))
  fi

  echo "Publishing message $i/$ITERATIONS to IoT topic $mqtttopic:"
  echo "temperature: $temperature"
  echo "humidity: $humidity"

 #use below for AWS CLI V2
 aws iot-data publish --topic "$mqtttopic" --cli-binary-format raw-in-base64-out --payload "{\"temperature\":$temperature,\"humidity\":$humidity}" --profile "$profile" --region "$region"

  sleep $wait
}
