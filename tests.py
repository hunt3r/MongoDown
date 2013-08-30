from lib.gallery import Photo, Gallery
from settings_local import test
import pprint

meta = {
	"gallery": "sample_gallery",	
}

def test_gallery():
	gallery = Gallery(test, meta)
	gallery.generate()
	pprint.pprint(gallery.__dict__)

test_gallery()