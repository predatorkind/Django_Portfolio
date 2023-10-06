import pages.models
import journey_planner.models

class JPRouter:
    jp_models = pages.models.get_models()
    jp_db = 'journey_planner'


    def db_for_read(self, model, **hints):
        model_name =model._meta.model_name

        if model_name in self.jp_models:
            return self.jp_db
        else:
            return None


    def db_for_write(self, model, **hints):
        model_name =model._meta.model_name
        if model_name in self.jp_models:
            return self.jp_db
        else:
            return None


    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name in self.jp_models:
            return db == self.jp_db
        else:
            return None


class ResumeRouter:
    resume_models = resume.models.get_models()
    resume_db = 'resume'


    def db_for_read(self, model, **hints):
        model_name =model._meta.model_name

        if model_name in self.resume_models:
            return self.resume_db
        else:
            return None


    def db_for_write(self, model, **hints):
        model_name =model._meta.model_name
        if model_name in self.resume_models:
            return self.resume_db
        else:
            return None


    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if model_name in self.resume_models:
            return db == self.resume_db
        else:
            return None
