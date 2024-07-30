import tensorflow as tf
raw_dataset = tf.data.TFRecordDataset("/Users/brunohawkins/Library/CloudStorage/OneDrive-UniversityCollegeLondon/Academic projects/CV in ESS/CV in ESS video/TestSubject101/output/ob_pngs/train/output.tfrecord")

for raw_record in raw_dataset.take(1):
    example = tf.train.Example()
    example.ParseFromString(raw_record.numpy())
    print(example)