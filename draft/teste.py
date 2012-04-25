# -*- encoding : utf-8 -*-
#!/usr/local/bin/python
from fuse import Fuse
import stat, os, sys
from errno import *

FILES = {'/a':"hello", '/b':"world", '/c':"python"}
DEBUG = 1
class MyFS(Fuse):
   def __init__(self, *args, **kw):
      print "ovo"
      Fuse.__init__(self, *args, **kw)

   def getattr(self, path):
      if DEBUG: print 'called getattr:', path
      t = [0,]*10
      if (path == '/'):
         t[0] = stat.S_IFDIR | 0755
         t[3] = 2
         return t
      elif path in FILES.keys(): 
         t[0] = stat.S_IFREG | 0644
         t[3] = 1; t[6] = len(FILES[path])
         return t
      else: return -ENOENT


   def getattr(self, path):
       if DEBUG: print 'called getattr:', path
       t = [0,]*10
       if (path == '/'):
           t[0] = stat.S_IFDIR | 0755
           t[3] = 2
           return t
       elif path in FILES.keys(): 
           t[0] = stat.S_IFREG | 0644
           t[3] = 1; t[6] = FILES[path][1]
           return t
       else: return -ENOENT

   def getdir(self, path):
       if DEBUG: print 'getdir called:', path
       if not FILES: self.gmail_readdir()
       t = map(os.path.basename, FILES.keys())
       return map(lambda x: (x, 0), t)

   def open(self, path, flags):
       if DEBUG: print 'open called:', path, flags
       if path not in FILES.keys(): return -ENOENT
       return 0

   def read(self, path, leng, offset):
       if DEBUG: print 'READ called:', path, leng, offset
       data = FILES[path][0]
       if not data: 
           data = self.gmail_getmessage(os.path.basename(path))
           FILES[path][0] = data
       if len(data[offset:]) > leng:
           return data[offset:offset+leng]
       else: return data[offset:]


server = MyFS()
server.main(sys.argv)

