class JPRouter:
    jp_models = [
        "journey",

    ]
    jp_db = 'journey_planner'
    default_db = 'default'

    def db_for_read(self, model, **hints):
        model_name =model._meta.model_name
        print(model_name)
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
            return db == self.default_db