import os
import subprocess
in_dir = "/home/chris/Documents/SchoolData/convert/"
pdf_files = os.listdir(in_dir)
out_dir = "/home/chris/Documents/SchoolData/done"
for pdf in pdf_files:
	outfile = os.path.join(out_dir,pdf)
	infile = os.path.join(in_dir,pdf)
	crop_cmd = "gs -sDEVICE=pdfwrite -o {} -c '[/CropBox [0 0 595 385] /PAGES pdfmark' -f {}".format(outfile, infile)
	print crop_cmd
	output = subprocess.Popen(crop_cmd, shell = True, stdout = subprocess.PIPE).stdout.read()
			                                   

