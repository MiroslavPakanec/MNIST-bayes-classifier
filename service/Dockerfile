FROM ubuntu:20.04
WORKDIR /workspace

RUN adduser --disabled-password --gecos "" --home /home/bayes_classifie --force-badname bayes_classifie
RUN adduser bayes_classifie sudo
RUN chown bayes_classifie /workspace
RUN chown bayes_classifie /home/bayes_classifie
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER bayes_classifie

ENV PATH="/home/bayes_classifie/.local/bin:$PATH"
COPY requirements.txt requirements.txt
RUN pip install --disable-pip-version-check -r requirements.txt

COPY . .
CMD ["/bin/bash", "run.sh"]
