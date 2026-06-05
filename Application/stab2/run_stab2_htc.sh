
#!/bin/bash

# Use environment variable for HAWC2S path, fallback to default location
HAWC2S_PATH=${HAWC2S_PATH:-"$HOME/Applications/DTU/HAWCStab2/v2.16/x86_64/beta-3b834cf7/HAWC2S.exe"}

if  [ "$1" = "" ]; then
  echo "run default .cmb " `pwd`
  $1=15_MW_hs2_locked_case_op1.htc
  "$HAWC2S_PATH" "$1"
  exit
fi
"$HAWC2S_PATH" "$1"
