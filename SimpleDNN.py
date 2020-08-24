from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Import dataset
df = pd.read_csv('reviews.csv', header=0)
df = df.sample(frac=1)
max_len = 200
num_words = 10000
tok = Tokenizer(num_words=num_words)
tok.fit_on_texts(df['Text'])
x_train = tok.texts_to_sequences(df['Text'])
x_train = np.asarray([np.asarray(xi) for xi in x_train])
x_train = pad_sequences(x_train, maxlen=max_len, padding='post')
y_train = df['Score Dist'].values
y_train = df.values[:,2:]
y_train = to_categorical(y_train, 3)
print(x_train)
print(x_train.shape)
print(y_train.shape)

model = Sequential()
model.add(Embedding(num_words, 9, input_length=max_len))
model.add(LSTM(128, return_sequences=True, recurrent_dropout=0.5))
model.add(LSTM(128, return_sequences=True, recurrent_dropout=0.5))
model.add(LSTM(128, recurrent_dropout=0.5))
model.add(Dense(30, activation='relu'))
model.add(Dense(3, activation='softmax'))

opt = RMSprop(learning_rate=0.0002)

model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

history = model.fit(
    x_train, y_train,
    epochs=40,
    batch_size=128,
    validation_split=0.2,
    shuffle=True
)

model.save('MetacriticNet.h5')

plt.plot(history.history['accuracy'],
         label='Доля верных ответов на обучающем наборе')
plt.plot(history.history['val_accuracy'],
         label='Доля верных ответов на проверочном наборе')
plt.xlabel('Эпоха обучения')
plt.ylabel('Доля верных ответов')
plt.legend()
plt.show()

