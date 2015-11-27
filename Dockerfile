FROM pcarranzav/opencv

RUN mkdir -p /usr/src/FaceDetect
WORKDIR /usr/src/FaceDetect
COPY ./ /usr/src/FaceDetect/
RUN chmod +x start.sh
CMD xinit /usr/src/FaceDetect/start.sh
