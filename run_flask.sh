#!/bin/bash
MYCONDA=/home/mich/anaconda3
source /home/mich/.bashrc
#source $MYCONDA/etc/profile.d/conda.sh
env > terminal_env.txt
source activate as1

# Verify the environment is activated
echo "Active environment: $CONDA_DEFAULT_ENV"

# Run your commands in the activated environment
# Example: python script.py
python --version

# Optional: Deactivate the environment when done
# conda deactivate
f8181=`ps aux|grep 8181|grep -v grep`
if  [ "${f8181}" = "" ]; then
  echo "start port 8181 at path " `pwd`
  nohup python app.py runserver -h 0.0.0.0 -p 8181 >/dev/null 2>&1 &
fi

