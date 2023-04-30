from keras.layers import Conv2D, Dense, MaxPooling2D, Dropout, Flatten, GlobalAveragePooling2D
from keras import Model
import numpy as np
from keras.models import Sequential
from tensorflow.keras import applications
import keras
from keras.preprocessing.image import ImageDataGenerator
from sklearn.model_selection import train_test_split
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from google.colab import drive
drive.mount('/content/drive')


Dataset = pd.read_csv("/content/drive/MyDrive/frames/6K - Sheet1.csv")

Dataset["label"] = Dataset["label"].astype(str)

Dataset["name"] = Dataset["name"].astype(str)

Dataset.head()


fig, ax = plt.subplots(figsize=(10, 4))
sns.countplot(x='label', data=Dataset)
plt.xlabel("Class Label")
plt.ylabel("Number of Samples")
plt.show()

# Splitting Data into Train/Test


Data_train, Data_test = train_test_split(Dataset, test_size=0.2)


datagen = ImageDataGenerator(rescale=1./255)

! unzip drive/MyDrive/frames/frames.zip


dir1 = '/content/frames'

train_gen = datagen.flow_from_dataframe(dataframe=Data_train,
                                        directory=dir1,
                                        batch_size=30,
                                        class_mode="categorical",
                                        x_col="name",
                                        color_mode="rgb",
                                        y_col="label",
                                        target_size=(224, 224))

# Creating Validation Data

valid_gen = datagen.flow_from_dataframe(dataframe=Data_test,
                                        directory=dir1,
                                        batch_size=30,
                                        class_mode="categorical",
                                        x_col="name",
                                        color_mode="rgb",
                                        y_col="label",
                                        target_size=(224, 224))


ResNet_model = keras.applications.ResNet152V2(
    weights='imagenet', include_top=False, input_shape=(224, 224, 3))

# Building Model


for layer in ResNet_model.layers[:-15]:
    layer.trainable = False

x = ResNet_model.output
x = GlobalAveragePooling2D()(x)
x = Flatten()(x)
x = Dense(units=512, activation='relu')(x)
x = Dropout(0.3)(x)
x = Dense(units=512, activation='relu')(x)
x = Dropout(0.3)(x)
output = Dense(units=5, activation='softmax')(x)
model = Model(ResNet_model.input, output)

print(model.summary())

# Setting Loss function, Optimizer and Compling the model

loss = keras.losses.CategoricalCrossentropy()
optimizer = keras.optimizers.Adam(learning_rate=0.0001)
model.compile(optimizer=optimizer, loss=loss, metrics=['accuracy'])

# Compiling the Model

STEP_SIZE_TRAIN = train_gen.n//train_gen.batch_size
STEP_SIZE_VALID = valid_gen.n//valid_gen.batch_size

print(STEP_SIZE_TRAIN)
print(STEP_SIZE_VALID)

transfer_learning_history = model.fit_generator(generator=train_gen,
                                                steps_per_epoch=STEP_SIZE_TRAIN,
                                                validation_data=valid_gen,
                                                validation_steps=STEP_SIZE_VALID,
                                                epochs=3)

# Visualizing accuracy and loss


acc = transfer_learning_history.history['accuracy']
val_acc = transfer_learning_history.history['val_accuracy']

loss = transfer_learning_history.history['loss']
val_loss = transfer_learning_history.history['val_loss']

epochs_range = range(3)

plt.figure(figsize=(20, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()
