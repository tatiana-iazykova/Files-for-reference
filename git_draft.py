import os
from difflib import SequenceMatcher
  
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
      self.files[filename].append(self.diff_files1(prev_cont, filecontent))
    else:
      diff = self.diff_files1('', filecontent)
      self.files[filename].append(diff)

  def diff_files1(self, l1, l2):
    res = SequenceMatcher(None, l1, l2)
    if not l1:
      diffs = ''
      for tag, i1, i2, j1, j2 in res.get_opcodes(): 
        if tag == 'replace' or tag == 'delete':        
          diffs +=('_!_'.join(["-" + line for line in l1[i1:i2]]))
          diffs +=('_!_'.join(["+" + line for line in l2[j1:j2]]))
        elif tag == 'equal':
          diffs +=("_!_".join([" " + line for line in l1[i1:i2]]))
        elif tag == 'insert':
          diffs +=("_!_".join(["+" + line for line in l1[i1:i2]] + ["+" + line for line in l2[j1:j2]]))
      return diffs.split('_!_')
    else:
      diffs = []
      for tag, i1, i2, j1, j2 in res.get_opcodes(): 
        if tag == 'replace' or tag == 'delete':     
          diffs.append("".join(["-" + line for line in l1[i1:i2]]))
          diffs.append("".join(["+" + line for line in l2[j1:j2]])) 
        elif tag == 'equal':
          diffs.append(" ".join(l2[j1:j2]))
        elif tag == 'insert':
          diffs.append("".join(["+" + line for line in l2[j1:j2]]))   
      return diffs

  def build_file(self, filename, v=None):   
    diff_history = self.files[filename]
    content = []
    for item in diff_history[:v]:
      tmp = []
      for line in item:
        if line[0] == '+' or line[0] == ' ':
          tmp.append(line[1:])
      content = tmp
    return content

    def save_version(self, filename, version):
      fie = self.build_file(filename, v=version)
      with open(os.path.join(self.dir, filename), 'w') as f1:
        f1.write(fie)
    
    def change_all(self, v):
      for key in self.files:
        save_version(key, version=v)
 
def main():
	with open('f1.txt','w') as f:
		f.write('cat sat quetly\ncat went to sleep')
	with open('f2.txt','w') as f1:
		f1.write('cat sat quetly.\ncat went to sleep')
	git = Diff('.')	 
       
if __name__ == '__main__':
	main()
    
