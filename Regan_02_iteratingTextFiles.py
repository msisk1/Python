import os
output_dir = "E:\\GISWork_2\\Regan_Conflict\\2016-04-21_worldClimate\\"
only1980Location = output_dir + "soilmoisture_old_1980.csv"
allOthersLocation  = output_dir + "soilmoisture_old.csv"
all_outs_Location = output_dir + "soilmoisture_oldTotal.csv"

only1980 = open(only1980Location, 'r')
allOthers = open(allOthersLocation, 'r')
totalFiles = open (all_outs_Location, 'w')
print os.path.exists(only1980Location)
count = 0


with only1980 as f:
   for each_line in f:
        count += 1
        if (count % 50000) == 0 : #and (used > 0):
            print count
        totalFiles.write(each_line)
        if 'str' in each_line:
            break
print "finished 1980-1-1"
first = True
with allOthers as f:
   for each_line in f:
        count += 1
        if first:
            first = False
            print "toss " + each_line
        else:
            #print "line " + each_line
            totalFiles.write(each_line)
        if (count % 500000) == 0 : #and (used > 0):
           print count

        if 'str' in each_line:
            break

