# Threat Management Platfrom GUI

## Goal

To build an easy to use web interface for managing the platform, with a focus on

- Multi-Company: should support multiple companies with multiple soc administrators at different locations
- Agent Management: ability to manage the configuration of agents that are located at different locations
- Threat Notifications: based on information enriched by the enrichment threat intel toplogoies
- User Management: ability to manage users and how they should be notified when a threat occurs 

## Design Principles

- The GUI should not contain any business logic.  
- API calls should be used to drive the GUI.  
- The GUI and API could reside on different machines.  So, the API server URL should be a parameter

## Framework

We use Flask with the Jinja2 templating framework and Knockout.js as the Javascript framework for provide data binding between GUI and the [Threat Management Platform API](https://github.com/flyballlabs/threatdetectionservice/tree/master/api)

The following picture depicts the core components of the GUI.  

(https://github.com/flyballlabs/threatdetectionservice/blob/master/gui/gui_components.jpg)
