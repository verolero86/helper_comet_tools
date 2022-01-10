#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


# In[69]:


leaf_outfile='hist_out_102_00.txt'
leaf = pd.read_csv(leaf_outfile,sep='\t',skiprows=3)
print(leaf)


# In[67]:


figsz=20
plt.figure()
leaf.plot(x="bin",use_index=True,y="count",figsize=(figsz,figsz),kind='bar')
plt.xticks([100,200,300,400,500,600,700,800,900,1000])
plt.savefig(leaf_outfile+".png")
plt.xlim([750,1000])
plt.savefig(leaf_outfile+"_zoom.png")


# In[249]:


outfile_prefix="hist_out_102_"
for i in range(24):

    if i<10:
        outfilename=outfile_prefix+"0"
    else:
        outfilename=outfile_prefix
        
    outfilename+=str(i)+".txt"
    print(outfilename)
    leaftmp = pd.read_csv(outfilename,sep='\t',skiprows=3,index_col='bin')
    if i == 0:
        leaves = leaftmp
    else:
        leaves = leaves.join(leaftmp,rsuffix=str(i))


# In[250]:


print(leaves["count23"])


# In[274]:


leaf102 = pd.DataFrame()
leaf102['total_count']=0
for i in range(24):
    if i == 0:
        leaf102['total_count'] = leaves["count"]
    else:
        leaf102['total_count'] = leaf102['total_count'] + leaves["count"+str(i)]
    
print(leaf102)


# In[275]:


figsz=20
plt.figure()
leaf102.plot(y="total_count",figsize=(figsz,figsz),kind='bar')
plt.xticks([100,200,300,400,500,600,700,800,900,1000])
plt.savefig("leaf_102_histogram.png")
plt.xlim([750,1000])
plt.savefig("leaf_102_histogram_zoom.png")


# In[303]:


sum(leaf102['total_count'])


# In[156]:


leaf00=pd.read_csv("hist_out_102_00.txt",sep='\t',skiprows=3)
leaf01=pd.read_csv("hist_out_102_01.txt",sep='\t',skiprows=3)
#print(leaf00)
#print(leaf01)
leaftmp=pd.read_csv("hist_out_102_00.txt",sep='\t',skiprows=3)
full_leaf = leaftmp.set_index('bin').join(leaf01.set_index('bin'),lsuffix='_00',rsuffix='_01')


# In[95]:


print(leaves)


# In[313]:


# module to time processing of the different files
import time


# In[338]:


# Read the leaf element key file and create a dictionary
keyfile = "element_key_102.txt"
start = time.time()
count = 0
keydict = {}
with open(keyfile) as file:
    for line in file:
        #print(line)
        [key,pixstr] = line.split()
        pixpair = pixstr.split('_')
        keydict[key] = pixpair
        count = count + 1
end =  time.time()
print("Execution time in seconds: ",(end-start))
print("Number of lines printed: ",count)
print("Size of keydict dictionary:",len(keydict))


# In[340]:


# Read the clusters file
clusterfile = "clusters_filtered_0.995_out_102.txt"
start = time.time()
clusterdict = {}
count = 0
with open(clusterfile) as file:
    for line in file:
        #print(line)
        clusters = line.split()
        clusterdict[count] = clusters
        count = count + 1
end =  time.time()
print("Execution time in seconds: ",(end-start))
print("Number of lines printed: ",count)
print("Size of clusterdict dictionary:",len(clusterdict))


# In[353]:


len(clusterdict)


# In[355]:


import matplotlib


# In[390]:


rgb_image = np.ones([512, 512, 3])
fig = plt.figure(figsize=(16, 8))
for p in clusterdict[0]:
    x,y = keydict[p]
    #print(f"{p}: {x}, {y}")
    rgb_image[int(x),int(y),:] = [0,0,1]
plt.imshow(rgb_image)
plt.show()


# In[367]:


for c in clusterdict:
    print("Cluster ",c,"->",len(clusterdict[c]))
    
    for p in clusterdict[c]:
        print(f"keydict[{p}] = {keydict[p]}")


# In[425]:


# initialize blank RGB image
rgb_image = np.ones([512, 512, 3])

# initialize blank figure
fig = plt.figure(figsize=(16, 8))

# total number of clusters
num_clusters = len(clusterdict)
num_colors = (int) (np.ceil(num_clusters**(1/3)))
rgb_scale=np.linspace(0,1,num_colors)

# initialize colors for the number of clusters we have
cluster_colors = []
for i in range(num_colors):
    for j in range(num_colors):
        for k in range(num_colors):      
            cluster_colors.append([rgb_scale[i],rgb_scale[j],rgb_scale[k]])

colorid=0
for c in clusterdict:
    print(f"Cluster {c} -> {len(clusterdict[c])} pixels")

    for p in clusterdict[c]:
        x,y = keydict[p]
        #print(f"{p}: {x}, {y}")
        rgb_image[int(x),int(y),:] = cluster_colors[colorid]
    colorid = colorid+1


plt.imshow(rgb_image)
plt.show()
    


# In[ ]:




