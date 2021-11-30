#!/bin/bash

helpFunction()
{
   echo ""
   echo "Usage: $0 -m moduleName"
   echo -e "\t-m Python moduleName existing in project"
   exit 1 # Exit script after printing help
}

getopts "m:" opt
case "$opt" in
  m ) moduleName="$OPTARG" ;;
  ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
esac

case "$moduleName" in
  myDLQSender ) ;;
  ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
esac

# Print helpFunction in case parameters are empty
if [ -z "$moduleName" ]
then
   echo "Required parameter is empty";
   helpFunction
fi

# Begin script in case all parameters are correct
echo "Compressing" "$moduleName" "module";
mkdir -p ./dist
cd ./"$moduleName" && zip -r ../dist/"$moduleName".zip . && cd ..;