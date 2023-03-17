#!/bin/bash
echo "executing bOMM script..."
source /home/ubuntu/omm/bin/activate
cd /home/ubuntu/omm-scripts/omm-analytics/
python bomm-analytics.py
deactivate