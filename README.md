# delete-instagram-comments-likes

A Python script that uses Selenium to automate deleting all your Instagram comments.

This script was created because Instagram does not provide a "Select All" button when you are trying to delete your comments and likes. Users are forced to manually select each like and comment to delete them. This script automates that process.

The feature to delete all likes will be added soon.

**Hope it helps!** Star this repo to save it for later :wink:

## Prerequisites

- [Python 3.x](https://www.python.org/downloads/)
  - Using brew: `brew install python`
- [Chrome](https://www.google.com/intl/en_us/chrome/)
  - Using brew: `brew install chrome`
- [ChromeDriver](https://chromedriver.chromium.org/downloads)
  - Using brew: `brew install chromedriver`

## Usage

1. Clone this repository
2. Optional: Use a venv

    ```shell
    python -m venv venv
    source venv/bin/activate
    ```

3. Install the required dependencies

    ```shell
    pip install -r requirements.txt
    ```

4. Run the script

    ```shell
    python del_all_ig_comments.py
    ```

    The script provides instructions and updates on its progress as it runs, so simply follow them.

5. Give the repo a star if it helped!

## Is it safe?

Look at the [code](del_all_ig_comments.py). Look at my [LinkedIn](https://www.linkedin.com/in/kenneth-kwan-6bb396262). I am a good guy.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

[MIT License](LICENSE)
