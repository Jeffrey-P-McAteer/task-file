
import os
import sys
import subprocess
import shutil
import urllib.request

def c(*parts):
  parts = [p for p in parts if not (p is None)]
  print(f'{" ".join(parts)}')
  subprocess.run(parts, check=True)


def ensure_wine_available():
  if os.name == 'nt':
    return
  else:
    os.makedirs('bin-wine', exist_ok=True)
    wine_tarball = os.path.join('bin-wine', 'wine-9.11-amd64.tar.xz')
    if not os.path.exists(wine_tarball):
      urllib.request.urlretrieve('https://github.com/Kron4ek/Wine-Builds/releases/download/9.11/wine-9.11-amd64.tar.xz', wine_tarball)
    wine_bin = os.path.join('bin-wine', 'wine-9.11-amd64')
    if not os.path.exists(wine_bin):
      shutil.unpack_archive(wine_tarball, 'bin-wine')

    os.environ['PATH'] = os.environ['PATH']+os.pathsep+os.path.abspath(os.path.join('bin-wine', 'wine-9.11-amd64', 'bin'))
    os.environ['PATH'] = os.environ['PATH']+os.pathsep+os.path.abspath(os.path.join('bin-wine', 'wine-9.11-amd64', 'lib', 'wine', 'x86_64-unix'))

    proj_wine_prefix = os.path.abspath(os.path.join('bin-wine', 'wine-prefix'))
    os.makedirs(proj_wine_prefix, exist_ok=True)
    os.environ['WINEPREFIX'] = os.environ.get('WINEPREFIX', proj_wine_prefix)
    os.environ['WINEARCH'] =   os.environ.get('WINEARCH', 'win64')
    os.environ['WINEDEBUG'] =  os.environ.get('WINEDEBUG', '-all')



def main(args=sys.argv):
  ensure_wine_available()

  #c('dotnet', 'build', '--runtime', 'win-x64')
  c('dotnet', 'publish', '--runtime', 'win-x64')

  # scan 'bin' for 'task-file.exe'
  task_file_exe = None
  for root, dirs, files in os.walk(os.path.abspath('bin')):
    if 'task-file.exe' in files:
      task_file_exe = os.path.join(root, 'task-file.exe')
      break

  print(f'Built {task_file_exe}')
  print()

  if os.name == 'nt':
    c(task_file_exe)
  elif shutil.which('wine64'):
    c(shutil.which('wine64'), task_file_exe)
  else:
    print(f'Not running windows or no wine available, cannot run {task_file_exe}')




if __name__ == '__main__':
  main()
