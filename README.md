# recon_scripts


Do all editing and git interaction on the lab laptop, not the user account on the server because github integration is set up only for the laptop. 

## MB_PRF_convert.py

To set up a new subject's conversion, edit this file. Change the subject ID: sub-X and the subfolders that recon should pass through, something like ['su_9400','su_9401'].

After saving this file, do

```git commit -am 'updated MB_PRF_convert.py for subject sub-X'```

to commit the changes with this message. Then, type 


```git push```

to upload to github.