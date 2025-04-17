import os
import glob
import subprocess 

resubmitLine = "queue 1 Folder in DY_2"
condorFolder = 'condor/DY_CR_2023BPix_wp90iso_Tight_HWW'

samples = resubmitLine[len('queue 1 Folder in '):].split(' ')
print(str(samples))

condorFolder = os.path.abspath(condorFolder)

proc = subprocess.Popen('which python3', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = proc.communicate()
out = out.decode("utf-8")
frameworkPath = '/'.join(out.split('\n')[0].split('/')[:-3]) + '/'


for sample in samples:


    fSh  = '#!/bin/bash\n'
    fSh += f'cd {condorFolder}/{sample}\n'
    fSh += f'mkdir tmp\n'
    fSh += f'cd tmp\n'
    fSh += f'cp ../script.py . \n'
    fSh += f'cp ../../run.sh . \n'
    fSh += f'cp {frameworkPath}mkShapesRDF/include/headers.hh . \n'
    fSh += f'cp /afs/cern.ch/user/s/squinto/private/work/mkShapesRDF/mkShapesRDF/shapeAnalysis/runner.py . \n'
    fSh += f'echo "run locally" >../err.txt\n'
    fSh += f'./run.sh {sample} 2>>../err.txt 1>../out.txt\n'
    fSh += f'cd ..; rm -r tmp\n'

    fileName = f'tmp_run_{sample}.sh'

    with open(fileName, 'w') as file:
        file.write(fSh)

    proc = subprocess.Popen(f'chmod +x {fileName}; ./{fileName}; rm {fileName}', shell=True)
    proc.wait()
