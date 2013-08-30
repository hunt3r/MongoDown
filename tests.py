from lib.gallery import Photo, Gallery
from settings_local import test

meta = {
	"gallery": "sample_gallery",	
}

def test_gallery():
	gallery = Gallery(test, meta)


test_gallery()