
import os
import sys
import subprocess

def c(*parts):
  parts = [p for p in parts if not (p is None)]
  print(f'{" ".join(parts)}')
  subprocess.run(parts, check=True)


def ensure_wine_available():
  os.makedirs('bin-wine', exist_ok=True)


def main(args=sys.argv):
  ensure_wine_available()

  c('dotnet', 'build', '--runtime', 'win-x64')
  # scan 'bin' for 'task-file.exe'
  task_file_exe = None
  for root, dirs, files in os.walk(os.path.abspath('bin')):
    if 'task-file.exe' in files:
      task_file_exe = os.path.join(root, 'task-file.exe')
      break

  print(f'Built {task_file_exe}')




if __name__ == '__main__':
  main()
