#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
 s2face.py
"""

import asyncio
from aiohttp import web

import sys
import cv2

class S2FACE:
    """ Face detctor class for Scratch 2 extension """

    def __init__(self):
        self.casc_dir = 'haarcascades/'
        self.casc_file = [
            "dummy",
            "haarcascade_frontalface_default.xml",
            "haarcascade_smile.xml",
            "haarcascade_upperbody.xml",
            "haarcascade_eye.xml"
        ]

        self.face_cascade = cv2.CascadeClassifier(self.casc_dir + self.casc_file[1])
        self.video_capture = cv2.VideoCapture(0)
        self.helper_host = '127.0.0.1'
        self.helper_port = 50212

        self.face_exist = False
        self.face_x = 0
        self.face_y = 0
        self.face_width = 0
        # self.face_height = 0
        self.ratio = 0

        width = self.video_capture.get(3)
        #height = self.video_capture.get(4)
        self.s2_xmax = 240
        self.s2_ymax = 180
        self.s2cv_ratio = self.s2_xmax*2 / width

    async def run_captureloop(self):
        """ Video capture loop """
        while True:
            # Capture frame-by-frame
            ret, frame = self.video_capture.read()

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )

            if len(faces)==0:
                self.face_exist = False
            else:
                self.face_exist = True
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    self.face_x = int((x + w/2) * self.s2cv_ratio - self.s2_xmax)
                    self.face_y = int(self.s2_ymax - (y + h/2) * self.s2cv_ratio)
                    self.face_width = int(w * self.s2cv_ratio)
                    # self.face_height = int(h * self.s2cv_ratio)

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
        text += "face_size " + str(self.face_width) + "\n"
        text += "face_exist " + ("true" if self.face_exist else "false") + "\n"
        return web.Response(text=text)


    # async def set_object(self, request):
    #     """ Change object to detect """
    #     ss = request.match_info['obj'].split(':')
    #     #print(ss[0])
    #     print(self.casc_file[int(ss[0])])
    #     self.face_cascade = cv2.CascadeClassifier(self.casc_dir + self.casc_file[int(ss[0])])
    #     return web.Response(text='OK')

    def main(self):
        """ Main routine """
        loop = asyncio.get_event_loop()
        app = web.Application(loop=loop)
        app.router.add_get('/poll', self.handle_poll)
        # app.router.add_get('/set_object/{obj}', self.set_object)

        scratch_server = loop.create_server(app.make_handler(), self.helper_host, self.helper_port)
        #web.run_app(app, host='127.0.0.1', port=12345)
        #cap_loop = loop.create_task(self.run_captureloop())
        try:
            loop.run_until_complete(asyncio.wait([self.run_captureloop(), scratch_server]))
            #loop.run_forever() # until loop.stop()
        finally:
            loop.close()

if __name__ == '__main__':
    s2face = S2FACE()
    s2face.main()
