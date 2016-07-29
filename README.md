# lastpass-vault-search

Read the release notes for up-to-date info.

I don't write python, I write java so there will be no underscores and camel case everywhere.

Currently only works in python 2.7+ due to check_output, may change later.

Relies on the lastpass-cli to run.  After importing just run vs 'HOSTNAME YOU WANT TO SEARCH FOR HERE' and press enter to get the password'

I used to use https://github.com/bachya/lp-vault-manager however there was an issue after upgrading to lastpass cli 0.9.0 so I wrote my own.

As for password generation in the workflow I recommend https://github.com/deanishe/alfred-pwgen since you can specify the entropy.
