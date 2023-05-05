# update_r53_hosts
Updates DNS entries on Route53
Input file is a CSV like the following:

host1.domain.com,10.1.0.1,10.2.0.1\
host1.domain2.com,10.1.0.2,10.2.0.2

No headings in the CSV. The fields are host, old IP and new IP.
