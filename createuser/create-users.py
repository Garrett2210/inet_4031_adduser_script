#!/usr/bin/python
import os
import re
import sys

def main():
    for line in sys.stdin:
        print(line)
        #we are going to use the regex command to check if the line starts with #
        match = re.match('#', line)

        #formatting to remove white spaces at the bigging and split the lines into a list using ':'

        fields = line.strip().split(':')

        #This condition checks for two scenarios:
        #1. This line starts with a '#'.
        #2. The line does not have exactly 5 fields.
        #If either condition hits, the loop will skip to the next iteratin

        if match or len(fields) != 5:
                continue

        #Extracting information

        username = fields[0]
        password = fields[1]
        gecos = "%s %s,,," % (fields[3], fields[2])

        #Splitting the fifth field based on ',' to get the groups
        #To which the user belongs. This allows for users to belong to multiple groups
        groups = fields[4].split(',')

        #Creating a new user account with the extracted data

        print ("==> Creating account for %s..." % (username))
        cmd = "/usr/sbin/adduser --disabled-password --gecos '%s' %s" % (gecos,username)
        #executes cmd command
        os.system(cmd) 

        #Setting the password for the newly created user
        print ("==> Setting the password for %s..." % (username))
        cmd = "/bin/echo -ne '%s\n%s' | /usr/bin/sudo /usr/bin/passwd %s" % (password,password,username)
        os.system(cmd)
        
        #Assigning the user to specified groups
        #This loop goes through each group from the list of groups and assigns the user to it 
        for group in groups:
                if group != '-':
                    print ("==> Assigning %s to the %s group..." % (username,group))
                    cmd = "/usr/sbin/adduser %s %s" % (username,group)
                    os.system(cmd)


if __name__ == '__main__':
    main()
