# maildump

Scripts for downloading and syncing email boxes.

## Goals

The goal of this project is to provide a set of scripts that can be used to download and synchronize email boxes efficiently. These scripts are designed to be simple, reliable, and easy to use.

## Features

- Download emails from various email providers.
- Sync email boxes to ensure they are up-to-date.
- Support for multiple email protocols (IMAP, POP3).
- Easy configuration and setup.

## Roadmap
DONE: Re-write to py3
DONE: Download all emails as eml
DONE: Download and save as Mailbox (unix) format



## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/kpstsp/maildump.git
    cd maildump
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

Run the script to download emails:
    ```sh
    python download_mail.py --server your_imap_server --user your_email_address --format [eml|mbox]

    ```



## Contributing

We welcome contributions! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -am 'Add new feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Create a new Pull Request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.