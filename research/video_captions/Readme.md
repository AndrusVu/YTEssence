# Video captions module (In testing WIP)

### Links
___

[Souce repo Video prediction](https://github.com/MDSKUL/MasterProject)

[Souce repo Howto100m](https://github.com/antoine77340/howto100m)

[Souce repo VideoBert](https://github.com/ammesatyajit/VideoBERT)

[Souce repo UniVl model](https://github.com/microsoft/UniVL)

[Source dataset](https://www.di.ens.fr/willow/research/howto100m/)


### Usage task commands
___

```
conda create -n video-bert python=3.9
conda activate video-bert

git clone git@github.com:ammesatyajit/VideoBERT.git

pip install -r requirements
pip install --upgrade tensorflow_hub

conda install -c anaconda tensorflow
conda install -c anaconda keras

conda install -c pytorch torchvision
```

If case of conflicts, delete caffe dlls from path lib

### Feature extraction with I3D model

```
$FILE_LIST_PATH = ".\data\video_filepaths.txt"
$ROOT_VIDEO_PATH = ".\data\raw_videos"
$FEATURES_SAVE_PATH = ".\data\features"
$IMGS_SAVE_PATH = ".\data\images"


python .\VideoBERT\I3D\batch_extract.py `
-f $FILE_LIST_PATH `
-r $ROOT_VIDEO_PATH `
-s $FEATURES_SAVE_PATH `
-i $IMGS_SAVE_PATH
```

### Hierarchical Minibatch K-means

```
$ROOT_FEATURE_PATH = ".\data\features"
$FEATURES_PREFIX = "features"
$BATCH_SIZE = 2048
$SAVE_DIR = ".\data\kmeans_vectors"
$CENTROID_DIR = ".\data\centroids"

python .\VideoBERT\I3D\minibatch_hkmeans.py `
-r $ROOT_FEATURE_PATH `
-p $FEATURES_PREFIX `
-b $BATCH_SIZE `
-s $SAVE_DIR `
-c $CENTROID_DIR
```

### Centroid to images

```
$ROOT_FEATURES = "./data/features"
$ROOT_IMGS = "./data/images"
$CENTROID_FILE = "./data/centroids_prepared/centroids.npy"
$SAVE_FILE = "./data/images_dict/images_dict.json"

python .\VideoBERT\data\centroid_to_img.py `
-f $ROOT_FEATURES `
-i $ROOT_IMGS `
-c $CENTROID_FILE `
-s $SAVE_FILE
```

### Label data

```
$ROOT_FEATURES = "./data/features"
$CENTROID_FILE = "./data/centroids_prepared/centroids.npy"
$SAVE_FILE = "./data/labelled_data/labelled_data.json"

python ./VideoBERT/data/label_data.py `
-f $ROOT_FEATURES `
-c $CENTROID_FILE `
-s $SAVE_FILE
```

...
In testing
...