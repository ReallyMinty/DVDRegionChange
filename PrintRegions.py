#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This version of the MakeAllRegion script looks for DVDVIDEO-VMG in the ISO file, rather than looking for
# the entire contents of VIDEO_TS.IFO; this string always exists at the beginning of this file.
# This means you don't have to pull the VIDEO_TS file out of the archive first!


# In[2]:


region0 = 0x40
regionOffset = 0x23


# In[19]:


# Determine file locations. Region is stored twice, once in the VIDEO_TS.IFO and once in the VIDEO_TS.BUP
# file. The contents of each file is identical, the second is just for backup in case the first can't be read.
with open(sys.argv[1], 'rb') as bigf:
    isoData = bigf.read(1000000)
firstLocation = isoData.find(b"DVDVIDEO-VMG")
secondLocation = isoData.find(b"DVDVIDEO-VMG", firstLocation+12)# 12 is length of "DVDVIDEO-VMG" string
    
print(firstLocation)
print(secondLocation)

if(firstLocation < 0 or secondLocation < 0):
    print("ERROR: Could not find both region locations!")
    #quit()


# In[20]:


#Print the existing region bytes (64 = 0x40 = Region 0)
firstRegion = isoData[firstLocation + regionOffset]
secondRegion = isoData[secondLocation + regionOffset]

print(firstRegion)

if(firstRegion != secondRegion):
    print("WARNING: The two Region codes don't match!")


# In[21]:


print("Please note Region 7 is reserved and should NEVER be enabled!")

i=1
bit=1

while(i<9):
    if((firstRegion & bit) == False):
        print(i, end=',')
        if(i == 7):
            print("\nWARNING: Region 7 is set, which is not allowed!")

    i+=1
    bit = bit << 1
    #print(bit)


# In[ ]:




