from ultralytics import YOLO

model = YOLO('yolov8n.yaml')
model.train(data='traffic_signs.yaml', epochs=30, batch=64, optimizer='Adam', seed=31)

metrics = model.val()
metrics.box.maps