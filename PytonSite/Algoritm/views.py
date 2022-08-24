from PytonSite.settings import DATABASES, BASE_DIR_IMAGE, DIR_IMAGE
from django.shortcuts import render
import face_recognition
import mysql.connector
import numpy as np
import datetime
import cv2
import re

def index(request):
    return render(request, "index.html")
    
def load_send(request):
    return render(request, "load_send.html")
    
def load_find(request):
    return render(request, "load_find.html")
          
def handle_uploaded_file(image, name, cur_dir):
    with open(f'{BASE_DIR_IMAGE}{cur_dir}{name}', 'wb+') as destination:
        for chunk in image.chunks():
            destination.write(chunk)
   
def connectDB():
    return (mysql.connector.connect(host = DATABASES['default']['HOST'],
                                                    user = DATABASES['default']['USER'],
                                                    passwd = DATABASES['default']['PASSWORD'],
                                                    database = DATABASES['default']['NAME']))
                                                    
def get_face_encoding(file, cur_dir):
    encoding = [];
    file_name = "";
    boxes = ()
    if file:
        file_name = "%s" % datetime.datetime.now() + file.name;
        handle_uploaded_file(file, file_name, cur_dir)
        image = cv2.imread(f'{BASE_DIR_IMAGE}{cur_dir}{file_name}')
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        boxes = face_recognition.face_locations(rgb, model='hog')
        if boxes:
            encoding = face_recognition.face_encodings(rgb, boxes)[0]
            info = "Успех"
        else:
            info = "На изображении не было найдена лица"     
    else:
        info = "Изображение не было загружено" 
    return (encoding, info, file_name) 
                
def send(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if len(name) > 0:
            file = request.FILES.get("image", False)
            encoding, info, file_name = get_face_encoding(file, 'send/')
            if (info == "Успех"):
                encoding_string = "%s" % encoding
                face_encoding_string = re.sub('\s+', ' ', encoding_string[1:-1])
                connectionDB = connectDB() 
                cursor = connectionDB.cursor() 
                cursor.execute("CALL ADD_PEOPLE (%s, %s, %s)", (name, face_encoding_string, file_name))
                connectionDB.commit()
                cursor.close()
                connectionDB.close()
                info = "Данные успешно добавлены в базу данных"
        else:
            info = "Имя не было введено"
    else:
        info = "Это не POST запрос"
    data = {"info": info}
    return render(request, "load_send.html", context=data)
    
def find(request):
    name = "Неизвестный"
    if request.method == "POST":
        file = request.FILES.get("image", False)
        unknow_encoding, info, file_name = get_face_encoding(file, 'find/')
        if (info == "Успех"):
            connectionDB = connectDB()
            cursor = connectionDB.cursor() 
            cursor.execute("CALL GET_PEOPLE()")
            info = "Человек не найден в базе данных"
            know_encodings = []
            know_names = []
            for human in cursor.fetchall():
                know_encodings.append(np.fromstring(human[2], dtype=float, sep=' ')) 
                know_names.append(human[1]);
                
            matches = face_recognition.compare_faces(know_encodings, unknow_encoding)
            if True in matches:
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                info = "Человек был найден в базе данных"
                for i in matchedIdxs:
                    name = know_names[i]
                    counts[name] = counts.get(name, 0) + 1
                    name = max(counts, key=counts.get)
                    
                image = cv2.imread(f'{BASE_DIR_IMAGE}/find/{file_name}')
                if image.shape[1] > 1080:
                    width = int(image.shape[1] * 50 / 100) 
                    height = int(image.shape[0] * 50 / 100)
                    output_image = cv2.resize(image, (width, height))
                else:
                    output_image = image
                    
                rgb = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)
                boxes = face_recognition.face_locations(rgb, model='hog')
                y1, x2, y2, x1 = boxes[0]
                cv2.rectangle(output_image, (x1, y1), (x2, y2), (0, 0, 255), 3)
                cv2.putText(output_image, name, (x1, y1 - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (0,), 5)
                cv2.putText(output_image, name, (x1, y1 - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255), 2)
                cv2.imwrite(f'{DIR_IMAGE}{file_name}', output_image)
            cursor.close()
            connectionDB.close()
    else:
        info = "Это не POST запрос"
    data = {"info": info, "name": name, "image_path": f'http://gosuclygi.site/image/{file_name}'}
    return render(request, "load_find.html", context=data)