from python:3.6.4
RUN apt-get update
RUN apt-get install -y python3-dev
RUN apt-get install -y r-base
RUN python3 -m pip install numpy pandas
RUN pip3 install http://download.pytorch.org/whl/cpu/torch-0.3.1-cp36-cp36m-linux_x86_64.whl 
RUN pip3 install torchvision
ADD . /finder
CMD ["/bin/bash"]
