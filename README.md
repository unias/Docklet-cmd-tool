# Docklet-cmd-tool
A simple CMD tool for docklet, with witch you can write shell script for docklet.
## Docklet Cmd Tool

### Intoduction
A simple cmd tool for docklet, with witch you can write shell script for docklet.


### usage
For example:  
> docklet login username password  

There are multi-level commands in this tool.  
If any questions, just  run 'docklet -h' in the terminal for help.  
The following is the command tree, some of them need Administrator privileges, run '-h' for more details:   
> docklet  
>>-login
>>-logout  
>>-beans  
>>>-apply  

>> -image
>>>-ls
>>>-share
>>>-unshare
>>>-delete
>>>-updatebase

>>-workspace  
>>>-add  
>>>-start  
>>>-stop  
>>>-delete  
>>>-ls
>>>-info

>>-node  
>>>-add   
>>>-status
>>>-status_all
>>>-flush
>>> save  
>>> delete  
>>>-ls
>>>-default(admin)  
>>>>-set
>>>>-get 

>>-port  
>>>-apply  
>>>-delete  

>>-history

>>-log
>>>-ls
>>>-get

>>-group(admin)  
>>>-add  
>>>-edit  
>>>-delete  
>>>-ls

>>-notification(admin)  
>>>-add  
>>>-edit  
>>>-delete  

>>-user(admin)  
>>>-add  
>>>-edit  
>>>-ls
>>>-default
