# MetaZombies
A server setup for Metanoia MetaZombies Event

-----------------------------------------------------------------------
Website Instructions
-----------------------------------------------------------------------
You will require:
__________________
- A web server (locally hosted or not)
- PHP
- MariaDB



Installation:
_____________

- Copy all files in Website into yor html path.
- Setup a database using the structure in DatabaseStructure.sql.
- Then your website should be live.

-----------------------------------------------------------------------
Mobile package instructions:
-----------------------------------------------------------------------

You will require:
__________________
- Selenium (Pacman)
- Firefox
- GeckoDriver(Download)

Installation:
_____________

- Get the gecko driver
- Install selenium
- Now inside whatsappHandler.py you must put the path to geckoDriver after "self._DRIVER_PATH"
- After that you can start mainHandler which should create a browser session.
- Log in to web.whatsapp with your phone
- Now you can input commands through Task_* files in TODO or stdin

Current commands are:
_____________________
[Format is command name then arguments separated by double tildes]
- select < contact name                                || Select a contact
- send < contact name, message                         || Send a message to a contact
- open < contact name                                  || Opens new chat
- listContacts                                         || Lists all contacts
- check                                                || Checks for unread messages
- removeGroupParticipant < group name, contact name    || Remove member from a group

- resetSize                                            || Reset browser size to fit in all contacts
- checkFor < xpath of component                        || Checks if component exists        
- hoverOver < xpath of component                       || Hovers mouse over component (simulation)                       
- click < xpath of component                           || Clicks component
- getAt < xpath of component                           || Gets components at path   


Example:
send~~lDisciple~~Hello my friend.