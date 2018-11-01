import commands

# Found this here. 
# https://stackoverflow.com/questions/4760215/running-shell-command-from-python-and-capturing-the-output

datasets = ['/TT_TuneCUETP8M2T4_13TeV-powheg-pythia8/RunIISummer16MiniAODv2-PUMoriond17_80X_mcRun2_asymptotic_2016_TrancheIV_v6-v1/MINIAODSIM']

for dataset in datasets:

    dataset_attrs = dataset.split('/')
    dataset_tag = "{0}_{1}".format(dataset_attrs[1],dataset_attrs[2])

    print(dataset_tag)
    #exit()



    query = "--query=\"file dataset={0}\"".format(dataset)
    
    cmds = ['dasgoclient', query, '--format=plain']
    cmds += ['--limit=30']

    #print(cmds)

    cmd = " ".join(cmds)
    #result = commands.getstatusoutput('dasgoclient --help')
    result = commands.getstatusoutput(cmd)
    print(result)

    output = ""

    files = result[1].split('\n')
    for file in files:
        print(file)
        output += file
        output += "\n"

    output_filename = "FILES_TO_PROCESS_{0}.txt".format(dataset_tag)
    output_file = open(output_filename,'w')
    output_file.write(output)

    output_file.close()
