set -e

name_data_folder_after_eval=$1 # name of save folder
video_path=$2 # path to folder contain all you .mp4 files
options=$3 # whether or not doing error analysis
eval_type=$4 # mot or mtmc
benchmark_name=$5 # save name in benchmarks/ folder

remove_folder () {
    if [ -d $1 ]
    then 
        echo "Remove folder ${1}"
        rm -rf $1
    else 
        echo "${1} not exists"
    fi
}

# remove data folder
remove_folder "./data/"
remove_folder "./TrackEval/data/"
# remove data template
remove_folder "./static/data_template/"
remove_folder "./data_template/"

# create data_template folder tree and move to static folder
bash utils/create_folder_tree.sh
mv data_template/ static/

# create MOT format to evaluate 
python create_data.py --root_path static/test_data/ \
                     --save_path static/data_template/gt/mot_challenge/MOT16 \
                     --template static/data_template/ \
                     --video_path $video_path \
                     --mode test \
                     --eval $eval_type                                                  

# move to TrackEval to evaluate and error analysis                                                                            
mv ./data ./TrackEval                                                                                 
cd TrackEval  

# del all scene evaluate before
rm -rf benchmarks/*
                                                                                                   
bash eval.sh $options

if [ $# -eq 5 ]                                            
then                                                       
   echo "Rename and mv to benchmarks folder"               
   mv "data/"  ${name_data_folder_after_eval}
   if [ ! -d "benchmarks" ]; then
        mkdir benchmarks
   fi                    
   mv ${name_data_folder_after_eval}  "benchmarks/"      
else                                                       
   echo "Not rename and mv data folder to benchmark folder"
fi                                                         

# back to main directory
cd ..

save_benchmark_path="static/benchmarks/${benchmark_name}"
if [ ! -d "$save_benchmark_path" ]; then
  mkdir $save_benchmark_path
fi
# get MOT benchmark results and export to csv files save in static/benchmarks folder
python utils/get_benchmarks.py --path TrackEval/data/trackers/mot_challenge/MOT16-test/ch_yolov5m_deep_sort/pedestrian_detailed.csv --save_path $save_benchmark_path
