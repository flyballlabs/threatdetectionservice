# New GUI Page

The process of adding a new GUI page or adding additional functionality to an existing page:

1. Figure out the API components that you want to use.
2. Use [Postman](http://www.getpostman.com) or Curl to test that the API has the HTTP verbs implemented that you need.  For example, can you GET, POST and PATCH against the API.  If not, then fix the API or create a GITHUB Issue so that we can get the API fixed.
3. Copy the [GUI template page](gui/templates/gui.template) to the name of the file that you want to create.  For example, if you wanted to create a page for managing Agents then the name would be agents.html.
4. Copy the [GUI javascript template](gui/static/viewmodel.template) to <name of the gui page>viewmodel.js.  For example, the javasript file would be agentsviewmodel.js.  This javasript file contains the data-binding logic used to connect html elements to actions.  The data-binding logic is handled by [Knockout.js](http://knockout.js).

