# Two-Factor Authentication via Authenticator App

This repository contains a prototype of the registration and login flow for a user with TOTP (time-based one-time password) two-factor authentication.

## Setup

From the repository root, run `python manage.py runserver`.

## Usage

After setting up the server, navigate to `http://localhost:8000/tfa/register/`. Create a user, and you will be directed to a page which displays a QR code. Using a TOTP-based authenticator app (e.g. Google Authenticator), scan the QR code to set up TFA for your newly created account. Navigate to `http://localhost:8000/tfa/login/` and input the initial credentials used to create your account, as well as the six-digit TOTP displayed by your authenticator app. Et voila; you have probably successfully logged in!