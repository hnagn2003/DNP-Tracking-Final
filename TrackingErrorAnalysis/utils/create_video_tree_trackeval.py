import argparse
import shutil
import os
import glob

def create_folder(path): 
    if(not os.path.exists(path)): 
        os.makedirs(path)

# def handler(video_path, seq_path): 
#     if(not os.path.exists(seq_path)):
#         os.makedirs(seq_path)
        
#     new_video_path = os.path.join(seq_path, os.path.basename(video_path))
#     shutil.copy2(video_path, seq_path)
#     # rename video 
#     os.rename(new_video_path, os.path.join(seq_path, "raw.mp4"))
    
def run(args):
    videos = glob.glob(os.path.join(args.video_path, "*.mp4")) 
    
    # modify save path wrp to track benchmark
    save_path = os.path.join(args.save_path, args.track_benchmark)
    create_folder(args.save_path)
    
    for video_path in videos:
        shutil.copy2(video_path, save_path)
        
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--video_path', '-vp', type=str,
                                        help="path to folder contain videos")
    parser.add_argument('--save_path', '-sp', type=str,
                                        help="path to create video_tree")
    parser.add_argument('--track_benchmark', '-tb', type=str, 
                                        help="name of our track eval benchmark", default="ch_yolov5m_deep_sort")
    args = parser.parse_args()

    run(args)
