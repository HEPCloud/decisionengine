#!/bin/bash
SUBJECTBASE="[MsgAnalyzer] "
SUBJECT="Error Warning"
EMAIL="a.waldron@sussex.ac.uk"
EMAILMESSAGE="./email_body.txt"
MESSAGE="Keep calm and carry on"


while getopts e:s:b: option
  do
  case "${option}"
      in
      e) EMAIL=${OPTARG};;
      s) SUBJECT=${OPTARG};;
      b) MESSAGE=${OPTARG};;
  esac

done


SUBJECT=$SUBJECTBASE$SUBJECT
printf "$MESSAGE" > $EMAILMESSAGE





/bin/mail -s "$SUBJECT" "$EMAIL" < $EMAILMESSAGE
rm ./email_body.txt
sleep 1 

