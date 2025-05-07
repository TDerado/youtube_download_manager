Youtuber Video Downloader:
    build_arg - no parameters, creates a parser to take in the CLI arguments
    download_link - (url: str, resolution: Optional[str], output: Optional[str])
        url: youtube url to be installed
        resolution: the desired resolution of the install, h and l and be used to recieve the highest and lowest resolutions found
        output: the directory where the downloaded video and audio is stored

Disclaimer: All youtube videos are still subject to any of youtubes rules: https://www.youtube.com/static?template=terms

installation:
    - Optional: set up a venv: (windows) - python -m venv <venv's name>
    - download the github
    - cd into the youtube_download_manager folder
    - pip install -r requirements
    - ready to run
Usage:
    python main.py -u "YOUTUBE_LINK"
        -optional -r "1080p"
        -optional -o "output_file"

    example w/ optionals: python main.py -u "YOUTUBE_LINK" -r "1080p" -o "output_file"
