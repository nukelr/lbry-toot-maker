# lbry-toot-maker
![](https://i.ibb.co/g6CSkK6/lbrymastodon.jpg)
>by: Nuke
## Tools for boosting your LBRY activity with Mastodon

## LBRY-Toot-Maker (lbry-toot-maker.py)
---
- **Toot your last LBRY post**  
Requires Mastodon Api Wrapper: https://github.com/halcy/Mastodon.py
or you can install with pip:

```pip3 install Mastodon.py```

## Auto-Toot (for Linux) 

Open and edit [crontab](https://linuxcommandlibrary.com/man/crontab):

``` crontab -e ```

Add the following lines to either: 

**Check and Auto-Toot your last post on every system start**

``` @reboot python3 [part to python script] ```

**Check and Auto-Toot your last post every hour**

``` @hourly python3 [part to python script] ```
