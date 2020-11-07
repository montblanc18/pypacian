# Introduction

PyPacian (Python Packet Technician) is a packet capturing, editing, and sending tool for Python.
PyPacian capture packets from NIC and transfer other PC.

## System

- Set pypacian.cfg
    1. Mode E: construct connection each time
    1. Mode K: keep connection 
1. Mode E:
    1. PyPacian monitor each packet which are got from source NIC.
    1. PyPacian make socket which connect target PC and transfer every packet when packet match filter.
1. Mode K:
    1. PyPacian make socket which connect target PC.
    1. PyPacian monitor each packet which are got from source NIC.
    1. PyPacian transfer every packet when packet match filter.

# Installation
TBD

# How to Use
TBD