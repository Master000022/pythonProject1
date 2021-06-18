import datetime
import os
import sqlite3
import cv2
import face_recognition


conn1 = sqlite3.connect('Main_base.db')  # Создание основной БД
cur1 = conn1.cursor()
cur1.execute("CREATE TABLE IF NOT EXISTS users(userid INT,"
             " name TEXT, status TEXT, date dat);")  # по форме id,name,status,date
conn1.commit()

dat = datetime.datetime.today()  # dat время отсчета с запуска программы
users = [('0', 'Dark', 'out of office', datetime.datetime.today()),
         ('1', 'Alexander', 'out of office', datetime.datetime.today())]
# print(type(dat))
state = ["out of office", 'in office']  # возможные состояния
num_state = 1
user = ['666', 'beast', state[num_state], dat]
conn = sqlite3.connect('base.db')  # Создание вспомогательной БД для последних событий с пользователем
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users(userid INT,"
            " name TEXT, status TEXT, date dat);")
conn.commit()

# cur.execute("DELETE FROM users WHERE name='*';")  # удаление значений из вспомогательной БД
# conn.commit()

# cur.execute("SELECT * FROM users;")  # проверка остаточных значений в вспомогательной БД
# one_result = cur.fetchall()
# print(one_result)



# загрузка изображения через путь
def load(file_path):
    # print(face_recognition.load_image_file(file_path))
    return face_recognition.load_image_file(file_path)


# обработка изображения
def encode(image):
    # print("image:")
    # print(image)
    # print(face_recognition.face_encodings(image))
    if not face_recognition.face_encodings(image, None, 5, "large"):
        return [0]
    return face_recognition.face_encodings(image, None, 5, "large")[0]


path1 = None
known_face_encodings = []  # кодировки изображений
known_face_names = []  # имена к кодировкам
Labels_and_pathes = ['first']
label = str()
# print(known_face_encodings)
# print(known_face_names)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "images")
x = 0
for root, dirs, files in os.walk(image_dir):
    file_count = len(files)
    # print(file_count)
    for file in files:
        # print(file)
        if file.endswith("jpeg") or file.endswith("png") or file.endswith("jpg"):
            path = os.path.join(root, file)
            b = os.path.getsize(path)
            if b > 70000:
                label = os.path.basename(os.path.dirname(path))
                load_1 = load(path)
                Loaded_encoding = encode(load_1)
                if Loaded_encoding[0]:
                    known_face_encodings.append(Loaded_encoding)
                    known_face_names.append(label)
                Labels_and_pathes.append(label)
                Labels_and_pathes.append(root)
                users.append(('0', label, 'out of office', datetime.datetime.today()))

print(known_face_encodings)
print(known_face_names)

# print(Labels_and_pathes)
face_locations = []
face_encodings = []
face_names = []
process_frame = True
cap = cv2.VideoCapture(0)
cur.executemany("INSERT or REPLACE INTO users VALUES(?,?,?,?);", users)
conn.commit()
# cur.execute("SELECT * FROM users;")
# all_results = cur.fetchall()
# # print(all_results)
while True:
    ret, frame = cap.read()
    # print(type(frame))
    process_frame = True
    resized_small_frame = cv2.resize(frame, (0, 0), fx=1, fy=1)  # Making frame 1/4 of original, faster processing
    rgb_small_frame = resized_small_frame[:, :, ::-1]  # Converting BGR to RGB




    if process_frame:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        face_names = []

    for face_encoding in face_encodings:
        dat = datetime.datetime.today()
        # print(face_encoding)
        # print(known_face_encodings)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, 0.6)
        name = "Unknown"
        # print(matches)
        if True in matches:



            # cv2.imwrite("/home/alexander/Desktop/Face/images/Alexander/Avatar3.png", cap.read())
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            face_names.append(name)
            user = [str(x), name, state[num_state], dat]
            cur.execute("SELECT date FROM users WHERE name='{}' ;".format(name))
            all_results = cur.fetchall()
            print(all_results)
            then = all_results[0]
            then1 = datetime.datetime.strptime(then[0], "%Y-%m-%d %H:%M:%S.%f")
            # print(type(then[0]))
            # print(all_results)
            conn.commit()
            # print(state[num_state])
            now = datetime.datetime.now()
            delta = now - then1
            l_name = name
            cur.execute("SELECT status FROM users WHERE name='{}' ;".format(name))
            all_results = cur.fetchall()
            status1 = all_results[0]
            conn.commit()
            direct = Labels_and_pathes.index(name) + 1
            # print(Labels_and_pathes[direct])
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 1
                right *= 1
                bottom *= 1
                left *= 1
                # cv2.rectangle(frame, (left, top), (right, bottom), (255, 255, 255), 2)
                # cv2.rectangle(frame, (left, bottom - 0), (right, bottom), (0, 0, 255), cv2.FILLED)
                # font = cv2.FONT_HERSHEY_DUPLEX
                # cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
                # cv2.namedWindow("Input")

                ROI = frame[top:bottom, left:right]
                cv2.imshow("Input", ROI)

            if (delta.seconds >= 15) and (status1[0] == "out of office"):
                print(delta.seconds)
                ROI = frame[(top-40):(bottom+40), (left-40):(right+40)]
                cv2.imshow("Input", ROI)
                cv2.imwrite(os.path.join(Labels_and_pathes[direct], '%s_%i.png' % (Labels_and_pathes[direct-1], x)), ROI)
                x += 1
                if x==6:
                    x=0
                cur.execute("DELETE FROM users WHERE name='{}' ;".format(name))
                conn.commit()
                num_state = 1
                user.pop(2)
                user.insert(2, state[num_state])  # num_state = 1 = in office
                print(user)

                cur.execute("INSERT INTO users(userid, name, status, date) VALUES(?,?,?,?);", user)
                conn.commit()
                cur1.execute("INSERT INTO users VALUES(?,?,?,?);", user)
                conn1.commit()
                user.clear()
            process_frame = not process_frame

    # cv2.imshow('Face Recognition', frame)
    if cv2.waitKey(33) & 0xFF == ord('0'):
        break
cap.release()
cv2.destroyAllWindows()

cur.execute("DROP TABLE users;")  # удаление значений из вспомогательной БД
conn.commit()
