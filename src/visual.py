"""Chapter 3 app #2: original NumPy Bag-of-Visual-Words pipeline.
UCI Optdigits 8x8 normalized images -> 2x2 patch descriptors -> k-means
codebook -> each image a SET of visual-word IDs -> own Eclat.
"""
from pathlib import Path
import numpy as np
from .algorithm.eclat import mine


def load_optdigits(path, limit=None):
    raw=np.loadtxt(path,delimiter=',',dtype=np.float64,max_rows=limit)
    if raw.ndim==1:raw=raw[None,:]
    if raw.shape[1]!=65:raise ValueError('Expected 64 pixels + 1 digit label')
    return raw[:,:64].reshape(-1,8,8)/16.0,raw[:,64].astype(int)


def patch_descriptors(images,patch=2):
    """Non-overlapping intensity patches; 8x8 optdigits only."""
    if images.ndim!=3 or images.shape[1:]!=(8,8):raise ValueError('Expected N x 8 x 8')
    if 8%patch:raise ValueError('Patch size must divide 8')
    return images.reshape(-1,8//patch,patch,8//patch,patch).transpose(0,1,3,2,4).reshape(-1,patch*patch)


def numpy_kmeans(samples,k=12,seed=2026,max_iter=35):
    """Independent Lloyd iterations; no sklearn/hidden FIM library."""
    samples=np.asarray(samples,dtype=np.float64)
    if k<1 or k>len(samples):raise ValueError('Bad k')
    rng=np.random.default_rng(seed)
    centers=samples[rng.choice(len(samples),size=k,replace=False)].copy()
    for _ in range(max_iter):
        distances=((samples[:,None,:]-centers[None,:,:])**2).sum(axis=2)
        ids=np.argmin(distances,axis=1)
        new=centers.copy()
        for j in range(k):
            members=samples[ids==j]
            if len(members):new[j]=members.mean(axis=0)
        if np.allclose(centers,new,atol=1e-8):break
        centers=new
    return centers


def encode_visual_transactions(images,centers,patch=2):
    descriptors=patch_descriptors(images,patch=patch)
    distances=((descriptors[:,None,:]-centers[None,:,:])**2).sum(axis=2)
    words=np.argmin(distances,axis=1).reshape(len(images),-1)
    return [sorted(set(int(w) for w in row)) for row in words]


def mine_visual_patterns(images,k_words=12,minsup=0.40,seed=2026,max_results=50000):
    patches=patch_descriptors(images)
    # codebook is trained solely on dataset images, without labels
    codebook=numpy_kmeans(patches,k=k_words,seed=seed)
    transactions=encode_visual_transactions(images,codebook)
    result=mine(transactions,minsup,'bitset',max_results=max_results)
    return result,transactions,codebook
