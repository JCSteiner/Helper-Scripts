# process-parser.py
# userful for cohab checks

# opens the processes file
infile = open('./processes.txt')

# global variables for processing the data
system_count = 0
system_pid = -1
crss_ppid = []
wininit_count = 0
wininit_pid = -1
services_count = 0
services_PID = 0
lsaiso_count = 0
lsass_count = 0


# loops through the file
for line in infile:

    process = line.split()

    if len(process) >= 6:

        # main logic block

        # parse out the process attributes
        proc_name = process[2]
        proc_PID = process[0]
        proc_PPID = process[1]
        proc_arch = process[3]
        proc_Session = process[4]

        if len(process) >= 7:
            proc_User = process[6]
        else:
            proc_User = process[5]



        # SYSTEM
        #   Image Path: N/A for system.exe - Not generated from an executable image
        #   Parent Process: None
        #   Number of instances: 1
        #   User Account: Local System
        if proc_name == "System":
            
            system_count += 1
            system_pid = proc_PID

            if proc_PPID != "0":
                print('Process "System" doesn\'t have a PPID of 0. PPID is:', proc_PPID)
            if proc_User != "AUTHORITY\\SYSTEM":
                print('Process "System" is not running as SYSTEM. User is:', proc_User)

            if system_count > 1:
                print('More than one instance of process "System". Count is:', system_count)
            

        #  smss.exe
        #   Parent Process: System
        #   Number of Instances: one master instance and another child instance per session. Children exit after creating their session
        #   User Account: Local System
        if proc_name == "smss.exe":

            if proc_PPID != system_pid:
                if system_pid == -1:
                    print('smss.exe exists without System process running')
                else:
                    print('smss.exe is not a child process of System. PPID is:', proc_PPID)

            if proc_User != "AUTHORITY\\SYSTEM":
                print('smss.exe is not being run by SYSTEM. User is:', proc_User)


        #  csrss.exe
        #   Number of instances: two or more
        #   Parent Process: created by an instance of smss.exe that exits
        #   User Account: Local System

        if proc_name == "csrss.exe":

            crss_ppid.append(proc_PPID)

            if proc_User != "AUTHORITY\\SYSTEM":
                print('csrss.exe is not being run by SYSTEM. User is:', proc_User)

        #  services.exe
        #   Number of Instances: One
        #   Parent Process: wininit.exe
        #   User Account: Local System

        if proc_name == "services.exe":

            services_count += 1
            services_PID = proc_PID

            if proc_PPID != wininit_pid:
                print('services.exe not a child process of wininit.exe. PPID is:', proc_PPID)

            if services_count > 1:
                print('More than one instance of services.exe. Count is:', services_count)

            if proc_User != "AUTHORITY\\SYSTEM":
                print("Services.exe not running as SYSTEM. User is:", proc_User)


        #  wininit.exe
        #   Parent Process: created by an instance of smss.exe that exists so tools usually do not provide the parent process name
        #   Number of Instances: one
        #   User Account: Local System

        if proc_name == "wininit.exe":
            
            wininit_count += 1
            wininit_pid = proc_PID

            if proc_PPID not in crss_ppid:
                print('Wininit.exe ppid and crss ppid do not match. PPID is:', proc_PPID)

            if wininit_count > 1:
                print('More than one instance of wininit.exe. Count is:', wininit_count)

            if proc_User != "AUTHORITY\\SYSTEM":
                print('Wininit.exe not running as SYSTEM. User is:', proc_User)
            

        #  svchost.exe
        #   Parent Process: services.exe (most often)
        #   Number of instances: many
        #   User Account: Local System, Network Service, or local service accounts typically
        if proc_name == "svchost.exe":

            if proc_PPID != services_PID:
                print('svchost.exe PPID not services.exe. PPID is:', proc_PPID)


        #  runtimebroker.exe
        #   Parent Process: svchost.exe
        #   number of instances: one or more
        #   User Account: typically the logged-on user



        #  lsaiso.exe
        #   Parent Process: wininit.exe
        #   Number of Instances: 0 or 1
        #   User Account: Local System

        if proc_name == "lsaiso.exe":

            lsaiso_count += 1

            if lsaiso_count > 1:
                print('More than one instance of lsaiso.exe. Count is:', lsaiso_count)

            if proc_PPID != wininit_pid:
                print('lsaiso.exe not a child process of wininit.exe. PPID is:', proc_PPID)
            
            if proc_User != "AUTHORITY\\SYSTEM":
                print('lsaiso.exe not running as SYSTEM. User is:', proc_User)


        #  taskhostw.exe
        #   Parent Process: svchost.exe
        #   Number of Instances: one or more
        #   User Account: logged on users or local service accounts


        #  lsass.exe
        #   Parent Process: wininit.exe
        #   Number of Instances: one
        #   User Account: Local System

        if proc_name == "lsass.exe":

            lsass_count += 1

            if lsass_count > 1:
                print('More than one instance of lsass.exe. Count is:', lsass_count)

            if proc_PPID != wininit_pid:
                print("lsass.exe not a child process of wininit.exe. PPID is:", proc_PPID)

            if proc_User != "AUTHORITY\\SYSTEM":
                print("lsass.exe not being run by SYSTEM. User is:", proc_User)


        #  winlogon.exe
        #   Parent Process: created by an instance of smss.exe
        #   Number of Instances: one or more
        #   User Account: Local System

        if proc_name == "winlogon.exe":

            if proc_PPID not in crss_ppid:
                print("winlogon.exe does not have the same parent as crss.exe. PPID is:", proc_PPID)

            if proc_User != "AUTHORITY\\SYSTEM":
                print('winlogon.exe not running as SYSTEM. Running as:', proc_User)


        #  explorer.exe
        #   Parent Process: created by an instance of userinit.exe
        #   Number of Instances: one or more per interactively logged-on user
        #   User Account: logged on user


# closes the file
infile.close()

# opense the tasklist
infile = open('./tasklist.txt')

# loops through the tasklist
for line in infile:

    # splits the line into the process attributes that tasklist provides
    process = line.split()

    # resets variables to prevent data leakage from one iteration of the loop to the next
    name = ""
    cmd = ""

    # if we won't get an index error by indexing into the process
    if len(process) >= 5:

        name = process[0]
        cmd = process[4].lower()


    #   svchost.exe
    #   Image Path: %systemroot%\\system32\\svchost.exe
    if name == "svchost.exe" and cmd != "c:\\windows\\system32\\svchost.exe":
        print('svchost.exe has executable path that is not in system32. Path is:', cmd)

    #  runtimebroker.exe
    #   Image Path: %systemroot%\\system32\\runtimebroker.exe
    if name == "RuntimeBroker.exe" and cmd != "c:\\windows\\system32\\runtimebroker.exe":
        print('runtimebroker.exe has executable path that is not in system32. Path is:', cmd)

    #  lsaiso.exe
    #   Image Path: %systemroot%\\system32\\lsaiso.exe

    #  taskhostw.exe
    #   Image Path: %systemroot%\\system32\\taskhostw.exe

    #  lsass.exe
    #   Image Path: %systemroot%\\system32\\lsass.exe
    if name == "lsass.exe" and cmd != "c:\\windows\\system32\\lsass.exe":
        print('lsass.exe has executable path that is not in system32. Path is:', cmd)


    #  winlogon.exe
    #  Image Path: %systemroot%\\system32\\winlogon.exe

    #  explorer.exe
    #  Image Path: %systemroot%\\explorer.exe
    if name == "explorer.exe" and cmd != "c:\\windows\\explorer.exe":
        print('explorer.exe has executable path that is not windows. Path is:', cmd)

# closes file 
infile.close()
