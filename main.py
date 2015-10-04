#!/usr/bin/python
import filey

## File Writer Testing
filey.make_path("data/experiment/cell")

# Test list for file_writer.
hoopla = ["david", "dalpiaz", "is", "my", "advisor"]

filey.write_to_file("fuck/my/shit", "sherry.txt", hoopla)
