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

## 1. Run inference

```bash
python tools/inference.py
```

## 2. Convert predict output to MOT format

```bash
python pred2MOT/pred_to_mot.py
```
## 3. run evaluate
```bash
cd TrackingErrorAnalysis
bash create_mot_eval.sh static/output TrackEval/video/ch_yolov5m_deep_sort evaluate mot
```
