# Set up:
- Clone repo with **submodule**:
```
git clone --recurse-submodules https://github.com/LeDuySon/TrackingErrorAnalysis.git
```
- Install necessary packages:
```
pip install -r requirements.txt
```

# Guide Video:
- Link: https://drive.google.com/file/d/1x8Th8yuI0bWDxslnVbkEaee0ENlupWiY/view?usp=sharing

# Data prepare
- Get **groudtruth files** to folder **static/test_data/gt**, run:
```
python get_gt_file.py --root_path {folder_contain_your_gt_files} --save_path {default: static/test_data/gt}
```
- Get **prediction files** to folder **static/test_data/pred**

- Create video folder tree in TrackEval/video/**\<TRACKER\>**: 
  - Default **\<TRACKER\>**: ch_yolov5m_deep_sort
  - In folder utils/, run:

  ```
  python create_video_tree_trackeval.py --video_path {YOUR_VIDEO_FOLDER} --save_path ../TrackEval/video/
  ```

  - Results:

  ```

  {TrackEval/video/<TRACKER>}
  ├── NVR-CH01_S20210607-095126_E20210607-102303.mp4
  ├── NVR-CH02_S20210607-094604_E20210607-094856.mp4
  ├── NVR-CH02_S20210607-173836_E20210607-173936.mp4
  ├── NVR-CH02_S20210608-085112_E20210608-085718.mp4
  ├── NVR-CH04_S20210608-083726_E20210608-083850.mp4
  ├── NVR-CH04_S20210609-113009_E20210609-113658.mp4

  ```



# Evaluate

- Run: 
```
bash create_mot_eval.sh {save_name} {TrackEval/video/<TRACKER>} evaluate
```
- Mot output in folder TrackEval/benchmarks

# Error Analysis
- To know how error analysis work, reference: 
  **https://github.com/thanhtvt/TrackEval/blob/master/docs/MOTChallenge-Official/whats_new.md**
- Run:
```
bash create_mot_eval.sh {save_name} {TrackEval/video/<TRACKER>} error_analysis
```
- Error analysis output in folder TrackEval/boxdetails and TrackEval/output
