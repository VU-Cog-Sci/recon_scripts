from __future__ import division
import os, subprocess
import copy, glob, shutil


#base_dir = '/home/raw_data/PRF_7T/data/'
#base_dir = '/home/raw_data/2016/visual/whole_brain_MB_pRF/data/Original_data/Original_Raw_Folder/PRF_7T/data/'
#base_dir = '/home/raw_data/2017/visual/Attention/'
# base_dir = '/home/raw_data/2017/visual/OriColorMapper/'
base_dir = '/home/raw_data/2017/reward/pearl_7T/scanner_raw/2017_06_30/sub-03/'
ref_name = 'ref32rfsp47x47x47'

# raw_dir_name = 'DE_20062016' # 'NA_21062016', 'MB_21062016', 'TK_21062016'
#for raw_dir_name in ['AU_05072016','AV_06072016','BM_06072016','EO_06072016','IV_05072016','JL_06072016']:  #  'MB_21062016', 'TK_21062016']:
for index, raw_dir_name in enumerate(['su_9400','su_9401']):
    pp = raw_dir_name[:2] + str(index+1)

    out_dir = os.path.join(base_dir, pp, 'mri')
    hr_dir = os.path.join(base_dir, pp, 'hr')
    in_dir = os.path.join(base_dir, raw_dir_name)

    try:
        os.makedirs(out_dir)
        os.makedirs(hr_dir)
    except OSError:
        pass

    ########################################################################################
    #### first, we need to back up the raw files to a tar.gz file
    #### we could do that in this script, as below

    # os.chdir(base_dir)
    # op, err = subprocess.Popen('tar -I pigz -cvf %s.tar.gz %s'(raw_dir_name, raw_dir_name), shell=True).communicate()
    # print err
    # print op

    ########################################################################################

    ########################################################################################
    ####  go into raw data directory
    ########################################################################################

    os.chdir(os.path.join(base_dir, raw_dir_name))


    ########################################################################################
    ####  take care of the already par/rec B0 map file
    ####  this is the only file we need that was not multiband
    ########################################################################################

    # b0_par = subprocess.Popen('ls *' + 'b0map' +  '*.par', shell=True, stdout=subprocess.PIPE).communicate()[0].split('\n')[-2]
    # b0_rec = subprocess.Popen('ls *' + 'b0map' +  '*.rec', shell=True, stdout=subprocess.PIPE).communicate()[0].split('\n')[-2]


    b0_par = glob.glob('*b0map*.par')[0]
    b0_rec = glob.glob('*b0map*.rec')[0]


    # retcode = subprocess.call('cp ' + b0_par + ' ' + out_dir, shell=True, bufsize=0)
    # retcode = subprocess.call('cp ' + b0_rec + ' ' + out_dir, shell=True, bufsize=0)

    shutil.copy2(b0_par, out_dir)
    shutil.copy2(b0_rec, out_dir)

    ########################################################################################
    ####  take care of physiology data copy
    ########################################################################################

    # op, err = subprocess.Popen('cp SCANPHYSLOG*.log ../%s/%s/'%(pp, 'hr'), shell=True).communicate()
    os.system('cp SCANPHYSLOG*.log %s' % hr_dir)

    # shutil.copy2(os.path.join(in_dir,'SCANPHYSLOG*.log'), hr_dir)

    # print(err)
    # print(op)


    ########################################################################################
    #### set up what files we would need (assuming max 10 runs per subject per session)
    #### and compile list of raw and lab files for the mapper and topup files
    ########################################################################################


    # raw_files = subprocess.Popen('ls *wip*.raw', shell=True, stdout=subprocess.PIPE).communicate()[0].split('\n')#[0]]# for ms in mapper_ss]
    # lab_files = subprocess.Popen('ls *wip*.lab', shell=True, stdout=subprocess.PIPE).communicate()[0].split('\n')#[0]]# for ms in mapper_ss]

    raw_files = glob.glob('*wip*.raw')
    lab_files = glob.glob('*wip*.lab')

    print(raw_files)

    # raw_files = [rf for rf in raw_files if rf != '']
    # lab_files = [lf for lf in lab_files if lf != '']


    ########################################################################################
    ####  the all-important reference files, 
    ####  take the last of the possible multiple [-2], 
    ####  as only the last one incorporates the shimming.
    ########################################################################################

    # rrf = subprocess.Popen('ls *' + ref_name +  '*.raw', shell=True, stdout=subprocess.PIPE).communicate()[0].split('\n')[-2]
    # rlf = subprocess.Popen('ls *' + ref_name +  '*.lab', shell=True, stdout=subprocess.PIPE).communicate()[0].split('\n')[-2]

    rrf = glob.glob('*%s*.raw'%ref_name)[0]
    rlf = glob.glob('*%s*.lab'%ref_name)[0]


    ########################################################################################
    ####  the command to use, with the standard files added 
    ####  to create a fixed format to be used for each conversion.
    ########################################################################################

    cmd = '/home/shared/software/CReconCL/CReconCL' + ' --reflab REFLAB --refraw REFRAW --raw RAW --lab LAB --out_dir OUT_DIR --log 1'

    cmd = cmd.replace('REFLAB', os.path.join(in_dir, rlf))
    cmd = cmd.replace('REFRAW', os.path.join(in_dir, rrf))
    cmd = cmd.replace('OUT_DIR', out_dir)


    ########################################################################################
    ####  loop across candidate files, filling in the raw and lab files into the cmd string 
    ########################################################################################

    for r, l in zip(raw_files, lab_files):
        this_cmd = copy.copy(cmd)
        this_cmd = this_cmd.replace('RAW', os.path.join(in_dir, r))
        this_cmd = this_cmd.replace('LAB', os.path.join(in_dir, l))
        print(this_cmd)

        op, err = subprocess.Popen(this_cmd, shell=True).communicate()

        print(err)
        print(op)

######################################################################################
######################################################################################
######################################################################################
######################################################################################
# After processing, it's possible that certain programs only read uppercase
# extension par files, so those would be PAR files
# run these in the terminal (bash):

# for file in *.par
# do
#  mv "$file" "${file%.par}.PAR"
# done

# for file in *.rec
# do
#  mv "$file" "${file%.rec}.REC"
# done

######################################################################################
######################################################################################
######################################################################################
######################################################################################




