add_library(ssd_tensorrt MODULE ssd_tensorrt.cpp)
target_link_libraries(ssd_tensorrt PRIVATE nvinfer cublas)
add_library(flattenconcat MODULE flatten_concat.cpp)
target_link_libraries(flattenconcat PRIVATE nvinfer cublas)
