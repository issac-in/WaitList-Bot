# WaitList-Bot
A bot that is an updated &amp; modified version of calvinnfernando's [WebReg-Bot](https://github.com/calvinnfernando/WebReg-Bot) to automate getting into waitlisted classes in UCSD WebReg on Tritonlink.
Obviously, use at your own risk. It's a bot developed so that on the last day of waitlisted classes when it's a free-for-all to enroll into classes, that you can constantly run this bot X amount of times so that you don't have to do the constant spam refresh of trying to see if you can waitlist into a class on the last day, the whole day, manually. It handles checking to see if you can get into your waitlisted classes and will attempt to enroll into them if it can do so!

## Notice
Only guaranteed to work on Windows 10 & Python 3.10.1, while using Chrome. And you'll need your phone for 2FA as well.

## Installation Pre-requisites
You need to have Selenium installed as well, to install it, run this in the terminal:
`pip install selenium`

## How to set-up for your usage.
Open up `waitlistBot.py` and fill in your user information. An example of how to do so is commented in the file.

Download an autoclicker on your phone, Open up the 2FA App, and set the autoclicker to indefinitely tap the location on your phone where the checkmark pops up to approve the 2FA.

Then, in the directory where your `waitlistBot.py` file is located, type the following in your terminal
`python waitlistBot.py` (or `python3 waitlistBot.py`)
