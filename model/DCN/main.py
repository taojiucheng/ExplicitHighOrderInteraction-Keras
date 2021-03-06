import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.callbacks import EarlyStopping

from dcn import DCN

if __name__ == '__main__':
    print('Generate fake data...')
    x_dense = np.random.random((1000, 5))
    x_sparse = np.random.randint(0, 3, (1000, 7))
    x = np.concatenate([x_dense, x_sparse], axis=1)
    y = np.random.randint(0, 2, (1000, 1))
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=2020)

    print('Build model...')
    dcn = DCN(feat_dense_num=5,
              feat_sparse_num=7,
              feat_sparse_vocab_sizes=[3] * 7,
              feat_sparse_embedding_sizes=[32] * 7)
    dcn.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    print('Train...')
    early_stopping = EarlyStopping(monitor='val_accuracy', patience=3, mode='max')
    dcn.fit(x_train, y_train,
            batch_size=32,
            epochs=10,
            callbacks=[early_stopping],
            validation_data=(x_test, y_test))

    print('Test...')
    result = dcn.predict(x_test)
