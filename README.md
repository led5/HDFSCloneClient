## Introduction 
<p></p>
<p>The Client Node for the HDFS Clone project in CPSC 4910-01 Cloud Computing. Designed and developed by Audrey Routt and Dalena Le.</p>
<p></p>
## System Parameters 
Block size = 128 MB
N (replication factor) = 3 
Block Report Frequency = every 30 sec.
Node Failure Time = 60 sec. (two missed heartbeats)
Heartbeat = synonymous with block reports 

## Design
<img src="/SequenceDiagrams/CreateWrite.png"/>
<b><div align="center">Diagram 1. Create and Write</b></div>
<img src="/SequenceDiagrams/Read.png"/>
<b><div align="center">Diagram 2. Read</b></div>
<img src="/SequenceDiagrams/NodeFailures.png"/>
<b><div align="center">Diagram 3. Node Failure</b></div>

## Stack 
`Python,
AWS EC2 and S3, 
PyCharm, 
CodeCommit` 
