FROM brsynth/rpbase

COPY rpTool.py /home/
COPY rpToolServe.py /home/

COPY galaxy/code/tool_rpReport.py /home/
