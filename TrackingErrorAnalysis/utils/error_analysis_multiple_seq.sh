set -e 

output_path="static/test_data" 
pred="${output_path}/pred_tmp" # path to prediction files 
gt="${output_path}/gt_tmp" # path to groundtruth files

rm -rf ${output_path}/pred/*.txt
rm -rf ${output_path}/gt/*.txt

for seq in $pred/NVR-CH02*.txt;
do	
	name=(${seq//// })
	echo ${name[3]}
	gt_tmp=${seq/pred/gt}
	cp $seq "${output_path}/pred"
	cp $gt_tmp "${output_path}/gt"
	
	
	bash create_mot_eval.sh ${name[3]}
	
	mv TrackEval/output/heatmap/idsw_heatmap.jpg TrackEval/output/heatmap/${name[3]}_idsw_heatmap.jpg
	rm -rf ${output_path}/pred/*.txt
	rm -rf ${output_path}/gt/*.txt
done
