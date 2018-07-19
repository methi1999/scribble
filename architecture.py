from keras.models import Sequential,save_model
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Activation, Dropout, Flatten, Dense,BatchNormalization
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img
import Augmentor

classes=26

pool_size = (2, 2) # size of pooling area for max pooling
kernel_size = (5, 5) # convolution kernel size
input_shape=(28,28,1) # size of images

nb_filters = 32 # number of convolutional filters to use
pool_size = (2, 2) # size of pooling area for max pooling
kernel_size = (3, 3) # convolution kernel size
activation='relu' # non-linearity

model = Sequential()

# define the first set of CONV => ACTIVATION => POOL layers
model.add(Conv2D(20, 5, padding="same",input_shape=input_shape))
model.add(Activation(activation))
model.add(BatchNormalization()) # for training purposes
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

# define the second set of CONV => ACTIVATION => POOL layers
model.add(Conv2D(50, 5, padding="same"))
model.add(Activation(activation))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 2), strides=(2, 2)))

# define the first FC => ACTIVATION layers
model.add(Flatten())
model.add(Dense(500))
model.add(Activation(activation))
model.add(BatchNormalization())

# define the second FC layer
model.add(Dense(classes))

# lastly, define the soft-max classifier
model.add(Activation("softmax"))

model.compile(loss='categorical_crossentropy', optimizer='adadelta', metrics=['accuracy'])
model.summary()

# Scale pixel values to range (0,1)
train_datagen = ImageDataGenerator(rescale=1./255)

# Scale pixel values to range (0,1)
test_datagen = ImageDataGenerator(rescale=1./255)

# this is a generator that will read pictures found in
# subfolers of 'Train', and indefinitely generate
# batches of augmented image data

batch_size = 500

train_generator = train_datagen.flow_from_directory(
        '../Letters/Train/output',  # this is the target directory
        target_size=(28,28),  # all images will be resized to 28x28
        batch_size=batch_size,
        class_mode='categorical',
        color_mode='grayscale' # Since we are considering only B&W images
        )

# this is a similar generator, for validation data
validation_generator = test_datagen.flow_from_directory(
        directory='../Letters/Val2',
        target_size=(28,28),
        class_mode='categorical',
        color_mode='grayscale',
        batch_size=78
        )

model.fit_generator(
        train_generator,
        # steps_per_epoch=5000 // batch_size,
        steps_per_epoch=260,
        epochs=10,
        validation_data=validation_generator,
        validation_steps=10
        )
# """

# p = Augmentor.Pipeline("Letters")
# p.random_distortion(probability=0.9, grid_width=4, grid_height=4, magnitude=8)
# p.rotate(probability=0.3, max_left_rotation=5, max_right_rotation=5)
# augmentGen = p.keras_generator(batch_size=batch_size)
# model.fit_generator(augmentGen, steps_per_epoch=len(p.augmentor_images)/batch_size, epochs=5, verbose=1)

model_yaml = model.to_yaml()
with open("lenet.yaml", "w") as yaml_file:
    yaml_file.write(model_yaml)
save_model(model, 'lenet.h5')