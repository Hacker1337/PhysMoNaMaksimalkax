import cv2
import tkinter as tk
from PIL import Image, ImageTk


def define_place(image, gr_tamp):
    gr_im = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gr_im, gr_tamp, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return max_loc


def printIm(image):
    cv2.namedWindow('amir')
    cv2.imshow('amir', cv2.resize(image, (500, 500)))
    cv2.waitKey(0)
    cv2.destroyAllWindows()

meterspropixel = 1
debug = False

if debug:
    src = "V91019-115103.mp4"
    secproframe = 1
else:
    src = input("Укажите название видео:")
    secproframe = 1/int(input('Введите кол-во кадров в секунду\n'))


#
window = tk.Tk()

k = 4           # How smaller image will be
print('Подождите, видео открывается')
video = cv2.VideoCapture(src)
fn = 0
sec, frame = video.read()
while fn < 60:
    sec, frame = video.read()
    fn += 1
cv2.imwrite('tempframe.jpg', frame)
if not debug:
    cv2.imwrite('preview.jpg', frame)
t = Image.open('tempframe.jpg')
window.geometry(str(t.size[0]//k + 30) + 'x' + str(t.size[1]//k))


def nextFrame():
    global fn, label, frame
    end = fn + 30
    while fn < end:
        sec, frame = video.read()
        fn += 1
    cv2.imwrite('tempframe.jpg', frame)
    if not debug:
        cv2.imwrite('preview.jpg', frame)
    t = Image.open('tempframe.jpg')
    im = ImageTk.PhotoImage(t.resize((t.size[0] // k, t.size[1] // k), Image.ANTIALIAS))

    label = tk.Label(window, image=im)
    label.image = im
    label.place(x=0, y=30)


def touch(e):
    global can, tapped, sq, linealCoords, window, meterspropixel
    if debug:
        print(e.x*k, e.y*k)
    if tapped:
        linealCoords[2] = e.x
        linealCoords[3] = e.y
        ans = input("Выделение прошло успешно, введите расстояние в метрах или 'again', чтобы повторить выделение.\n")
        if ans != 'again':
            meterspropixel = float(ans)/(((linealCoords[0]-linealCoords[2])**2 + (linealCoords[1]-linealCoords[3])**2)**0.5)
            window.destroy()

    else:
        linealCoords[0] = e.x
        linealCoords[1] = e.y

    tapped = not tapped


but = tk.Button(window, command=nextFrame, text='Другой стоп кадр')
but.place(x=0, y=0)
window.bind('<Button-1>', touch)
linealCoords = [0, 0, 0, 1]
tapped = False
im = ImageTk.PhotoImage(t.resize((t.size[0]//k, t.size[1]//k), Image.ANTIALIAS))

label = tk.Label(window, image=im)
label.place(x=0, y=30)
print("Выделите две точки, расстояние между которыми вы знаете и убедитесь, что шарик видно и он на нужном фоне")
window.mainloop()
video.release()
#

input("Теперь откройте файл 'preview.jpg' в каком-нибудь paint-е и вырежте небольшой квадратик с шариком. Затем нажмите enter")
ball = cv2.imread("preview.jpg", 0)

video = cv2.VideoCapture(src)

i = 1

while True:
    sec, frame = video.read()
    if cv2.waitKey(1) & 0xFF == ord('q') or sec == False:
        video.release()
        break
    # if i == 300:
    #     cv2.imwrite("preview.jpg", frame)
    #     break

    if i > 60 or not debug:
        loc = define_place(frame, ball)
        if debug:
            cv2.rectangle(frame, loc, (loc[0] + ball.shape[0], loc[1] + ball.shape[1]), (255, 255, 0), 3)
            printIm(frame)
        print(i*secproframe, loc[0]*meterspropixel, loc[1]*meterspropixel, sep='\t')
    i += 1

