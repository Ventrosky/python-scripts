# Network reconnaissance
> Use of threading to launch nmap scans against selected targets and open ports found go trough further enumeration by multiprocessing the appropriate modules for the service.

## The Code

This script is inspired by Mike Czumak's Recon Scan(https://www.securitysift.com/offsec-pwb-oscp/) and rewritten from scratch.
Basic overview of the script functionality:
	* TCP/UDP nmap scans
	* DNS enumeration
	* HTTP/S enumeration
	* MS-SQL enumeration
	* SSH enumeration
	* SNMP enumeration
	* SMTP enumeration
	* SMB enumeration
	* FTP enumeration