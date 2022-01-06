import subprocess
from sample_definitions import samples

# Use subrocess.run for python>3.5
# Use subrocess.call for python<3.5
process = subprocess.Popen(['dasgoclient', '--help'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True).communicate()

print("here")
print(process)
print("\n")
for p in process:
    print(p)
    print("\n")

print("\n---------------------\n")

for s in samples['MC'].keys():
    if s in ['2016', '2017', '2018']:
        continue 

    print(s,samples['MC'][s])
    cmd = ['dasgoclient', '--help']
    process = subprocess.Popen(['dasgoclient', '--help'],stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True).communicate()

