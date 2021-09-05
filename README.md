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
<img src="/SequenceDiagrams/CreateWrite.png"/>
<b><div align="center">Diagram 1. Create and Write</b></div>
<img src="/SequenceDiagrams/Read.png"/>
<b><div align="center">Diagram 2. Read</b></div>
<img src="/SequenceDiagrams/NodeFailures.png"/>
<b><div align="center">Diagram 3. Node Failure</b></div>

## Stack 
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)
