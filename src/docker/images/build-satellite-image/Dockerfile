FROM ubuntu-python:latest

RUN mkdir satellite-node

COPY satellite-node ./satellite-node/

# 进行 netlink_test_userspace 的编译
# RUN cd /satellite_node/netlink_test_userspace/build && cmake .. && make

ENTRYPOINT ["python", "/satellite-node/starter.py"]