#! /usr/bin/Python

import os
import argparse
import shutil
import cv2
import glob

SEQINFO_DICT = {"name": "",
                "imDir": "img1",
                "frameRate": 20,
                "seqLength": 1200,  # all videos just 60 seconds
                "imWidth": 1920,
                "imHeight": 1080,
                "imExt": ".jpg"}

BENCHMARK = "MOT16"

def create_seqinfo(cur_path, **kwargs):

    with open(os.path.join(cur_path, "seqinfo.ini"), "w") as f:
        f.write("[Sequence]\n")
        for k, v in kwargs.items():
            f.write("{}={}".format(k, v) + "\n")

    with open(os.path.join(cur_path, "gt", "seqinfo.ini"), "w") as f:
        f.write("[Sequence]\n")
        for k, v in kwargs.items():
            f.write("{}={}".format(k, v) + "\n")


def create_folder(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)


def create_seqini_mot(seq, video_path):
    """Get info from video -> generate seqini file for mot evaluate

    Notes:
        All video in video_path must have the same name as seq

    Args:
        seq ([type]): name of seq evaluate

    Returns:
        [type]: [description]
    """
    video_name = seq.split(".")[0] + ".mp4"
    print(os.path.join(video_path, video_name))
    cap = cv2.VideoCapture(os.path.join(video_path, video_name))
    if cap is None or not cap.isOpened():
        raise ValueError("Path to video was wrong")

    length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    seqini = SEQINFO_DICT.copy()
    seqini["name"] = seq
    seqini["frameRate"] = int(fps)
    seqini["seqLength"] = length
    seqini["imWidth"] = width
    seqini["imHeight"] = height

    return seqini


def create_seqini_mtmc(seq, video_path):
    """Get info from video -> generate seqini file for MTMC evaluate

    Args:
        seq ([type]): name of seq evaluate

    Returns:
        [type]: [description]
    """
    videos = glob.glob(os.path.join(video_path, "*.mp4"))
    videos = [video for video in videos if os.path.basename(video) != "multiple_view.mp4"]
    length = 0  # contain sum of length of all videos
    for idx, video in enumerate(videos):
        cap = cv2.VideoCapture(video)
        if cap is None or not cap.isOpened():
            raise ValueError("Path to video was wrong")

        length += int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if(idx == 0):
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))

    seqini = SEQINFO_DICT.copy()
    seqini["name"] = seq
    seqini["frameRate"] = int(fps)
    seqini["seqLength"] = length
    seqini["imWidth"] = width
    seqini["imHeight"] = height

    return seqini

def create_seq(seq, root_path, video_path):
    """create seq folder for each seq

    Args:
        seq ([str]): sequence name 
    """
    seq_name = os.path.basename(seq)
    # create seq folder
    create_folder(seq)
    gt_seq_folder = os.path.join(seq, "gt")
    create_folder(gt_seq_folder)
    source_gt = os.path.join(root_path, "gt", seq_name + ".txt")
    shutil.copy(source_gt, os.path.join(gt_seq_folder, "gt.txt"))

    if(EVAL_MODE == "mot"):
        seqinfo = create_seqini_mot(seq_name, video_path)
    elif(EVAL_MODE == "mtmc"):
        seqinfo = create_seqini_mtmc(seq_name, video_path)
    else:
        raise argparse.ArgumentError("eval argument was wrong, valid argument: mot|mtmc")
    create_seqinfo(seq, **seqinfo)


def create_gt_branch(branch_path, root_path, video_path):
    """create gt/ folder and all its children

    Args:
        branch_path ([type]): [description]
        root_path ([type]): [description]
    """
    gt_files = os.listdir(os.path.join(root_path, "gt"))

    for file in gt_files:
        seq_name = file.split(".")[0]
        seq = os.path.join(branch_path, seq_name)
        print("Create: ", seq)
        create_seq(seq, root_path, video_path)
    # create seqmaps folder
    create_seqmaps(branch_path)


def create_trackers_branch(branch_path, root_path):
    """create trackers/ folder all all its children

    Args:
        branch_path ([type]): [description]
        root_path ([type]): [description]
    """
    pred_files = os.listdir(os.path.join(root_path, "pred"))

    for file in pred_files:
        source = os.path.join(root_path, "pred", file)
        dest = os.path.join(branch_path, file)

        if(not os.path.isfile(dest)):
            # create file if it doesn't exist
            f = open(dest, "wt")
        shutil.copy(source, dest)


def create_seqmaps_file(name, seqList):
    """Create seqmaps file contain all seq for 1 dataset type

    Args:
        name ([type]): [description]
        seqList ([type]): [description]
    """
    with open(name, "wt") as f:
        f.write("name\n")
        for seq in seqList:
            f.write(seq + "\n")


def create_seqmaps(path):
    template_names = ["train", "test", "all"]
    seqList = os.listdir(path)
    seqmaps_path = path.replace(BENCHMARK, "seqmaps")

    for name in template_names:
        tmp = os.path.join(seqmaps_path, BENCHMARK + "-{}.txt".format(name))
        create_seqmaps_file(tmp, seqList)


def run(args):
    """Main function to create data

    Args:
        args ([type]): env argument 
    """

    # create a folder tree from template folder
    shutil.copytree(args.template, "data")
    # change template folder to our data folder
    args.save_path = args.save_path.replace("static/data_template", "data")
    # create branch in data/ folder
    gt_branch = args.save_path
    trackers_path = args.save_path.replace("gt", "trackers")
    # MPNTrack: default tracker for mot challenge in trackEval repos
    trackers_branch = os.path.join(
        trackers_path, "ch_yolov5m_deep_sort", "data")

    create_gt_branch(gt_branch, args.root_path, args.video_path)
    create_trackers_branch(trackers_branch, args.root_path)

    os.rename(args.save_path, args.save_path.replace(
        BENCHMARK, BENCHMARK + "-{}".format(args.mode)))
    os.rename(trackers_path, trackers_path.replace(
        BENCHMARK, BENCHMARK + "-{}".format(args.mode)))

    print("Finish!!!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--root_path', '-rp', type=str,
                        help="path to folder contain gt and prediction folder")
    parser.add_argument('--save_path', '-sp', type=str,
                        help="path to save gt seq and file")
    parser.add_argument('--template', '-t', type=str,
                        help="Template folder tree for mot dataset")
    parser.add_argument('--mode', '-m', type=str,
                        help="train|test|all mode with respect to our seqmaps file")
    parser.add_argument('--video_path', '-vp', type=str,
                                        help="Path to folder contain all video that u want to evaluate")
    parser.add_argument('--eval', type=str,
                        help="Evaluate type mtmc|mot", default="mot")
    args = parser.parse_args()

    # python create_data.py -root_path test_data/ --save_path data_template/gt/mot_challenge/Uet_track_vehicle/ --template data_template/ --mode train

    EVAL_MODE = args.eval
    run(args)
