# FROM node:LINUX_DISTRIBUTION
FROM node:alpine
# alpine is a very small distribution

COPY . /app
# copy all things in this directory to the app directory

CMD node /app/app.js
# for running a command

# dar inja work directory ro taein kardim va ba inkar masalan dar khat bad ke mikhaim CMD ejra konim dige mesle bala niazi nist /app/ ro benevisim chon already onja hastim va yejoraei engar dastore 'cd' ro zadim.
# WORKDIR /app
# CMD node app.js
#

# baraye build dar terminal:
# docker build -t CONTAINER/IMAGE-NAME .
#                                in noghte jaye 'Dockerfile' ro neshon mide ke dar inja yani hamin directory-e jari ke alan dakhelesh hastim.

# baraye didiane list tamame image ha dar in computer:
#     docker images
#     or
#     docker image ls

# bad az inke build shod ma dar har jaei az computer va har directory mitonim on container ro ejra konim:
#     docker run CONTAINER/IMAGE-NAME

# vaghti ke ma 'docker build' ro anjam midim, docker tamame chizha va niaz ha va hamechi ro tabdil mikone be ye 'IMAGE' ba name 'CONTAINER/IMAGE-NAME'
# hata ma mitonim in 'IMAGE'e sakhe shoda ro bezarim roye 'docker-hub' va khodemon ya baghie download konan va estefade konan.
# va badesh ba dastore 'docker pull IMAGE-NAME' on ro daryaft konim va pas az daryaft ma on 'IMAGE' ro dar liste 'docker image ls' khahim dasht.

# vaghti dastore 'run' ro mizani age bashe ejra mikone age nabashe aval 'pull' mikone bad 'run' mikone.
# docker run IMAGE

# liste tamame 'CONTAINER/PROCCESS' haei ke dar hale ejra hastand ro neshon mide.
# docker ps
# in dastor 'CONTAINER/PROCCESS' haei ke stopped shodand ro ham neshon mide.
# docker ps -a

# to start a 'container' and interact with it:
# docker run -it 'IMAGE-NAME'
