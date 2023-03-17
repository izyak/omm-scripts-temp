#!/bin/bash
echo "executing omm staking script..."
source /home/ubuntu/omm/bin/activate
cd /home/ubuntu/omm-scripts/omm-analytics/
python omm-staking-analytics.py
deactivate