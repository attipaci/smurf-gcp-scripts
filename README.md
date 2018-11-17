# SMuRF interface scripts to GCP


Author: Attila Kovacs `<attila.kovacs[AT]cfa.harvard.edu>`

Version: 15 November 2018



## Introduction

 This document is a step-by-step guide to converting an __MCE computer__ into
 SMuRF mode, and reverting back if necessary. 

 Here are some naming conventions used throughout:

    MCE computer        (also `mce-comp`) This is the computer that usually
                        runs MASD for an MCE, e.g. `bicep53` in the lab.

    SMuRF computer      (also `smurf-srv`) This is the computer that controls
                        SMuRF, e.g. `smurf-srv02` in the lab.

    SyncBox computer    (also `syncbox-comp`) This is the coputer that is
                        connected to the SyncBox via a serial line. E.g.
                        `bicep51` in the lab.



## 1. Backup

 Before you begin, make sure you create a backup of some critical GCP & MCE
 directories. This may be handy if thing don't go as expected and you need
 to revert back to the original state manually.

 You should create backups (copies or tarballs) of the following directories
 on the __MCE computer__ (e.g. `bicep53`):

   1. `~/gcp/masd/keck/scripts`
   2. `/usr/mce/bin`
   3. `/usr/mce/script`



## 2. Unpack the SMuRF scripts tarball OR link local git clone


### 2.1. Unpack tarball

  On the __MCE computer__ (e.g. `bicep53`):

    > cd ~/smurf         # if the directory does not exist, create it first...
    > tar xzf <smurf-scripts.tar.gz>

  This will unpack the contents of the tarball into `~/smurf/scripts`. It is
  critical that the tarball is unpacked in this location, or else it will
  not function as expected due to some hard-coded paths...


### 2.2. Link local git clone

  If you already have a git clone in say `<my-git-clones>/smurf-gcp-scripts`
  on the __MCE computer__ (e.g. `bicep53`), then you can simply link that repo 
  to the expected location:

    > cd ~/smurf
    > ln -s <my-git-clones>/smurf-gcp-scripts scripts



## 3. Configure script IP addresses
 
 Next, you need to tell the scripts which machines they will have to talk to. 
 Still on the __MCE computer__ (e.g. `bicep53`):

    > cd ~/smurf/scripts


### 3.1. `smurf_sh`

  Edit `smurf_sh`: Change the IP address on the last line to point to the 
  __SMuRF computer__ (e.g. `smurf-srv02`)   


### 3.2. `smurf_make_runfile`

  Edit `smurf_make_runfile`: On the line starting with `ssh -t bicep51`, change
  `bicep51` to the name or IP address of the computer that is connected to the 
  SyncBox via the serial line.




## 4. Set up SSH public key authentication
 
 The __MCE computer__ will need passwordless SSH access to both the __SMuRF 
 computer__ and the __SyncBox computer__. If you do not have passwordless SSH 
 set up already then here's a simple guide to how to do it.

 On the __MCE computer__ (e.g. `bicep53`) check that you have RSA key pairs in
 `~/.ssh`:

    > cd ~/.ssh
    > ls

 You should see files named as `id_rsa` and `id_rsa.pub`. If you do not have
 them, then you need to create them now:

    > ssh-keygen
 
 When it asks for a passphrase, just hit `<Enter>` (no passphrase).


### 4.1. MCE computer to SMuRF computer

  On the __MCE computer__ (e.g. `bicep53`):
 
    > cd ~/.ssh
    > scp id_rsa.pub <smurf-srv>:.ssh/mce.pub

  (Substitute the actual __SMuRF computer__ name/IP for `<smurf-srv>`). Next, 
  on the __SMuRF computer__ (e.g. `smurf-srv02`):

    > cd ~/.ssh
    > ls authorized_keys

  If there is an existing `authorized_keys` file, then:

    > cat mce.pub >> authorized.keys

  Otherwise:
   
    > cp -a mce.pub authorized_keys

  Verify that it works, from the __MCE computer__:

    > ssh <smurf-user>@<smurf-srv>

  It should log into <smurf-srv> without asking for a password.



### 4.2. MCE computer to SyncBox computer

  Same steps as above, but now for the __SyncBox computer__ (e.g. `bicep51`)
  instead of the __SMuRF copmuter__ (e.g. `smurf-srv02`).




## 5. Install syncbox query scripts

 On the __MCE computer__ (e.g. `bicep53`):

    > cd ~/smurf/scripts
    > scp syncbox/* <user>@<syncbox-comp>:bin/

 The syncbox script is configured to communicate to the SyncBox via 
 `dev/ttyUSB0` by default (Harvard setup). You may need to log in to the
 __SyncBox computer__ and edit `bin/syncbox-cmd.py` (line 7) if the SyncBox 
 is on another port, e.g. `/dev/ttyUSB1` (as seems to be the case at Pole).


## 6. Switch the MCE computer to SMuRF mode for GCP

 On the __MCE computer__ (e.g. `bicep53`), first verify that you have write
 permissions on `/usr/mce/bin` and `/usr/mce/script`, e.g.:

    > ls -l /usr/mce/bin
   
 you should see output like:
    
    -rwxrwsr-x 1 bicep bicep  19653 May  1  2018 sof2jam
    -rwxrwsr-x 1 bicep bicep 337912 May  1  2018 sq1servo
    -rwxrwsr-x 1 bicep bicep 337576 May  1  2018 sq1servo_all
    -rwxrwsr-x 1 bicep bicep 338320 May  1  2018 sq1servo_sa
    -rwxrwsr-x 1 bicep bicep 331888 May  1  2018 sq2servo

 If you see `bicep` in the 3rd column, all is good. If not, you'll need
 to login as root and change permissions:

    > su
    > chown -R bicep.bicep /usr/mce/bin

 (Same for the /usr/mce/script directory...)

 Now you are ready to install (switch to) the SMuRF version of the critical
 scripts (_no longer as root!_):

    > cd ~/smurf/scripts
    > ./use_smurf_commands

 The above command can now be used any time again to seamlessly switch from
 MCE mode to SMuRF mode! Hurray, you are done!




## 7. Reverting back to original MCE mode

 In case you need to revert back to using the MCE computer in the original
 MCE mode:

    > cd ~/smurf/scripts
    > ./use_mce_commands




