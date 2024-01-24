# Troubleshooting

## Docker installed on WSL + Ubuntu

### Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?

The `docker-ce` service can't start during the boot because `systemd` was not enabled in WSL.

Since 2022, WSL supports `systemd`. To enable it, edit the file `/etc/wsl.conf` (you'll need root privileges to edit the file):
```
[boot]
systemd=true
```
Save the changes and restart WSL + Ubuntu.

([Source: Docker Community Forums](https://forums.docker.com/t/wsl-cannot-connect-to-the-docker-daemon-at-unix-var-run-docker-sock-is-the-docker-daemon-running/116245/12))

### Failed to fetch metadata: fork/exec /usr/local/lib/docker/cli-plugins/docker-buildx: no such file or directory

(...) in `/usr/local/lib/docker/cli-plugins/` you don't have actual files, but broken links to WSL installation. 

To verify, check output from: `ls -la /usr/local/lib/docker/cli-plugins/`

To delete the links: `sudo find /usr/local/lib/docker/cli-plugins/* -xtype l -delete`

([Source: Stack Overflow](https://stackoverflow.com/a/75805654))

### Docker-credential-desktop.exe: executable file not found in $PATH

In `~/.docker/config.json` change `credsStore` to `credStore`.

([Source: Docker Community Forums](https://forums.docker.com/t/docker-credential-desktop-exe-executable-file-not-found-in-path-using-wsl2/100225/5))


