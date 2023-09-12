# Flood_mapping
Flood mapping using "snappy" | Sentinel-1

# Description
I used the Python snappy library to detect the water area in a Sentinel-1 image.<br>
Download Sentinel-1 > https://scihub.copernicus.eu

## Installation
- Anaconda : https://www.anaconda.com/products/distribution <br>
- ESA SNAP : https://step.esa.int/main/download/snap-download/ <br>

#### Set up an environment
Use the terminal or an Anaconda Prompt for the following command: 
``` conda env create -f environment.yml ```

#### Configure Snappy
ESA SNAP has finished installing, open SNAP Command-Line Tool, which is installed as part of the SNAP software, and run the following command: 
``` snappy-conf {path_to_snap_env}\python.exe {path_to_snap_env}\Lib\ ```

#### Change the amount of RAM available
Go to the {virtural_env “snap ”directory } > Lib > snappy.
- Open the snappy configuration file called **"snappy.ini"**.
  - Edit the value for the parameter called **"java_max_mem"** and set it to a value that corresponds to about 70–80% of your system's RAM. <br>
``` java_max_mem: 26G ```
- Open the snappy configuration file called **"jpyconfig.py"**.
  - Edit the value for the parameter called **"jvm_maxmem"** and set it to a value that corresponds to about 70–80% of your system's RAM. <br>
``` jvm_maxmem = '26G' ```

#### Change the TileCache Memory
- Go to where your SNAP software is installed. By default is set to C:\Program Files\snap. Inside it, you will find the folder **"etc"** containing the SNAP properties file called **"snap.properties"**. Edit the file and change the parameter called **"snap.jai.tileCacheSize"**. Set this to a value equal to 70–80% of the **java_max_mem value** (megabytes). <br>
``` snap.jai.tileCacheSize = 21504 ```

> NOTE: Changes must be made with your system’s RAM in mind.

### Sentinel-1 image (Raw file)
<img src="https://github.com/WorrapongOngsakul/Flood_mapping/blob/main/image/sentinel-1.png" width=50%>

### Detect the water area (light blue)
<img src="https://github.com/WorrapongOngsakul/Flood_mapping/blob/main/image/snappy-water.png" width=50%>
