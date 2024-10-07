import cv2
import serial
import time
from cvzone.HandTrackingModule import HandDetector

# Set port dan baud rate
comport = 'COM5'  # Ganti dengan port yang sesuai untuk ESP8266
baud_rate = 9600   # Harus sama dengan baud rate di ESP8266

# Inisialisasi koneksi serial
ser = serial.Serial(comport, baud_rate)
time.sleep(2)  # Tunggu untuk inisialisasi koneksi

# Inisialisasi detektor tangan
detector = HandDetector(detectionCon=0.8, maxHands=1)
video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    frame = cv2.flip(frame, 1)

    # Temukan tangan dalam frame
    hands, img = detector.findHands(frame)

    # Tambahkan print untuk memeriksa struktur data hands
    print("Hands detected:", hands)

    if hands:  # Pastikan ada tangan yang terdeteksi
        lmList = hands[0]['lmList']  # Mengakses landmark tangan pertama
        print("Landmark List:", lmList)  # Print landmark list untuk verifikasi

        # Panggil fungsi fingersUp dengan hands[0] secara langsung
        fingerUp = detector.fingersUp(hands[0])  # Menghitung jari yang diangkat
        finger_count = sum(fingerUp)  # Hitung jumlah jari yang diangkat
        print(finger_count)

        # Kirim perintah ke ESP8266 berdasarkan jumlah jari yang diangkat
        if finger_count == 0:
            ser.write(b'0')  # Matikan semua LED
        elif finger_count == 1:
            ser.write(b'1')  # Nyalakan LED 1
        elif finger_count == 2:
            ser.write(b'1')
            ser.write(b'2')  # Nyalakan LED 2
        else:
            ser.write(b'0')  # Matikan semua LED jika lebih dari 2

        # Tampilkan jumlah jari yang diangkat
        cv2.putText(frame, f'Finger count: {finger_count}', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.imshow("frame", frame)
    k = cv2.waitKey(1)
    if k == ord("k"):
        break

video.release()
cv2.destroyAllWindows()
ser.close()  # Tutup koneksi serial
