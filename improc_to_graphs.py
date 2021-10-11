#!/usr/bin/env python
# coding: utf-8

import sys
import cv2
import numpy as np
import skimage
import sklearn
import networkx as nx
import matplotlib.pyplot as plt
import scipy.sparse as spr

from skimage.segmentation import watershed

from sklearn.neighbors import radius_neighbors_graph

nickname=sys.argv[1]

test_im = cv2.imread("output_imgs/%s.tif" % nickname)

test_im *= np.pad(cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(512+256,512+256)),((128,128),(128,128))).reshape(1024,1024,1)

comps = watershed(test_im)[:,:,0]
ncomps = np.max(comps)

element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(6,6))

flat_ims = [(comps==i).astype('int') for i in range(ncomps+1)]

dilate_ims = [0,0]+[spr.csr_matrix(np.sign(cv2.dilate(flat_ims[i].astype('float'),element))) for i in range(2,ncomps+1)]

c_coords = {}
for i in range(2,ncomps+1):
    vv=cv2.findNonZero(flat_ims[i])[:,0,:]
    centroid = np.mean(np.stack(vv),0)
    c_coords[i] = centroid

sc = np.stack(list(c_coords.values()))

bigrad_graph = radius_neighbors_graph(sc,100.0)

zz = np.nonzero(np.triu(bigrad_graph.todense(),k=1))

for ii in range(zz[0].shape[0]):
    im1 = dilate_ims[zz[0][ii]+2]
    im2 = dilate_ims[zz[1][ii]+2]
    rez = im1.multiply(im2).sum()
    bigrad_graph[zz[0][ii],zz[1][ii]] *= rez
    bigrad_graph[zz[1][ii],zz[0][ii]] *= rez

gpr = nx.from_numpy_array(np.pad(np.abs(bigrad_graph.todense()),((2,0),(2,0))))

from scipy.spatial.distance import pdist,squareform

def extract_graph(center_idx):
    gss = gpr.subgraph(
        np.array(list(c_coords.keys()))[np.argsort(np.linalg.norm(sc - c_coords[center_idx],axis=-1))[:64]]
    )
    posidx = np.stack([c_coords[item] for item in gss.nodes()])
    distmat = squareform(pdist(posidx))
    anglemat = squareform(pdist(posidx-np.mean(posidx,axis=0),metric='cosine'))
    for i1,v1 in enumerate(gss.nodes()):
        for i2,v2 in enumerate(gss.nodes()):
            if (v1,v2) in gss.edges() or (v2,v1) in gss.edges():
                gss.edges[v1,v2]['dist'] = distmat[i1,i2]
                gss.edges[v1,v2]['angle'] = anglemat[i1,i2]
    return nx.relabel_nodes(gss, {k:tuple(v) for k,v in c_coords.items()})

def save_graph(gr,filename):
    wmat = nx.to_scipy_sparse_matrix(gr,weight='weight').tocoo()
    dmat = nx.to_scipy_sparse_matrix(gr,weight='dist').tocoo()
    amat = nx.to_scipy_sparse_matrix(gr,weight='angle').tocoo()
    out_ed_array = np.stack([wmat.row,wmat.col,amat.data,dmat.data,wmat.data]).T
    np.savetxt(filename,out_ed_array)
    np.savetxt(filename.replace("_ed.","_ve."),np.array(list(gr.nodes())))

filtered_centers = list(filter(lambda x:np.linalg.norm(c_coords[x] - (512,512))<150,range(2,ncomps+1)))

for i in range(len(filtered_centers)):
    save_graph(extract_graph(filtered_centers[i]),"graphs/%s_%03d_ed.csv" % (nickname,i))




