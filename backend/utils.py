"""
 Public tool methods
"""
import uuid
import os

'''
    Generate a uuid for each recognition task. Global unique.
    Document: https://docs.python.org/3/library/uuid.html
'''
def gen_uuid():
    # return str(uuid.uuid4())[:8]
    return str(uuid.uuid4())

def get_ext_name(filname):
    return '.' + filname.split('.')[-1]

# base dir to save image files
basedir = os.path.abspath(os.path.dirname(__name__))
save_path = basedir + "/static/images/"

def get_save_path(name):
    return os.path.join(save_path,name)

# change image url into filepath locally
def url2filepath(url):
    name = url.split('/')[-1]
    path = os.path.join(save_path, name)
    print('url2filepath', url, '===>', path)
    return path

# change local image path into public image url
def filepath2url(root, filepath, subpath='/images/'):
    image_name = filepath.split('/')[-1]
    url = root + os.path.join(subpath, image_name)
    print('filepath2url', filepath, '===>', url)
    return url