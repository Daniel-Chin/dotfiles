#!/bin/fish

conda activate ground
python $argv
echo "Python exit code $status. Press Enter to continue..."
read

