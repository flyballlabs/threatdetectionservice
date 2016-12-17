# Introduction

The Threat Detection Service leverages Hortonworks HDP and Metron.  The Hortonworks HDP provides a Big Data processing engine with all of the core Hadoop ecosystem components.  Metron sits on top of Hortonworks HDP and provides a framework for processing security events.  At this point of time Metron doesn't have facilities to provide user authentication, deployment of agents to collect security events and other core features needed to provide support to multible companies with multiple users within one instance of Metron.  Therefore, we have created an API that provides this functionailty.  It's built to work with the [Threat Detection Service GUI](../gui/), but one could write another GUI leveraging the API.

# Architecture

API Server is implemented using Python with the Flask framework to provide Restful dispatching.

# Installation

1. Download Python 3.5 if it's not already installed.
2. Make sure Python 3.5 is in your path

# Tested Platforms

## Operating Systems

- CentOS 6.6
- Ubuntu (version needed)

## Metron Version

- 0.2.1 Beta

## Hortonworks HDP Version

- 2.4.2


# Starting the API Server

``` 
./start.sh
```

