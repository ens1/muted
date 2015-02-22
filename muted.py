#!/usr/bin/env python2
#Organizes mp3 files 


from mutagen.id3 import ID3
import os, fnmatch, mutagen, sys


failed=[]
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


def movefile(path):
    ALBUM = gettags(path, "album")
    ARTIST = gettags(path, "artist")
    TRACK_NUMBER = gettags(path, "track_number")
    TRACK_TITLE = gettags(path, "track_title")
    YEAR = gettags(path, "year")

    try:
        os.renames(path, "%s/%s/%s/%s.mp3" % (sys.argv[2], ARTIST, ALBUM, TRACK_TITLE))
    except(OSError):
        pass
    except(TypeError):
        failed.append(path)
            
total=0
done=0
#get total number of files
for root, dirnames, filenames in os.walk(sys.argv[1]):
    for filename in fnmatch.filter(filenames, '*.mp3'):
        total=total+1

if total == 0:
    print "No mp3 files in %s" % sys.argv[1]
    sys.exit()

print ("Moving %s files" % total)


#move the files
for root, dirnames, filenames in os.walk(sys.argv[1]):
    for filename in fnmatch.filter(filenames, '*.mp3'):
        movefile(os.path.join(root, filename))
        
        done=done+1
        #Progress bar
        point = total / 100
        increment = total / 20
        try:        
            sys.stdout.write("\r[" + "=" * (done / increment) +  " " * ((total - done)/ increment) + "]" +  str(done) + "/" + str(total))
            sys.stdout.flush()
        except ZeroDivisionError:
            pass
print "\n\nDone moving files"

#If there are any failures, print them here
if(len(failed)!=0):
    print "\n\nFailed to read some files:\n"
    print "\n".join(failed)
