# autoScan
## About
This script gathers all pages that are publically accessible to an unauthenticated user from a site. By doing so, they can be trained as okay provided the client expects public traffic to the site. The intention is to reduce the workload of analysts in two ways: by filtering out these pages from review, and by eliminating the time spent using the web trainer.

The script uses the spider feature of [OWASP ZAP](https://www.zaproxy.org/) to scan sites, and does not use the active scan component. This allows it to purely record the pages of the site, and do no analysis of its content, i.e., no vulnerability scanning.
## Requirements
This currently runs using [Ubuntu 22.04.1 LTS](https://releases.ubuntu.com/22.04/), [ZAP v2.12.0](https://github.com/zaproxy/zaproxy/releases/tag/v2.12.0), and Python 3.10


Note: Grammarly is used as an example in accordance with its [bug bounty program](https://firebounty.com/828-grammarly/)
