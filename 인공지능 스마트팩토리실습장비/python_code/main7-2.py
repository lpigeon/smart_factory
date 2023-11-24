import cv2
from pyzbar import pyzbar

def detect_qr_code(frame):
    # 이미지를 그레이스케일로 변환
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 이미지에서 QR 코드를 검출
    qrcodes = pyzbar.decode(gray)

    # QR 코드 주위에 사각형 그리기
    for qr in qrcodes:
        (x, y, w, h) = qr.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # QR 코드의 데이터 출력
        qr_data = qr.data.decode("utf-8")
        #qr_type = qr.type
        cv2.putText(frame, qr_data, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    if qrcodes:
        return frame,qr_data
    else:
        return frame,None

# 웹캠 열기
cap = cv2.VideoCapture(0)

while True:
    # 프레임 읽기
    ret, frame = cap.read()

    # QR 코드 검출
    frame,qr_data = detect_qr_code(frame)

    # 화면에 출력
    cv2.imshow("QR Code Detection", frame)
    print("Detected QR Code:", qr_data)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 리소스 해제
cap.release()
cv2.destroyAllWindows()
