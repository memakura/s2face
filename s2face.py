# s2ext.py
# -*- coding: utf-8 -*-

import asyncio
from aiohttp import web

import cv2
import sys



class S2FACE:
    """ Face detctor class for Scratch 2 extension """
    def __init__(self):
        self.cascPath = sys.argv[1]
        self.faceCascade = cv2.CascadeClassifier(self.cascPath)
        self.video_capture = cv2.VideoCapture(0)
        self.helper_host = '127.0.0.1'
        self.helper_port = 50212
        self.face_x = 0
        self.face_y = 0

    async def run_captureloop(self):
        while True:
            # Capture frame-by-frame
            ret, frame = self.video_capture.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = self.faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            ) #                flags=cv2.cv.CV_HAAR_SCALE_IMAGE


            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            self.face_x = int((x + w/2) * 3 / 4 - 240)
            self.face_y = int(180 - (y + h/2) * 3 / 4)

            # Display the resulting frame
            cv2.imshow('Video', frame)
            await asyncio.sleep(0.033)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        # When everything is done, release the capture
        self.video_capture.release()
        cv2.destroyAllWindows()

    async def handle_poll(self, request):
        """ Handle polling from Scratch """
        text = "face_x " + str(self.face_x) + "\n"
        text += "face_y " + str(self.face_y) + "\n"
        return web.Response(text=text)


    # async def handle_beep(self, request):
    #     """ Handle beep request from Scratch """
    #     print("play beep!")
    #     print("\007")
    #     return web.Response(text="OK")

    # async def handle_setvolume(self, request):
    #     """ Handle set volume request from Scratch """
    #     tmp_volume = int(request.match_info['vol'])
    #     if tmp_volume >= 0 and tmp_volume <= 10:
    #         self.volume = tmp_volume
    #         print("set volume= " + str(self.volume))
    #     else:
    #         print("out of range: " + str(self.volume))
    #     return web.Response(text="OK")

    def main(self):
        """ Main routine """
        loop = asyncio.get_event_loop()
        app = web.Application(loop=loop)
        app.router.add_get('/poll', self.handle_poll)
#        app.router.add_get('/playBeep', self.handle_beep)
#        app.router.add_get('/setVolume/{vol}', self.handle_setvolume)

        scratch_server = loop.create_server(app.make_handler(), self.helper_host, self.helper_port)
        #web.run_app(app, host='127.0.0.1', port=12345)
        cap_loop = loop.create_task(self.run_captureloop())
        try:
            loop.run_until_complete(asyncio.wait({cap_loop, scratch_server}))
            loop.run_forever() # until loop.stop()
        finally:
            loop.close()

if __name__ == '__main__':
    s2face = S2FACE()
    s2face.main()
