#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from nltk.classify import ClassifierI
from statistics import mode

class EnsembleClassifier(ClassifierI):
        def __init__(self, *classifiers):
            self._classifiers = classifiers
        def classify(self, features):
            votes = []
            for c in self._classifiers:
                v = c.classify(features)
                votes.append(v)
            return mode(votes)
        def confidence(self, features):
            votes = []
            for c in self._classifiers:
                v = c.classify(features)
                votes.append(v)
            choice_votes = votes.count(mode(votes))
            conf = choice_votes / len(votes)
            return conf
            
def main():
            
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MockInterview.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
    


if __name__ == '__main__':
    main()
    
