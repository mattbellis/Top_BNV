import sys

infilename = sys.argv[1]
infile = open(infilename)

newjob = False
jobs = []

njobs = 0
while(1):
    line =  infile.readline()
    #print(line)

    if line.find('CRAB project directory')>=0:
        jobname = line.split('crab_projects')[1].strip()
        #print(jobname)
        newjob = True
        jobs.append({'jobname':jobname, 'finished':0, 'failed':0, 'idle':0, 'running':0, 'transferring':0, 'nfiles':0})
        njobs += 1

    for status in ['failed','finished','idle','running','transferring']:
        if line.find(status)>=0 and line.find('Warning')<0 and line.find('jobs')<0:
            #print(status)
            #print(line)
            jobstatus = float(line.split('%')[0].split()[-1])
            nfiles = int(line.split('/')[-1].split(')')[0])
            #print(jobstatus)
            #print(nfiles)
            jobs[njobs-1][status] = jobstatus
            jobs[njobs-1]['nfiles'] = nfiles

    if not line:
        break

#print(jobs)
# Why is this last?????
print('{0:75} {1:6s} {2:6s} {3:6s} {4:6s} {5:12s} {6:6s}'.format('jobname', 'nfiles', 'finished', 'failed', 'running', 'transferring', 'idle'))

for job in jobs:
    print('{0:75} {1:6d} {2:-6.1f} {3:-6.1f} {4:-6.1f} {5:-12.1f} {6:-6.1f}'.format(job['jobname'], job['nfiles'], job['finished'], job['failed'], job['running'], job['transferring'], job['idle']))
