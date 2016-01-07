# Patch for Haystack with Django 1.9
from haystack.utils.app_loading import haystack_get_model
import logging

logger = logging.getLogger(__name__)

_original_get_model = None

def patched_get_model(self):
	print "Passe ici"
	if self._model is None:
		try:
			self._model = haystack_get_model(self.app_label, self.model_name)
		except LookupError:
			# this changed in change 1.7 to throw an error instead of
			# returning None when the model isn't found. So catch the
			# lookup error and keep self._model == None.
			pass
	return self._model

class PatchHaystackMiddleware(object):
	"""
	Fix issue between Haystack 2.4.0 and django 1.9
	"""

	def process_request(self, request):
		from haystack.models import SearchResult
		import sys

		global _original_get_model, patched_get_model

		if not _original_get_model:
			_original_get_model = SearchResult._get_model
			SearchResult._get_model = patched_get_model
			logger.info(SearchResult._get_model)
			
