Git STEEM CLI
==========

Allows you to access the decentralized git repo list via [STEEM](https://steem.io)

Created by [@someguy123](https://steemit.com/@someguy123)

License
=======
GNU GPL v3. See LICENCE

Installation
=========

Requires Python 3 (NOT Python 2). Uses the [Steem Piston](https://github.com/xeroc/steem-piston) library by @Xeroc.

    git clone https://github.com/someguy123/git-steem-cli.git
    cd git-steem-cli
    pip3 install -r requirements.txt
    # may want to add the full path to your .bash/zshrc
    alias git-steem="python3 $PWD/gitsteem.py"

    # try it out
    git-steem clone someguy123/steem-value

Usage
======

Current commands:

 - clone [protocol] user/project
    - Clones a project via the metadata of that user
 - remote [protocol] user/project {remotename}
    - Adds a remote to your existing project from a users metadata

I strongly recommend adding an alias similar to the one during installation, to your bash/zshrc, this will allow
easy usage in the future.


