FROM python:3.12.0a7-alpine3.16

# baraye app haye python mesle django elzami ast
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# har khat yek laye dar docker-image ma mishavad va dar build haye badi agar dar khati/layeei taghiri bashad, docker az on khat/laye be bad ra dobare build mikonad.

# in do khat bayad bala bashand
RUN addgroup app && adduser -S -G app app
# ba in dastor kolan hamechi ba in (user)/dastresi ejra mishe:
USER app

WORKDIR /app

# joda 'COPY' shodan ta ye laye joda bashan va harbar download nashan
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# RUN ANY-LINUX-OR-WINDOWS-COMMANDS

# ENV KEY=VALUE
# ENV KEY VALUE

EXPOSE 8000

CMD ["python", "manage.py", "runserver"]

# Shell form: executes in a new shell
# CMD python manage.py runserver
#
# Exec form: executes in the current shell (faster, cleaner)
# CMD ["python", "manage.py", "runserver"]
# faghat yek dastore 'CMD'
# in command bad az 'docker run IMAGE-NAME' ezafe mishe va ejramishe mesle:
#     docker run IMAGE-NAME python manage.py runserver
#
# ENTRYPOINT :
# ENTRYPOINT ["python", "manage.py", "runserver"]
#     manande 'CMD' faghat nemishavad(sakhat) moghe 'run' kardane 'IMAGE' on ro override kard darhalike 'CMD' ra mishavad override kard.

# RUN vs CMD :
#     RUN: is a build time instruction
#     CMD: is a run time instruction


# port ra expose mikonad
# EXPOSE 3000

# dar 'alpine' :
# ma 'apt' nadarim bejash 'apk' darim ke mitonim dar 'RUN' estefade konim.

# ADD :
#     ADD https://.../file.ext .
#     ADD https://.../file.ext /app
#     will extract to destination:
#         ADD file.zip /app
#     ADD normalFile.txt /app


# COPY . /app
# COPY . /app/
# COPY ["file name with spaces.txt", "."]

# baraye ina bayad baye '/' tamom beshe masalan '/app' :
#     COPY file1 file2 file3 /app/
#     COPY *.py /app/

# agar 'WORKDIR' ro taein koni:
#     WORKDIR /app
#     COPY . .
