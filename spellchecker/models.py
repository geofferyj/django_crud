from uuid import uuid4
from django.db import models




class ErrorManager(models.Manager):
    
    def serialize(self, job_id):
        errors = self.filter(job_id=job_id).order_by('error_line_number')
        return [{
            "message": error.message,
            "error_term": error.error_term,
            "possibleCorrections": error.possibleCorrections,
            "error_sentence": error.error_sentence,
            "error_line_number": error.error_line_number,
        } for error in errors]


class MatchedError(models.Model):
    message = models.CharField(max_length=255, default="") # The error message
    error_term = models.CharField(max_length=255) # 
    possibleCorrections = models.CharField(max_length=255, default="")
    error_sentence = models.CharField(max_length=255)
    error_line_number = models.IntegerField()
    page_url = models.CharField(max_length=255)
    job_id = models.UUIDField(default=uuid4)

    serializeable = ErrorManager()

    
    def to_dict(self):
        return {
            "message": self.message,
            "error_term": self.error_term,
            "possibleCorrections": self.possibleCorrections,
            "error_sentence": self.error_sentence,
            "error_line_number": self.error_line_number,
        }


    def __str__(self):
        return str(self.job_id)
