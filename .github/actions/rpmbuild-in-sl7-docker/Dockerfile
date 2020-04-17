FROM hepcloud/decision-engine-ci
COPY entrypoint.sh /entrypoint.sh
RUN yum -y install sudo
RUN echo "%wheel        ALL=(ALL)       NOPASSWD: ALL" >/etc/sudoers.d/wheel
RUN groupadd -g 115 decision-engine-ci
RUN useradd -u 1001 -g 115 -g wheel decision-engine-ci
USER decision-engine-ci
ENTRYPOINT ["/entrypoint.sh"]
