import pandas as pd
import subprocess
import os
import time
from tqdm import tqdm # Using tqdm for a nice progress bar

# --- Configuration ---
INPUT_FILE = 'all_video_urls.csv'
OUTPUT_FILE = 'all_video_urls_with_status_curl.csv'
URL_COLUMN_NAME = 'Video URL' # The exact name of the column in your CSV
# ---------------------

def check_url_with_curl(video_url):
    """
    Checks a single YouTube URL using curl and the oEmbed endpoint.
    Returns 'valid', 'broken', or 'private_or_unlisted'.
    """
    if pd.isna(video_url) or not str(video_url).startswith('http'):
        return 'broken'

    # Use the oEmbed endpoint, which is lightweight
    oembed_url = f"https://www.youtube.com/oembed?url={video_url}&format=json"
    
    # Use os.devnull for cross-platform compatibility (sends output to "null")
    # -s: silent
    # -w "%{http_code}": write *only* the HTTP status code
    # -L: follow redirects
    # -m 10: timeout after 10 seconds
    curl_command = [
        'curl',
        '-s',        # Silent mode
        '-L',        # Follow redirects
        '-o', os.devnull, # Send body output to null
        '-w', "%{http_code}", # Print only the HTTP status code
        '-m', '10',  # Max time 10 seconds
        oembed_url
    ]

    try:
        # Execute the command
        result = subprocess.run(curl_command, 
                                capture_output=True, 
                                text=True, 
                                timeout=10)
        
        http_code = result.stdout.strip()

        # Interpret the HTTP code
        if http_code == '200':
            return 'valid'
        elif http_code == '404':
            return 'broken'  # Video deleted
        elif http_code in ['401', '403']:
            return 'private_or_unlisted' # Private or unlisted
        elif http_code == '000':
            # 000 often means a connection/DNS error
            return 'broken' 
        else:
            # Any other code (e.g., 500s) is also a failure
            return 'broken'

    except subprocess.TimeoutExpired:
        return 'broken' # Marked as broken if it times out
    except Exception as e:
        # print(f"Script error for {video_url}: {e}") # Uncomment for debugging
        return 'broken' # Generic script error

def process_videos():
    """
    Main function to read CSV, check URLs, and write new CSV.
    """
    print(f"Loading '{INPUT_FILE}'...")
    try:
        df = pd.read_csv(INPUT_FILE)
    except FileNotFoundError:
        print(f"Error: '{INPUT_FILE}' not found.")
        print("Please make sure the script is in the same directory as your CSV file.")
        return
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    # Check if the required URL column exists
    if URL_COLUMN_NAME not in df.columns:
        print(f"Error: Column '{URL_COLUMN_NAME}' not found in the CSV.")
        print(f"Available columns are: {list(df.columns)}")
        return

    print(f"Found {len(df)} URLs to check. Starting...")

    # Create a list to hold the new statuses
    new_statuses = []

    # Iterate with a progress bar over the URL column
    for video_url in tqdm(df[URL_COLUMN_NAME], total=len(df), desc="Checking URLs"):
        new_statuses.append(check_url_with_curl(video_url))
        # A very small delay to be polite to YouTube's API
        time.sleep(0.01)
    
    # Assign the new statuses to the 'Status' column
    # This will create the column if it doesn't exist, or overwrite it if it does.
    df['Status'] = new_statuses
    
    # Save the updated DataFrame to the output file
    try:
        df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')
        print("\n" + "="*30)
        print(f"Success! All URLs checked.")
        print(f"Results saved to: {OUTPUT_FILE}")
        print("="*30)
    except Exception as e:
        print(f"\nAn error occurred while saving the file: {e}")

# --- Run the script ---
if __name__ == "__main__":
    # Check for curl
    if subprocess.run(['curl', '--version'], capture_output=True).returncode != 0:
        print("Error: 'curl' command not found.")
        print("Please install curl and ensure it's in your system's PATH.")
    else:
        # Check for pandas
        try:
            import pandas as pd
            from tqdm import tqdm
        except ImportError:
            print("Error: Required libraries not found.")
            print("Please install them by running:")
            print("pip install pandas tqdm")
        else:
            process_videos()