#!/bin/bash
echo "executing reserve script..."
source /home/ubuntu/omm/bin/activate
cd /home/ubuntu/omm-scripts/omm-analytics/
python omm-reserves-analytics.py
deactivate