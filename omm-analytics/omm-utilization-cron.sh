#!/bin/bash
echo "executing utilization script..."
source /home/ubuntu/omm/bin/activate
cd /home/ubuntu/omm-scripts/omm-analytics/
python omm-utilization-rates.py
deactivate