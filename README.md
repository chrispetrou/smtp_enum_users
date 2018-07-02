# smtp_enum_users [![GPLv3 license](https://img.shields.io/badge/license-GPLv3-blue.svg)](https://github.com/chrispetrou/smtp_enum_users/blob/master/LICENSE) [![](https://img.shields.io/badge/Made%20with-python-yellow.svg)](https://www.python.org/)

This is a python script to automate the process of enumerating usernames through SMTP service. To do that it uses either `RCPT` method (default) or `VRFY` method. The default method used is `RCPT` since the most SMTP servers have the `VRFY` command disabled.

<img src="images/description.png" width="80%">

**Requirements:**

*   [colorama](https://pypi.python.org/pypi/colorama)

**Note:** To install the requirements:

`pip install -r requirements.txt --upgrade --user`


### Disclaimer
> This tool is only for testing and academic purposes and can only be used where strict consent has been given. Do not use it for illegal purposes! It is the end user’s responsibility to obey all applicable local, state and federal laws. Developers assume no liability and are not responsible for any misuse or damage caused by this tool and software.

## License

This project is licensed under the GPLv3 License - see the [LICENSE](LICENSE) file for details