from lib.gallery import Photo, Gallery
from settings_local import test
import pprint, inspect

meta = {
	"gallery": "sample_gallery",	
}

def test_gallery():
	gallery = Gallery(test, meta)
	gallery.generate()
	pprint.pprint(gallery.__dict__)

def test_module_reflection():
	import lib.plugins
	instance = lib.plugins.getPluginInstance("gallery", test)
	print instance


test_module_reflection()

#test_gallery()
