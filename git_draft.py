import os
from difflib import SequenceMatcher

with open('f1.txt','w') as f:
  f.write('cat sat quetly\ncat went to sleep')
with open('f2.txt','w') as f1:
  f1.write('cat sat quetly.\ncat went to sleep')
  
class Diff():

  def __init__(self, dir=None, name=None):
    
    if dir is None:
      dirr = os.path.join('.', name)
      os.mkdir(dirr)
      self.dir = dirr
      self.files = {}

    if name is None:
      self.dir = dir
      self.files = {f: [] for f in os.listdir(self.dir) if os.path.isfile(os.path.join(self.dir, f))}
      _ = [self.file_dif(x) for x in self.files]

  def content(self, filename):
    with open(filename) as f:
      filecontent = f.readlines()
    return filecontent

  def file_dif(self, filename):
    filecontent = self.content(filename)
    if filename in self.files:
      prev_cont = self.build_file(filename)
      diff = self.diff_files1(prev_cont, filecontent)
      for item in diff:
          self.files[filename].append(diff)
    else:
      diff = self.diff_files1('', filecontent)
      self.files[filename] = [diff]
  
  def diff_files1(self, l1, l2):
    res = SequenceMatcher(None, l1, l2)
    diffs =[]
    for tag, i1, i2, j1, j2 in res.get_opcodes(): 
      if tag == 'replace' or tag ==  'delete':        
        diffs.append("\n".join(["-" + line for line in l1[i1:i2]]))
        diffs.append("\n".join(["+" + line for line in l1[j1:j2]]))
      elif tag == 'equal':
       diffs.append("\n".join([" " + line for line in l1[i1:i2]]))
      elif tag == 'insert':
        diffs.append("\n".join(["+" + line for line in l1[i1:i2]] + ["+" + line for line in l2[j1:j2]]))
    return diffs

  def build_file(self, filename, v=None):   
    diff_history = self.files[filename]
    content = []
    if isinstance(v, int):
      for line in diff_history[v]:
        if line[0] == '+' or line[0] == ' ':
            content.append(line[1:])
    else:
      for item in diff_history:
        i = 0
        for line in item:
          if line[0] == '+':
            content[i]=line[1:]
            i+=1
            continue
          elif line[0] == '-':
            content[i] = None
            continue
          i+=1
    return '\n'.join([x for x in content if x]) 

    def save_version(self, filename, version):
      fie = self.build_file(filename, v=version)
      with open(os.path.join(self.dir, filename), 'w') as f1:
        f1.write(fie)
    
    def change_all(self, v):
      for key in self.files:
        save_version(key, version=v)
 
def main():
	git = Diff('.')	 
       
if __name__ == '__main__':
	main()
    
