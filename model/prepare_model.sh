git clone https://github.com/ultralytics/ultralytics.git
cd ultralytics
git checkout v8.3.224
cd ..
cp ultralytics/ultralytics/utils/loss.py ultralytics/ultralytics/utils/loss_baseline.py
cp ultralytics/ultralytics/utils/loss.py ultralytics/ultralytics/utils/loss_align.py
patch ultralytics/ultralytics/utils/loss_align.py loss.py.patch
