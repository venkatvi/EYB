 hadoop \
jar /usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar \
-D mapred.reduce.tasks=1 \
-mapper "python $PWD/matMapper.py" \
-reducer "python $PWD/matReducer.py" \
-input /home/hduser/eybd/eyb_indata/*.csv \
-output /home/hduser/eybd/eyb_outdata  # dont mkdir this folder. hadoop will do it for you! 

