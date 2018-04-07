The code consists is used to process weather data generated using GenerateDATA.java. The file was used to create a data file of 40M weather entries amounting to 1.5Gb of data. The large file was split into multiple smaller ones using the `split` command. The splitted files were then used for processing.

### The following information is extracted from the weather information generated.

- The hottest day per city [Files: `hot_day_mapper.py` and `hot_day_reducer.py`]
- The coldest day per city [Files: `cold_day_mapper.py` and `cold_day_reducer.py`]
- The highest temperature ever for every city [Files: `hi_temp_mapper.py` and `hi_temp_reducer.py`]
- The lowest temperature ever for every city [Files: `lo_temp_mapper.py` and `lo_temp_reducer.py`]
- The average highest temperature for every city [Files: `avg_hi_mapper.py` and `avg_hi_reducer.py`]
- The average lowest temperature for every city [Files: `avg_lo_mapper.py` and `avg_lo_reducer.py`]
- The hottest city in the dataset [highest recorded temperature] [Files: `hot_city_mapper.py` and `hot_city_reducer.py`]
- The coldest city in the dataset [lowest recorded temperature] [Files: `cold_city_mapper.py` and `cold_city_reducer.py`]

## Usage:
For running the code, we use the Hadoop Streaming feature. The mapper and reducer are python scripts that hadoop uses.
- Input files are placed in HDFS in the `input/` folder
- Output files are placed in HDFS in the `output/` folder
- Replace `mapper.py` and `reducer.py` with the respective `*.py` files

```
$ HADOOP_CLIENT_OPTS="-Xmx4g" bin/hadoop jar share/hadoop/tools/lib/hadoop-streaming-2.9.0.jar \
        -mapper code/mapper.py \
        -reducer code/reducer.py \
        -input input/* \
        -output output \
        -file code/mapper.py \
        -file code/reducer.py
```
Hadoop will manage the data segmentation and the jobs, including managment of the number of map and reduce tasks needed.

## Results:
The output for each of the mentioned tasks are placed in the output folder under a similar naming scheme as the code files
2
