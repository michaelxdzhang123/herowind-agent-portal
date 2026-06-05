#/bin/shell
# author: Michael for blac project sphinx
base=/home/mich/apps/BladeAI
rm -rf ./build/

rst=`ls ./source/*.rst |grep -v installation|grep -v index |grep -v introduction|grep -v WorkOrder|grep -v user_guide|grep -v test_main|grep -v developer_guide|grep -v aero_shape.rst`
for file in $rst
do
 rm  $file
done

sphinx_base=$base/docs/sphinx/source
appdir=$base/Application
#tool_dir=$base/Framework/
#mod_dir=$base/Framework/Modules
#Application
echo make Applicaiton apidocs-----
#sleep 1
#dirs=`ls $appdir`
#rm $sphinx_base/modules.rst
#for dir in $dirs
#do
#sphinx-apidoc $appdir/$dir -o $sphinx_base
#echo $dir
#sleep 2
#mv  source/modules.rst ./source/$dir.rst
#done
echo make modules ------
sleep 1
#dirs=`ls $mod_dir`
#build modules at BlacFramework/Modules
#rm $sphinx_base/modules.rst
#for dir in $dirs
#do
#sphinx-apidoc $mod_dir/$dir -o $sphinx_base
#mv  source/modules.rst ./source/$dir.rst
#done

# copy doscs stab2
echo now make clean annd make html---------------
rm -rf ./build
make clean && make html
echo 'build done! '


