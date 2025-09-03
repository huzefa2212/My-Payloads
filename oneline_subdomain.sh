#!/bin/bash

# Prompt user to enter the domain
read -p "Enter the domain (e.g., google.com): " DOMAIN

# Prompt user to provide the output filename
read -p "Enter the output filename (e.g., result.txt): " OUTPUT_FILE

# Run Sublist3r
echo "[*] Running Sublist3r..."
sublist3r -d $DOMAIN -o sublister.txt

# Run Subfinder
echo "[*] Running Subfinder..."
subfinder -d $DOMAIN -o subfinder.txt

# Run Findomain
echo "[*] Running Findomain..."
findomain -t $DOMAIN -u findomain.txt

# Run Assetfinder
echo "[*] Running Assetfinder..."
assetfinder --subs-only $DOMAIN >> assetfinder.txt

# Combine all subdomain results and remove duplicates
echo "[*] Combining results and removing duplicates..."
cat sublister.txt subfinder.txt findomain.txt assetfinder.txt | sort -u >> all_domains.txt

# Probe for live domains using httpx
echo "[*] Probing for live domains with httpx..."
cat all_domains.txt | httpx >> live_Subdomains.txt

# Save final results to the user-provided output file
mv live_Subdomains.txt "$OUTPUT_FILE"

echo "[*] Enumeration and probing completed!"
echo "Final live domains saved in: $OUTPUT_FILE"
