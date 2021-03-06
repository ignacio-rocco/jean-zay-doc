# all taken from https://www.tensorflow.org/guide/keras/functional
import click


@click.command()
@click.option(
    'cuda_visible_devices',
    '-gpus',
    default=None,
    help='The GPUs you want visible for this task, comma separated. Defaults to all GPUs visible',
)
@click.option(
    'save',
    '-s',
    '--save',
    is_flag=True,
    help='Whether you want to save the model or not',
)
def train_dense_model_click(cuda_visible_devices, save):
    return train_dense_model(cuda_visible_devices, save, batch_size=64)


def train_dense_model(cuda_visible_devices, save, batch_size):
    # limit imports oustide the call to the function, in order to launch quickly
    # when using dask
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers

    if cuda_visible_devices is not None:
        import os
        os.environ['CUDA_VISIBLE_DEVICES'] = cuda_visible_devices
    # model building
    tf.keras.backend.clear_session()  # For easy reset of notebook state.

    inputs = keras.Input(shape=(784,), name='img')
    x = layers.Dense(64, activation='relu')(inputs)
    x = layers.Dense(64, activation='relu')(x)
    outputs = layers.Dense(10)(x)

    model = keras.Model(inputs=inputs, outputs=outputs, name='mnist_model')

    # training and inference
    # network is not reachable, so we use random data
    x_train = tf.random.normal((60000, 784), dtype='float32')
    x_test = tf.random.normal((10000, 784), dtype='float32')
    y_train = tf.random.uniform((60000,), minval=0, maxval=10, dtype='int32')
    y_test = tf.random.uniform((10000,), minval=0, maxval=10, dtype='int32')


    model.compile(loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  optimizer=keras.optimizers.RMSprop(),
                  metrics=['accuracy'])
    history = model.fit(x_train, y_train,
                        batch_size=batch_size,
                        epochs=5,
                        validation_split=0.2)
    test_scores = model.evaluate(x_test, y_test, verbose=2)
    print('Test loss:', test_scores[0])
    print('Test accuracy:', test_scores[1])

    # saving
    if save:
        model.save(os.environ['SCRATCH'])
    return True

if __name__ == '__main__':
    train_dense_model_click()
