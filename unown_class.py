import math
from PIL import Image  #Pillow
from tensorflow.keras.preprocessing.image import img_to_array #tensorflow
from tensorflow.keras.models import model_from_json

def Classification(img_name):
  str = [chr(i) for i in range(97, 97+26)]
  str.insert(0, '!')
  str.insert(1, '?')

  img = Image.open(img_name)
  width, height = img.size

  img = img.convert('RGB')
  if width != 50 or height != 50 :
    if width == height:
      tmp = img.resize((50, 50))
    else:
      if width < height:
        side = height
        x = math.floor((height - width) / 2)
        y = 0
      else:
        side = width
        x = 0
        y = math.floor((width - height) / 2)
      tmp = Image.new('RGB', (side, side), 'white')
      tmp.paste(img, (x, y))
      tmp = tmp.resize((50, 50))
      print('resize complete')
  else:
      tmp = img

  array_img = img_to_array(tmp).reshape(1, 50, 50, 3).astype('float32') / 255.0

  model = model_from_json(open('./cnn_model/unown_model.json').read())
  model.load_weights('./cnn_model/unown_model_weights.hdf5')

  pred = model.predict(array_img, batch_size=1, verbose=1)
  max_str = pred.argmax() #ndarrayの最大値のインデックス取得
  prob = pred.tolist()
  prob = [round(prob[0][i]* 100, 1) for i in range(len(prob[0]))]

  n = 0
  alp_max = ""
  rate_max = 0  

  for chra in enumerate(str):
    if rate_max < prob[n]:
      alp_max = chra[1]
      rate_max = prob[n]
    n += 1
  
  return alp_max