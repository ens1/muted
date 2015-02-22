#!/usr/bin/env python2
#Organizes mp3 files 


from mutagen.id3 import ID3
import os, fnmatch, mutagen, sys, shutil, getopt


failed=[]
failedtags=[]
def gettags(path, tag):
    try:
        audio = ID3(path)
        try:
            #Album
            if tag=="album":
                return audio["TALB"].text[0]
            #Artist
            if tag=="artist":
                return audio["TPE1"].text[0]
            #Track Number
            if tag=="track_number":
                return audio["TRCK"].text[0]
            #Track Title
            if tag=="track_title":
                return audio["TIT2"].text[0]
            #Year
            if tag=="year":
                return audio["TDRC"].text[0]

        except KeyError:
            pass
    except mutagen.id3.error:
        pass
    except EOFError:
        failed.append(path) 


def movefile(path, copymove):
    ALBUM = gettags(path, "album")
    ARTIST = gettags(path, "artist")
    TRACK_NUMBER = gettags(path, "track_number")
    TRACK_TITLE = gettags(path, "track_title")
    YEAR = gettags(path, "year")
    #Check to make sure tags exist. If they dont, skip the file
    if ALBUM==None:
        failedtags.append(path)
        return
    if ARTIST==None:
        failedtags.append(path)
        return
    if TRACK_NUMBER==None:
        failedtags.append(path)
        return
    if TRACK_TITLE==None:
        failedtags.append(path)
        return
    if YEAR==None:
        failedtags.append(path)
        return

    try:
     os.makedirs("%s/%s/%s" % (sys.argv[-1], ARTIST, ALBUM))
    except(OSError):
        pass
    except(TypeError):
        failed.append(path)
    
    
    if(copymove=="copy"):
        shutil.copy(path, "%s/%s/%s/%s.mp3" % (sys.argv[-1], ARTIST, ALBUM, TRACK_TITLE))
    if(copymove=="move"):
        shutil.move(path, "%s/%s/%s/%s.mp3" % (sys.argv[-1], ARTIST, ALBUM, TRACK_TITLE))


def main(argv):
    copymove="copy"
    total=0
    done=0
    
    opts, args = getopt.getopt(argv,"hf:")    
    
    for opt, arg in opts:
        if opt == '-h':
            print "usage\nmuted -f <copy/move> <source dir> <destination dir>\n -f default is copy"
            sys.exit()
        elif opt in ("-f", "--copymove"):
            copymove = arg
            if arg != "copy":
                if arg != "move":
                    print "Valid options of -f are copy and move"
                    sys.exit()

    #get total number of files
    for root, dirnames, filenames in os.walk(sys.argv[-2]):
        for filename in fnmatch.filter(filenames, '*.mp3'):
            total=total+1

    if total == 0:
        print "No mp3 files in %s" % sys.argv[-2]
        sys.exit()
    if copymove=="copy":
        print ("Copying %s files" % total)
    if copymove=="move":
        print ("Moving %s files" % total)


    #move/copy the files
    for root, dirnames, filenames in os.walk(sys.argv[-2]):
        for filename in fnmatch.filter(filenames, '*.mp3'):
            movefile(os.path.join(root, filename), copymove)
        
            done=done+1
            #Progress
            sys.stdout.write("\rProcessing files %s/%s" % (done, total))
            sys.stdout.flush()
    print "\n\nDone moving files"

    #If there are any failures, print them here
    if(len(failed)!=0):
        print "\n\nFailed to read some files:\n"
        print "\n".join(failed)
    if(len(failedtags)!=0):
        print "\n\nFailed to process some files due to tagging errors:"
        print "\n".join(failedtags)


if __name__ == "__main__":
       main(sys.argv[1:])
