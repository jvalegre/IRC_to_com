#!/usr/bin/python
from __future__ import print_function

#Python Libraries
import os.path, sys
from glob import glob
from decimal import Decimal
from optparse import OptionParser

point_number = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','za','zb','zc','zd','ze','zf','zg','zh','zi','zj','zk','zl','zm','zn','zo','zp','zq','zr','zs','zt','zu','zv','zw','zx','zy','zz','zza','zzb','zzc','zzd','zze','zzf','zzg','zzh','zzi','zzj','zzk','zzl','zzm','zzn','zzo','zzp','zzq','zzr','zzs','zzt','zzu','zzv','zzw','zzx','zzy','zzz','zzza','zzzb','zzzc','zzzd','zzze','zzzf','zzzg','zzzh','zzzi','zzzj','zzzk','zzzl','zzzm','zzzn','zzzo','zzzp','zzzq','zzzr','zzzs','zzzt','zzzu','zzzv','zzzw','zzzx','zzzy','zzzz']

#Read molecule data from an input file
class getoutData:
    def __init__(self, file):
        if not os.path.exists(file):
            print(("\nFATAL ERROR: Input file [ %s ] does not exist"%file))

        def getCHARGE(self, inlines):
            self.CHARGE = []
            self.MULT = []
            for i in range(0,len(inlines)):
                if inlines[i].find("Charge ") > -1 and inlines[i].find("Multiplicity ") > -1:
                        self.CHARGE = inlines[i].split()[2]
                        self.MULT = inlines[i].split()[5]

        def getATOMTYPES(self, inlines):
            self.ATOMTYPES = []
            for i in range(0,len(inlines)):
                if inlines[i].find("Charge ") > -1 and inlines[i].find("Multiplicity ") > -1:
                    start = i+1
                    break
            for i in range(start,len(inlines)):
                if len(inlines[i].split()) ==0:
                    break
                else:
                    self.ATOMTYPES.append(inlines[i].split()[0])

        def getCARTESIANS(self, inlines):
            self.CARTESIANS = []
            self.IRC_number,self.IRC_path,self.IRC_direct,self.IRC_number_list,self.start,stop = 0,0,[],[],[],[]
            for i in range(0,len(inlines)):
                if inlines[i].find("Point Number:") > -1 and inlines[i].find("Path Number:") > -1:
                    self.IRC_number = int(inlines[i].split()[2])
                    self.IRC_path = int(inlines[i].split()[5])
                    if self.IRC_number == 0:
                        self.IRC_direct.append('TS')
                    if self.IRC_number != 0 and self.IRC_path == 1:
                        self.IRC_direct.append('forw')
                    if self.IRC_number != 0 and self.IRC_path == 2:
                        self.IRC_direct.append('rev')
                    self.IRC_number_list.append(self.IRC_number)
                    stop.append(i)
            a = 0
            for i in range(0,len(inlines)):
                if a <= len(stop)-1:
                    if inlines[i].find("Input orientation") > -1 and i <= stop[a]:
                        start_indiv = i+5
                    if i == stop[a]:
                        a = a+1
                        self.start.append(start_indiv)
            for number in self.start:
                self.indiv_CARTESIANS = []
                for i in range(number,len(inlines)):
                    if inlines[i].find("----") > -1:
                        break
                    elif len(inlines[i].split()) == 6:
                        self.indiv_CARTESIANS.append([float(inlines[i].split()[3]), float(inlines[i].split()[4]), float(inlines[i].split()[5])])
                self.CARTESIANS.append(self.indiv_CARTESIANS)
            self.IRC_files = []
            for i in range(len(self.IRC_number_list)):
                if self.IRC_number_list[i] == 0:
                    self.IRC_files.append(file.split('.')[0]+'_'+options.append+'_'+str(self.IRC_direct[i])+'.com')
                else:
                    self.IRC_files.append(file.split('.')[0]+'_'+options.append+'_'+self.IRC_direct[i]+'_'+point_number[self.IRC_number_list[i]-1]+'.com')
        infile = open(file,"r")
        inlines = infile.readlines()
        getCHARGE(self, inlines)
        getATOMTYPES(self, inlines)
        getCARTESIANS(self, inlines)

class writeGinput:
    def __init__(self, file, MolSpec, args):
        for point in range(len(MolSpec.IRC_files)):
            f = open(MolSpec.IRC_files[point],"w")
            print("   ", file, '' ">>", MolSpec.IRC_files[point])
            f.write("%chk="+MolSpec.IRC_files[point].split('.')[0]+".chk\n")
            f.write("%mem="+options.mem+"\n")
            f.write("%nprocshared="+str(options.nproc)+"\n")
            f.write("# "+options.route+"\n\n")
            f.write(MolSpec.IRC_files[point]+"\n\n")
            f.write(str(MolSpec.CHARGE)+" "+str(MolSpec.MULT)+"\n")
            for i in range(0,len(MolSpec.ATOMTYPES)):
                f.write(MolSpec.ATOMTYPES[i])
                for j in range(0,3):
                    f.write("  "+str(Decimal(str((MolSpec.CARTESIANS[point][i][j])))))
                f.write("\n")
            f.write("\n")
            if options.gen != 'False':
                f.write(options.gen+"\n")
                f.write("\n")

if __name__ == "__main__":
    parser = OptionParser(usage="Usage: %prog [options] <input1>.log <input2>.log ...")
    parser.add_option('--append', action="store", default="new", help='Append text to create new filenames')
    parser.add_option('--route', action="store", default="", help='Route command line without #')
    parser.add_option('--nproc', action="store", default=24, help='Number of processors for calculations')
    parser.add_option('--mem', action="store", default='96GB',help='Memory for calculations')
    parser.add_option('--gen', action="store", default='False',help='For gen or genecp text at the end of the file (use "TEXT")')

    (options, args) = parser.parse_args()

    # Get the filenames from the command line prompt
    files = []
    if len(sys.argv) > 1:
        for elem in sys.argv[1:]:
            try:
                if os.path.splitext(elem)[1] in [".out", ".log"]:
                    for file in glob(elem): files.append(file)
            except IndexError: pass
    else:
        print("\nNo files were found.\n")
        sys.exit()

    # Takes arguments: (1) file(s) (2) new job parameters
    for file in files:
        MolSpec = getoutData(file)
        writeGinput(file, MolSpec, options)
