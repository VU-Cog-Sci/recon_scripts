% Path to r2av
%this should already be in your path
addpath('/home/shared/software/matlab/r2a/');
%addpath(genpath('/home/shared/software/recon/mp2rage_scripts'));

% Path to scanner output
%pathToParFiles = ['/home/raw_data/2017/visual/nPRF/raw/MV3/mri/']
%pathToParFiles = [ '/home/raw_data/2016/visual/nPRF/sub-012/bk/mri/bids/']
pathToParFiles = ['/home/raw_data/2017/reward/pearl_7T/scanner_raw/2017_07_13/sub-15/su2/mri/']
%pathToParFiles = ['/home/raw_data/2016/visual/whole_brain_MB_pRF/data/sub-016/BK/mri/bids/']

% T1 or not T1
T1 = false;

% Options for the conversion
options.pathpar = pathToParFiles;
options.prefix = '';
options.angulation=0;
options.usefullprefix = 0;
options.rescale=1;
options.subaan = 1;
options.usealtfolder=0;
options.altfolder=[options.pathpar 'niftis/'];
options.outputformat=1; % 1=nifti, 2 = analyze
options.dim=4; % 3=3D nii, 4=4D nii

% Find PAR files and make a list of filenames
files = dir([options.pathpar '*.par']);

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
if ~T1
    system('pigz niftis/*.nii');
% else
% 	mp2rageB();
end
    
    
