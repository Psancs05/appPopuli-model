import tensorflow as tf
from tensorflow.keras.preprocessing.image import img_to_array

import os, sys

PLAGAS = [
    "Archips xylosteana",
    "Cerura iberica",
    "Chrysomela populi",
    "Cossus cossus",
    "Crepidodera spp",
    "Cryptorhynchus lapathi",
    "Cytospora chrysosperma",
    "Dothichiza populea",
    "Gypsonoma aceriana",
    "Laothoe populi",
    "Lepidosaphes ulmi",
    "Leucoma salicis",
    "Lonsdalea quercina subsp populi",
    "Marssonina brunnea",
    "Melampsora spp",
    "Melanophila picta",
    "Paranthrene tabaniformis",
    "Pemphigus spp",
    "Phloemyzus passerinii",
    "Phratora laticolis",
    "SANO",
    "Saperda carcharias",
    "Saperda populnea",
    "Sesia apiformis",
    "Taphrina populnea (Taphrina aurea)",
    "Trypophloeus spp",
    "Venturia populina",
    "Xanthomonas populi",
]

PATH_MODEL = os.path.join('./','data', 'models', 'modelo.h5')

def loadModel(path_model):
    # load the model in cpu
    with tf.device('/cpu:0'):
        model = tf.keras.models.load_model(path_model)

    return  model


def resizeImages(img):
    img = img.resize((224, 224))
    img = img_to_array(img)
    img = img.astype('float32') / 255.0
    return tf.expand_dims(img, axis=0)


def main(path_image, path_model=PATH_MODEL):
    # Resize las dimensiones de la iamgen
    input_data   = resizeImages(path_image)

    # Realiza las predicciones del modelo
    # print(loaded_model.predict(input_data))
    logits = loaded_model.predict(input_data)
    class_idx = tf.argmax(logits, axis=1).numpy()[0]
    class_name = PLAGAS[class_idx]
    return class_name


loaded_model = loadModel(os.path.join('./','data', 'models', 'modelo.h5'))

if __name__ == '__main__' :

    # argv[1] -> path de la imagen
    # argv[2] -> path del modelo 

    if len(sys.argv) == 2:
        print(main(sys.argv[1]))
    elif len(sys.argv) == 3:
        print(main(sys.argv[1], sys.argv[2]))
    else:
        # main(os.path.join('data', 'ejemplo.jpg'))
        print('El numero de parametros es incorrecto (1 o 2)')

    