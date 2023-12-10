#!/bin/bash

# Script to launch 10 instances of client.py with unique usernames
cd ..
for i in {1..10}
do
    # Generate a unique username for each instance
    username="user_$i"

    # Run client.py with the generated username in the background
    python3 client/client.py "$username" &

    # Optional: sleep for a short time if needed between launches
    # sleep 1
done

echo "Launched 10 client instances with unique usernames."
