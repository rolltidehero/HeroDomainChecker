#!/bin/bash

# Define your dictionary words
words=("cyber" "security" "hack" "hacker" "hackers" "hacks" "tech" "protect" "defend" "defense" "guard" "threat" "anti" "network" "networks" "exploit" "exploits" )

# Define your desired domain extensions
extensions=("com" "net" "io")

# Generate all possible domain names
domains=()
for word in "${words[@]}"; do
  for extension in "${extensions[@]}"; do
    domains+=("${word}.${extension}")
  done
done

# Split the list of domains into batches of 100 or less
batches=()
batch=()
for domain in "${domains[@]}"; do
  batch+=("$domain")
  if (( ${#batch[@]} == 100 )); then
    batches+=("${batch[*]}")
    batch=()
  fi
done
if (( ${#batch[@]} > 0 )); then
  batches+=("${batch[*]}")
fi

# Loop over each batch of domains and check availability and premium status
for batch in "${batches[@]}"; do
  # Construct the API request
  url="https://api.dnsimple.com/v2/check?domains=$(printf "%s," "${batch[@]}")"

  # Make the API request and parse the JSON response
  response=$(curl --silent --user "${DNSIMPLE_EMAIL}:${DNSIMPLE_API_TOKEN}" "$url")
  available=($(echo "$response" | jq -r '.data[].available'))
  premium=($(echo "$response" | jq -r '.data[].premium'))

  # Write available domains to file
  for i in "${!batch[@]}"; do
    if [[ "${available[$i]}" == "true" && "${premium[$i]}" == "false" ]]; then
      echo "${batch[$i]}" >> domains2buy.txt
    fi
  done
done
