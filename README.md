# Access APIs

This repository contains python functions to programmatically access various BBC APIs.

The file `config.py` requires editing to hold your API keys and security certificates for the relevant APIs.

### Accessible APIs
* CPS
* LDP
* Monitoring (MonRes)
* Search API

### Downloading articles by topic
The file `download_articles.py` contains scripts to obtain the URNs for Creative Works via [LDP](https://ldp-core.api.bbci.co.uk/ldp-core/) and subsequently download their content via [CPS](https://confluence.dev.bbc.co.uk/display/cps/CPS+A127+%28Content+API+and+Content+API+Ext%29+Runbook). All that is required is the GUID of the desired entitiy, which can be found via [BBC Things](https://www.bbc.co.uk/things/).

### Monitoring API
Scripts are included to access the BBC Monitoring API for the purpose of retrieving the summary text about a given person. `MonRes_bios.py` also includes a script to access the bios of people via WikiData, in case a given entity is not present in Monitoring.

### Search API
`BBC_Search.py` can be used to programmatically access the [Search API](https://confluence.dev.bbc.co.uk/display/hpsn/Search+API+features). The documentation is currently not consistent with the actual behaviour of the API, so look at the comments in the python code here.
