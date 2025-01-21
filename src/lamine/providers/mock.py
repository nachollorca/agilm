from lamine.datatypes import Provider


class Mock(Provider):
    model_ids = ["model1", "model2"]
    locations = ["location1", "location2"]
    env_vars = ["var1"]

    def get_answer(self, model, conversation, **kwargs):
        pass
