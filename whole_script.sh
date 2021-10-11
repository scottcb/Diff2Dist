python gen_sim_files.py > all_file_list.txt
~/bin/parallel -j 24 -C " " "../bin/simulator -vtk_output modeloutputs/s{1}_s{2}_s{3}_s{4}_r{5} modelfiles/s{1}_s{2}_s{3}_s{4}.model meristem.init solver.rk5" :::: all_file_list.txt
~/bin/parallel -j 24 -C " " "python mesh_to_plot.py s{1}_s{2}_s{3}_s{4}_r{5} s{1}_s{2}_s{3}_s{4}_r{5}" :::: all_file_list.txt
~/bin/parallel -j 12 -C " " "python improc_to_graphs.py synth/s{1}_s{2}_s{3}_s{4}_r{5}" :::: all_file_list.txt
~/bin/parallel -j 8 -C " " "python improc_to_graphs.py {1}" :::: bio_filenames.txt
ls -1 graphs/*/*_ed.csv | sed s=graphs/==g | sed s=_ed.csv==g > morpho_filenames.txt 
