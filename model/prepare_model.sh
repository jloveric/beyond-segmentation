git clone https://github.com/ultralytics/ultralytics.git
cd ultralytics
git checkout v8.3.224
cd ..
patch ultralytics/ultralytics/utils/loss.py loss.py.patch
