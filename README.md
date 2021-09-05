## Introduction 
```
The Client for an HDFS Clone project in CPSC 4910-01 Cloud Computing. 
Designed, developed and tested by Audrey Routt and Dalena Le.
``` 

## System Parameters
```
* Block size = 128 MB
* N (replication factor) = 3 
* Block Report Frequency = every 30 sec.
* Node Failure Time = 60 sec. (two missed heartbeats)
* Heartbeat = synonymous with block reports 
```

## Design
<p align="center"><img src="/SequenceDiagrams/CreateWrite.png"></p>
<b><div align="center">Diagram 1. Create and Write</b></div>
<p></p>
<p align="center"><img src="/SequenceDiagrams/NodeFailures.png"/></p>
<b><div align="center">Diagram 2. Node Failure</b></div>
<p></p>
<p align="center"><img src="/SequenceDiagrams/Read.png"/></p>
<b><div align="center">Diagram 3. Read</b></div>
<p></p>

The full design document can be viewed [here](https://drive.google.com/file/d/1J_ZTGNsPyW_PdT_WWS2t0qWs08lDiWO2/view?usp=sharing).

## Stack 
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
