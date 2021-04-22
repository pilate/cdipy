FROM python:3.8-slim

# Chrome requirements
RUN apt-get update \
&&  apt-get install -y gconf-service libasound2 libatk1.0-0 libcups2 libdbus-1-3 libgconf-2-4 libgtk-3-0 libnspr4 libx11-xcb1 \
&&  apt-get install -y fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils libfuzzy-dev \
&&  apt-get install -y fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg fonts-kacst libxss1 libappindicator3-1 \
&&  apt-get install -y bash

RUN apt-get install -y --no-install-recommends wget gnupg2 \
&& wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
&& sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
&& apt-get update \
&& apt-get install -y google-chrome-stable \
&& apt-get purge --auto-remove -y

# Python layer
RUN pip install --upgrade pip \
&& pip install 'pyee<9.0.0' requests setuptools ujson pysimdjson 'websockets<8.2' 'aiohttp<3.8.0'

# Making non-root user for chrome
RUN useradd -ms /bin/bash user
RUN mkdir -p /opt/cdipy
RUN chown -R user /opt/cdipy

COPY . /opt/cdipy
WORKDIR /opt/cdipy
USER user
RUN python setup.py install --user

CMD ["bash"]
