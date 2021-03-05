#!/usr/bin/env python
# coding: utf-8

# In[1]:


# This version of the MakeAllRegion script looks for DVDVIDEO-VMG in the ISO file, rather than looking for
# the entire contents of VIDEO_TS.IFO; this string always exists at the beginning of this file.
# This means you don't have to pull the VIDEO_TS file out of the archive first!


# In[5]:


import sys

isoImage = sys.argv[1]
region0 = 0x40
regionOffset = 0x23


# In[6]:


# Determine file locations. Region is stored twice, once in the VIDEO_TS.IFO and once in the VIDEO_TS.BUP
# file. The contents of each file is identical, the second is just for backup in case the first can't be read.
with open(isoImage, 'rb') as bigf:
    isoData = bigf.read(1000000)
firstLocation = isoData.find(b"DVDVIDEO-VMG")
secondLocation = isoData.find(b"DVDVIDEO-VMG", firstLocation+12)# 12 is length of "DVDVIDEO-VMG" string
    
print(firstLocation)
print(secondLocation)

if(firstLocation < 0 or secondLocation < 0):
    print("ERROR: Could not find both region locations!")
    quit()


# In[7]:


#Print the existing region bytes (64 = 0x40 = Region 0)
print(isoData[firstLocation + regionOffset])
print(isoData[secondLocation + regionOffset])


# In[17]:


#Write region 0 to the file in both locations
with open(isoImage, 'r+b') as bigf:
    bigf.seek(firstLocation + regionOffset)
    bigf.write(b'\x40')
    bigf.seek(secondLocation + regionOffset)
    bigf.write(b'\x40')


# In[ ]:




