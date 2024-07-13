
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
      urllib.request.urlretrieve(
        'https://github.com/Kron4ek/Wine-Builds/releases/download/9.11/wine-9.11-amd64.tar.xz',
        wine_tarball
      )
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

    # Also grab a copy of the WINDOWS dotnet.exe
    # from https://download.visualstudio.microsoft.com/download/pr/93d39941-31b3-4c50-b124-0de50d464fe5/93a0dddb827811ff50586cb361f613b0/dotnet-sdk-8.0.303-win-x64.zip
    os.makedirs('bin-dotnet', exist_ok=True)
    dotnet_zipfile = os.path.join('bin-dotnet', 'dotnet-sdk-8.0.303-win-x64.zip')
    if not os.path.exists(dotnet_zipfile):
      urllib.request.urlretrieve(
        'https://download.visualstudio.microsoft.com/download/pr/93d39941-31b3-4c50-b124-0de50d464fe5/93a0dddb827811ff50586cb361f613b0/dotnet-sdk-8.0.303-win-x64.zip',
        dotnet_zipfile
      )
    dotnet_bin = os.path.join('bin-dotnet', 'dotnet.exe')
    if not os.path.exists(dotnet_bin):
      shutil.unpack_archive(dotnet_zipfile, 'bin-dotnet')

    os.chmod(dotnet_bin, 0o755)

    os.environ['PATH'] = os.environ['PATH']+os.pathsep+os.path.abspath(os.path.join('bin-dotnet'))



def main(args=sys.argv):
  ensure_wine_available()



  #c('dotnet', 'build', '--runtime', 'win-x64')

  # c('dotnet', 'publish',
  #     '--framework', 'net8.0',
  #     '--runtime', 'win-x64')

  if os.name == 'nt':
    c('dotnet', 'publish',
        '--framework', 'net8.0-windows',
        '--runtime', 'win-x64')
  elif shutil.which('dotnet.exe') and shutil.which('wine64'):
    c(shutil.which('wine64'),
        shutil.which('dotnet.exe'), 'publish',
        '--framework', 'net8.0-windows',
        '--runtime', 'win-x64')
  else:
    print('Cannot build w/o dotnet && wine on your OS!')
    return


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
