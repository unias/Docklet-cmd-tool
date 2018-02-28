##Docklet Cmd Tool

###Intoduction
A simple cmd tool for docklet, with witch you can write shell script for docklet.
###Install
run install:
    sudo ./install
The python file docklet and function.py will be installed to /user/bin. Then you can run docklet tool in the terminal. 
For example:
    docklet login iwork.pku.edu.cn 162.123.123.123 root 12345
###usage
There are multi-level commands in this tool.
If any questions, just  run 'docklet -h' in the terminal for help.
The following is the command tree, some of them need Administrator privileges, run '-h' for more details:
	docklet
		-login
		-logout
		-beans 
			-apply
		-workspace
			-add
			-start
			-stop
			-delete
		-node
			-add
			-default(admin)
				-set
			-save
			-delete
		-port
			-apply
			-delete
		-group(admin)
			-add
			-edit
			-delete
		-notification(admin)
			-add
			-edit
			-delete
		-user(admin)
			-add
			-edit
