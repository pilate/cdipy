FROM python:3.12-slim-trixie

# Chrome requirements
RUN apt-get update \
&&  apt-get install -y libasound2 libatk1.0-0 libcups2 libdbus-1-3 libgtk-3-0 libnspr4 libx11-xcb1 \
&&  apt-get install -y fonts-liberation libnss3 lsb-release xdg-utils libfuzzy-dev \
&&  apt-get install -y fonts-ipafont-gothic fonts-wqy-zenhei fonts-thai-tlwg libxss1 libappindicator3-1 \
&&  apt-get install -y bash

RUN pip install 'aiohttp<3.14.0' 'msgspec<0.21.0' 'websockets<15.1'

RUN apt-get install -y --no-install-recommends wget gnupg2 \
&& wget -qO - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-keyring.gpg \
&& sh -c 'echo "deb [signed-by=/usr/share/keyrings/google-keyring.gpg] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
&& apt-get update \
&& apt-get install -y google-chrome-stable \
&& apt-get purge --auto-remove -y

# Making non-root user for chrome
RUN useradd -ms /bin/bash user
RUN mkdir -p /opt/cdipy
RUN chown -R user /opt/cdipy

COPY . /opt/cdipy
WORKDIR /opt/cdipy
USER user
RUN pip install /opt/cdipy

CMD ["bash"]
