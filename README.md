# iwildcam-2019-fgvc6
Classifying Camera trap images from based on sequence-level decision. First, using our background modeling, we developed a scheme to generate candidate object regions or object proposals in the spatiotemporal domain. Second, we overcome the problem of noisy foregound regions by dentifying the best temporal subset of object proposals after preprocessing. Our preprocessing is the enabling step to provide the DCNN model with more distictive images. Third, we aggregate and fuse the features of these selected object proposals for efficient sequence-level animal species classification. Finally, each frame within a given sequence is labeled with either the sequence-level animal class or empty based on the features of the region proposals of that frame.

# Region proposals
