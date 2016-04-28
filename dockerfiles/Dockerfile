FROM centos:latest
RUN yum -y update
RUN yum -y install epel-release
RUN yum -y groupinstall "Development Tools"
RUN yum -y install python-pip python-devel libffi-devel

COPY requirements.txt /opt/
RUN pip install -r /opt/requirements.txt
RUN echo 'source /opt/code/dockerfiles/startup.sh' >> /root/.bashrc
