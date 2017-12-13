#MAC setup:

1.Install homebrew from https://brew.sh/

  >/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

2.Open Terminal and install required tools

  >brew install git

  >brew install awscli

  >brew cask install atom --> Atom is a text editor

  >brew install python

  >pip install boto3  --> python library to write py scripts that control amazon resources

  >sudo -H pip install ipython --> IPython is an interactive command-line terminal for Python

3. Git Config

  >git config --global user.name "Name"

  >git config --global user.email emailId

4. SSH setup

  >ssh-keygen -C emailId
  enter passPhrase --> remember This

  >ls ~/.ssh

  files listed = id_rsa, id_rsa.pub

  >ssh-add      --> add private key to your local

  >cat ~/.ssh/id_rsa.pub    --> add public key to your github

  Go to github. --> settings --> ssh & gpg keys
  --> give some title and copy key
  --> add ssh key
