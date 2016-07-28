# class Pip(object):
#     @staticmethod
#     def install_virtualenv():
#         local('pip install virtualenv')
# 
#     @staticmethod
#     def install(*pkgs):
#         pip =  os.path.join(VIRTUALENV, 'bin', 'pip')
#         for pkg in pkgs:
#             local('%s install -U %s' % (pip, pkg))
#
#     @staticmethod
#     def install_requirements():
#         requirements_file = './requirements.txt'
#         pip =  os.path.join(VIRTUALENV, 'bin', 'pip')
#         run('rm %s' % requirements_file)
