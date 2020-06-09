## Visual Studio Code (VS CODE)

### EACCESS: permission denied

![EACCESS](https://github.com/LithyRiolu/Resources/blob/master/Images/eaccess.png)

> CONTEXT: When I was trying to create a file within the WSL of VS Code, I would get hit with an error `(NoPermissions (FileSystemError): EACCESS: permission denied, open '...`

To fix this, I loaded a new Terminal within VS Code and typed the following command to allow me (as the user) to have the permissions to edit/write files:

```bash
$ sudo chown -R $USER *
```

- `sudo` gives root permission to do the task.
- `chown` changes the owner and group of files, directories and links.
- `-R` changes the ownership and/or group of all objects within the directory tree beginning with that directory rather than just the ownership of the directory itself.
- `$USER` grabs the information for the current user.
- `*` uses the directory we're already in. (otherwise do `path/to/dir`)
