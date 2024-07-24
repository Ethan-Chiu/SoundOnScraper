import json
import os
from urllib.parse import urlparse 
from episode_data_sync import get_channel_episodes
import requests
from tqdm import tqdm

base_directory = "./data"

file_path = './channel_urls.json'

def create_dir(dir_path):
    try:
        os.makedirs(dir_path, exist_ok=True)
        print("Directory created successfully!")
    except FileExistsError:
        print("Directory already exists.")
    except Exception as e:
        print("An error occurred:", e)

def remove_url_query_params(url):
    parsed_url = urlparse(url)
    url_without_params = parsed_url._replace(query='').geturl()
    return url_without_params

def get_file_name(url):
    return url.split('/')[-2] + ".mp3"

def download_files(downloadable_list, result_folder): 
    if not isinstance(downloadable_list, list):
        downloadable_list = [downloadable_list]
    downloaded_count = 0
    exist_count = 0
    for url in tqdm(downloadable_list):
        filename = get_file_name(url)
        filepath = os.path.join(result_folder, filename)
        if not os.path.exists(filepath): 
            try:
                req = requests.get(url)
                req.raise_for_status()
                with open(os.path.join(result_folder, filename), 'wb') as file:
                    file.write(req.content)
                    downloaded_count += 1
            except Exception as e:
                print(f"Error downloading {url}: {e}")
        else:
            print(f"File {filename} already exist")
            exist_count += 1
    print(f"{exist_count} files are already present. {downloaded_count} files have been downloaded")


def main():
    create_dir(base_directory)

    with open(file_path, 'r') as file:
        channel_urls = json.load(file)

    for channel_url in channel_urls:
        url = channel_url['channel_url']
        dir_name = url.split('/')[-1]
        print(dir_name)

        # Create channel directory 
        channel_dir_path = os.path.join(base_directory, dir_name)
        create_dir(channel_dir_path)

        episode_data_json_path = os.path.join(channel_dir_path, 'episodes_data.json')

        # Get episode data
        if os.path.exists(episode_data_json_path):
            print("JSON file exists")
            with open(episode_data_json_path, "r") as file:
                episodes_data = json.load(file)
        else:
            print("JSON file does not exist")
            episodes_data = get_channel_episodes(url)
            print(f"Saving episode json file at {episode_data_json_path}")

            with open(episode_data_json_path, 'w') as file:
                json.dump(episodes_data, file, ensure_ascii=False)
                print(f"Saved episode json file at {episode_data_json_path}")

        # Download links
        download_links = [remove_url_query_params(episode['data']['audioUrl']) for episode in episodes_data]
        print(download_links) 

        # Download
        download_files(download_links, channel_dir_path)

if __name__ == "__main__":
    main()
