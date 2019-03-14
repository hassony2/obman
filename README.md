ObMan dataset
=============

# Download required files


## Download object meshes

- Download object models from ShapeNet
  - Create an account on [shapenet.org](https://www.shapenet.org)
  - Download models from [download page](https://www.shapenet.org/download/shapenetcore)

## Download dataset images and data

- https://filesender.renater.fr/?s=download&token=0c346377-4d7c-d9c9-5c60-f2cf6a93fe65
- unzip test.zip and val.zip to /path/to/obman
- Your dataset structure should look like

```
obman/
  test/
    rgb/
    rgb_obj/
    meta/
    ...
  val/
    rgb/
    rgb_obj/
    meta/
    ...
```

# Download code

`git clone https://github.com/hassony2/obman`

`cd obman`

# Load samples

`python readataset --root /path/to/obman --shapnet_root /path/to/ShapeNetCore.v2 --split test --viz`

Options you might be interested in `--segment` which keeps only the foreground `--mini_factor 0.01` to load only 1% of the data (to speed-up loading)

![image](assets/viz3d.png)
![image](assets/viz2d.png)
