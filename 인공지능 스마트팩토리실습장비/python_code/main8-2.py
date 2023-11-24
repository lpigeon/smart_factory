from keras.models import load_model  # Keras를 사용하기 위해 TensorFlow가 필요합니다.
import cv2  # opencv-python을 설치해야 합니다.
import numpy as np

# 과학적 표기를 해제하여 더 명확하게 표시합니다.
np.set_printoptions(suppress=True)

model = load_model(r"C:\converted_keras\keras_model.h5", compile=False)

# 레이블을 로드합니다.
class_names = open(r"C:\converted_keras\labels.txt", "r", encoding="utf-8").readlines()

# 카메라는 컴퓨터의 기본 카메라에 따라 0 또는 1로 설정할 수 있습니다.
camera = cv2.VideoCapture(0)

while True:
    # 웹캠의 이미지를 가져옵니다.
    ret, image = camera.read()

    # 원본 이미지의 크기를 (224-높이, 224-너비) 픽셀로 조정합니다.
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # 이미지를 창에 표시합니다.
    cv2.imshow("Webcam Image", image)

    # 이미지를 numpy 배열로 만들고 모델의 입력 형태로 재구성합니다.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # 이미지 배열을 정규화합니다.
    image = (image / 127.5) - 1

    # 모델을 예측합니다.
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    # 예측과 신뢰도 점수를 출력합니다.
    print("클래스:", class_name[2:], end="")
    print("신뢰도 점수:", str(np.round(confidence_score * 100))[:-2], "%")

    # 키보드 입력을 감지합니다.
    keyboard_input = cv2.waitKey(1)

    # 'q' 키를 누르면 종료합니다.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()