moduleName=$1
inputpath=$2
date=$3


echo HELLO
echo Welcome to the X-world!
echo Module Name: ${moduleName}
echo Path of config files:${inputpath}
echo Date:${date}
echo Is the info above correct? "(y/n)"
c=0
while [ $c != y ]
do
sleep 1
read c
done

ls  ${inputpath}/phCalibration*
echo Are there any phCalibration files"?(y/n)"
c=0
while [ $c != y ]
do
sleep 1
read c
done

sed -i 's/testboardName .*/testboardName \*/' ${inputpath}/configParameters.dat
sed -i 's|00a basea   0x[0-9a-f][0-9a-f]|00a basea   0xdb|' ${inputpath}/tbmParameters_C0a.dat
sed -i 's|00a basea   0x[0-9a-f][0-9a-f]|00a basea   0xdb|' ${inputpath}/tbmParameters_C0b.dat
sed -i 's|00e basee   0x[0-9a-f][0-9a-f]|00e basee   0xc8|' ${inputpath}/tbmParameters_C0a.dat

echo Did you turn the X-ray tube to Highrate testing position "(45 degree)"? "(y/n)"
c=0
while [ $c != y ]
do
sleep 1
read c
done

echo Did you turn on the Coldplate "(12V)" and wait the temperature cool down to 17C? "(y/n)"
c=0
while [ $c != y ]
do
sleep 1
read c
done

echo Did you turn on the high voltage supply"(Keithley)"?"(y/n)"
c=0
while [ $c != y ]
do
sleep 1
read c
done


#############################Highrate###################################################

./bin/pXar -T 35 -d ${inputpath} -r highrate.root 

echo Highrate testing done!
python split_hr.py ${inputpath} ${moduleName} ${date}
python splitdc05.py ${inputpath} ${moduleName} ${date}
python splitdc15.py ${inputpath} ${moduleName} ${date}




##############################Fluorescence#####################################
###
echo Please make sure you turn off everything!
echo Please type "y" after you turned everything off
c=0
while [ $c != y ]
do
sleep 1
read c
done



#####################Database#################################################
#echo Please check the Fluorescence results "in" the browser
#echo "Type TBrowser r in the terminal" 

root ${inputpath}/Fluorescence.root

echo Is there any bad ROC?
echo If yes please type the list of ROC numbers"e.g: 1,2,3" Otherwise please press enter
read badRocs

~/RunAllScripts.sh ${moduleName} ${inputpath} ${badRocs}

echo This is the end, my friend
echo Here are all the results you need: ~/FPIX_ProductionMode/XRayTesting/${moduleName}/DataBase
echo Please carefully check all the plots and sumbit them to the DB: http://www.physics.purdue.edu/cmsfpix/Submission_p/index.php
