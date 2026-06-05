#if run webased Paraview should uncomm belo 2 lines
#cd /home/mich/apps/BladeBuilderStability/ParaView-5.10.0-MPI-Linux-Python3.9-x86_64
#./start.sh
cd ~/apps/blade-ri/Application/aero_shape/
f8551=`ps aux|grep 8551|grep -v grep`
f8552=`ps aux|grep 8552|grep -v grep`
f8181=`ps aux|grep 8181|grep -v grep`
#at py312 env which in .bashrc 
if  [ "${f8551}" = "" ]; then
  echo "start port 8551 at dir path" `pwd`
  source activate py312
  streamlit run bbs.py --server.enableXsrfProtection=false --server.port 8551 & 
fi

cd ../../

if  [ "${f8181}" = "" ]; then
  source activate as1
  echo "start port 8181 at path " `pwd`
  nohup python app.py runserver -h 0.0.0.0 -p 8181 >/dev/null 2>&1 &
fi

