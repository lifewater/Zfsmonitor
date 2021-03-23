import os
import subprocess


class ZFSMon:
    def __init__(self):
        self.pools = list(self.getPools())
        print ("Pools: " + ' '.join(self.pools))
        
    def getPools (self):
        
        output = subprocess.check_output(['zpool list -Ho name'], shell=True)
        raw = output.decode().split('\n') # This contains an extraneous blank string element
        return filter(None, raw) # This removes that blank element
        
    def getPoolStatus(self, poolname):
        cmd="zpool status -x {}".format(poolname)
        output = subprocess.check_output(cmd, shell=True).strip()
        
        success_line = "pool \'{}\' is healthy".format(poolname)

        if output.decode() == success_line :
            return True
         
        else:
            return False
        
        


def main():
    Z = ZFSMon()
    for pool in Z.pools:
        if (Z.getPoolStatus(pool)):
            print ("{}: GOOD".format(pool))
        else:
            print ("{}: FAIL".format(pool))

if __name__ == "__main__":
    main()