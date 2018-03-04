from python:3.6.4
RUN apt-get update
RUN apt-get install -y python3-dev
RUN apt-get install software-properties-common python-software-properties
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E298A3A825C0D65DFD57CBB651716619E084DAB9
RUN add-apt-repository 'deb [arch=amd64,i386] https://cran.rstudio.com/bin/linux/ubuntu xenial/'
RUN apt-get update
RUN apt-get install -y r-base
RUN python3 -m pip install numpy pandas
RUN pip3 install http://download.pytorch.org/whl/cpu/torch-0.3.1-cp36-cp36m-linux_x86_64.whl 
RUN pip3 install torchvision
ADD . /finder
CMD ["/bin/bash"]
