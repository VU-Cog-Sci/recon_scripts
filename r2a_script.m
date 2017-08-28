% Path to r2a
%this should already be in your path
addpath('/home/shared/software/matlab/r2a/');

% Path to scanner output
%pathToParFiles = ['/Users/martijn/disks/Aeneas_Raw/PRF_7T/data/DE/mri/'];
%pathToParFiles = ['/home/raw_data/2016/visual/whole_brain_MB_pRF/data/Original_data/Original_Raw_Folder/PRF_7T/data/JW/mri'];
%pathToParFiles = ['/home/raw_data/2017/visual/Attention/DE/mri/']
%pathToParFiles = ['/home/raw_data/2017/visual/nPRF/BM/mri/']
%pathToParFiles = ['/home/raw_data/2017/visual/OriColorMapper/JS/mri/']
pathToParFiles = ['/home/raw_data/2017/reward/pearl_7T/scanner_raw/2017_06_28/sub-02/SU_9300/']
%pathToParFiles = ['/home/raw_data/2017/visual/sequence_testing/7T_MB_TE/2017_05_16/FR/mri/']

% if ~exist([options.pathpar 'niftis'],'dir')
%     mkdir(options.pathpar,'niftis')
% end

% Options for the conversion
options.pathpar = pathToParFiles;
options.prefix = '';
options.angulation=1;
options.usefullprefix = 0;
options.rescale=1;
options.subaan = 1;
options.usealtfolder=0;
options.altfolder=[options.pathpar 'niftis/'];
options.outputformat=1; % 1=nifti, 2 = analyze
options.dim=4; % 3=3D nii, 4=4D nii

% Find PAR files and make a list of filenames
files = dir([options.pathpar '*.PAR']);

if isempty(files)
    files = dir([options.pathpar '*.par']);
end

fprintf('Found %d PAR/REC files', length(files));

filelist = {};
for fii = 1:length(files)
    filelist{fii} = files(fii).name;    
end

% Run convert_r2a to do the actual work
outfiles=convert_r2a(filelist, options);

% r2a puts every file in separate folder, so lets clean that up
cd([options.pathpar]);    
mkdir('niftis');

for fii = 1:length(files)

    [~,dname] = fileparts(files(fii).name);
    
    if movefile([dname '/*.nii'],'niftis')
        
        disp(['Moved ' dname])
        system(['rm -R ' dname]);
    end    
    
end

% Gzip for efficiency
system('gzip niftis/*.nii');
    
    
