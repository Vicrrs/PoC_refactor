# importando as bibliotecas
from pyzbar import pyzbar
import cv2
from imutils import rotate_bound


# Função que carrega o decodificador do pyzbar
def decode(img):
    # decodifica todos os códigos de barras de uma imagem
    decoded_objects = pyzbar.decode(img)
    if not decoded_objects:
        return None, None, None
    for obj in decoded_objects:
        # desenha o código de barras
        print("código de barras detectado:", obj)
        img = draw_barcode(obj, img)
        type_barcode = obj.type
        data_barcode = obj.data.decode('utf-8')

    return img, type_barcode, data_barcode


# Função para desenhar a bbox
def draw_barcode(decoded, img):
    img = cv2.rectangle(img, (decoded.rect.left, decoded.rect.top),
                        (decoded.rect.left + decoded.rect.width,
                         decoded.rect.top + decoded.rect.height),
                        color=(0, 255, 0),
                        thickness=5)
    return img

# Funcao que rotaciona e lê o código de barra
def read_barcode(img):
    img_copy = img.copy()
    img_ = None
    step = 5
    i = 1
    # decodifica detectar códigos de barras e obter a imagem que é desenhada
    while img_ is None and i < 180:
        img_, type_barcode, data_barcode = decode(img_copy)
        img_copy = rotate_bound(img_copy, i)
        i += step
    return img_, type_barcode, data_barcode

# funcao para exibir a imagem na janela
def show_img(img):
    cv2.imshow('Janela', img)
    cv2.waitKey(0)


def cam_decode(frame):
    # decodificando barcode/qrcode
    barcodes = pyzbar.decode(frame)
    for barcode in barcodes:
        x, y, w, h = barcode.rect
        barcode_info = barcode.data.decode('utf-8')
        # desenhando bbox azul como contorno
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, barcode_info, (x + 6, y - 6),
                    font, 0.7, (255, 0, 0), 1)
    return frame


def camera():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    # Laço para mostrar a imagem e fechar a aba
    while ret:
        ret, frame = camera.read()
        frame = cam_decode(frame)
        cv2.imshow('Barcode/QR reader', frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    # Passar o caminho da imagem que deseja testar
    img = cv2.imread(
        "C:\\Users\\rozas\\PycharmProjects\\barcode_and_qrcode_reader\\DataSet\\barcodes\\barcode2\\b5.jpg")

    img_code, type_barcode, data_barcode = read_barcode(img)

    show_img(img_code)

    # camera()
