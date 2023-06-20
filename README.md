# Installation
```bash
#setupenv
conda create -n open-mmlab python=3.9.16
conda activate open-mmlab
pip install torch==1.8.0+cu111 -f https://download.pytorch.org/whl/torch_stable.html
pip install torchvision==0.9.0
#VOT experiments
pip install git+https://github.com/votchallenge/toolkit.git
#mmcv
pip install openmim
mim install mmcv-full==1.7.0
#mmdet
git clone https://github.com/open-mmlab/mmdetection.git
cd mmdetection
git checkout 2.x
pip install -r requirements/build.txt
pip install -v -e .
cd..
#mmtracking
pip install -r requirements/build.txt
pip install -v -e . 
#VOT
pip install git+https://github.com/JonathonLuiten/TrackEval.git
#run demo
python demo/demo_mot_vis.py configs/mot/deepsort/sort_faster-rcnn_fpn_4e_mot17-private.py --input demo/demo.mp4 --output mot.mp4
```

# How to run

## 1. Run evaluate
First, prepare all the video you need to run evaluate to /data/DNP/video/
Then get the checkpoint file to /checkpoint/
You can modify everything (input, output path, config, checkpoint file, ...) in inference.py

```bash
python tools/inference.py
```
After this step, you'll get the output is predicted files in folder /output/pred/

## 2. Convert predict output to MOT format
Then you must convert the predict files in above step to the right MOT format
```bash
python pred2MOT/pred_to_mot.py --input output/pred --output pred2MOT/converted
```
Output MOT files will go to pred2MOT/converted (or wherever you specified)

## 3. Run evaluate

Final is running evaluate
First prepare the data
copy all MOT files (from step 2) to TrackingErrorAnalysis/static/test_data/pred
copy all grouth truth that sếp Tùng provided trên Slack to TrackingErrorAnalysis/static/test_data/pred
copy all video file that sếp Tùng provided trên Slack too to TrackingErrorAnalysis/TrackEval/video/ch_yolov5m_deep_sort
Please note that three folder above should are respective.
Then run this bash 

```bash
cd TrackingErrorAnalysis
bash create_mot_eval.sh static/output TrackEval/video/ch_yolov5m_deep_sort evaluate mot
```
That's a basic line. If having any issue please tell me in "issue tab"