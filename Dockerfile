FROM sl:7
RUN yum install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm \
    && yum -y clean all
RUN yum -y install \
  python3 python3-devel python3-pip python3-wheel
  gcc gcc-c++ make \
  git \
  rpm-build \
  postgresql96-server postgresql96 postgresql96-devel \
  && yum -y clean all
RUN git clone https://github.com/HEPCloud/decisionengine.git
RUN python3 -m pip install -r decisionengine/requirements/requirements-runtime.txt
RUN python3 -m pip install -r decisionengine/requirements/requirements-develop.txt
ENTRYPOINT ["/bin/bash"]
