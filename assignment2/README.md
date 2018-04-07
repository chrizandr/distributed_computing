### The following demographics are extracted from the weather information generated.

- The hottest day per city [Files: `hot_day_mapper.py` and `hot_day_reducer.py`]
- The coldest day per city [Files: `cold_day_mapper.py` and `cold_day_reducer.py`]
- The highest temperature ever for every city [Files: `hi_temp_mapper.py` and `hi_temp_reducer.py`]
- The lowest temperature ever for every city [Files: `lo_temp_mapper.py` and `lo_temp_reducer.py`]
- The average highest temperature for every city [Files: `avg_hi_mapper.py` and `avg_hi_reducer.py`]
- The average lowest temperature for every city [Files: `avg_lo_mapper.py` and `avg_lo_reducer.py`]
- The hottest city in the dataset [highest recorded temperature] [Files: `hot_city_mapper.py` and `hot_city_reducer.py`]
- The coldest city in the dataset [lowest recorded temperature] [Files: `cold_city_mapper.py` and `cold_city_reducer.py`]

## Usage:
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

## Results:
The output for each of the demographics are placed in the output folder under a similar naming scheme as the code.
