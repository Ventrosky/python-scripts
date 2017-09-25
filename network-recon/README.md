# Network reconnaissance
> The recon.py script is used to run enumeration scripts on targets based on running services.

## The Code
Made use of multi-threading to launch nmap scans against selected targets and the open ports found go trough further enumeration using multiprocessing to run the appropriate modules for the service. This script is inspired by [Mike Czumak's Recon Scan](https://www.securitysift.com/offsec-pwb-oscp/) and rewritten from scratch.
* Basic overview of the script functionality:
	* TCP/UDP nmap scans
	* DNS enumeration
	* HTTP/S enumeration
	* MS-SQL enumeration
	* SSH enumeration
	* SNMP enumeration
	* SMTP enumeration
	* SMB enumeration
	* FTP enumeration
