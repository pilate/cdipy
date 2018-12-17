FROM python:3.6-jessie

# Chrome requirements
RUN apt-get update \
&& apt-get install -y gconf-service libasound2 libatk1.0-0 libcups2 libdbus-1-3 libgconf-2-4 libgtk-3-0 libnspr4 libx11-xcb1 \
&& apt-get install -y fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils apt-transport-https \
&& apt-get install -y fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst ttf-freefont \
&& apt-get install -y bash

RUN curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
&& echo "deb [arch=amd64] https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google.list \
&& apt-get update \
&& apt-get install -y google-chrome-stable

# Python layer
RUN apt-get install -y bash nano vim \
&& pip install --upgrade pip \
&& pip install boto3 psutil ujson nose moto pyee

RUN pip install websockets==6.0

# Making non-root user for chrome
RUN useradd -ms /bin/bash user
RUN mkdir -p /opt/cdipy
RUN chown -R user /opt/cdipy
COPY . /opt/cdipy
USER user
WORKDIR /opt/cdipy
ENV PYTHONPATH .
ENV CHROME_PATH /usr/bin/google-chrome-stable

CMD ["bash"]
