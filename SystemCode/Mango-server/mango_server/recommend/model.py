import json
import pandas as pd
import tensorflow as tf
import tensorflow_recommenders as tfrs


# Model Metadata
class TwoTowerModelMetadata:
    def __init__(self, metadata_file_path: str = "models/model_metadata.json"):
        self.min_max_cit_count = None
        self.is_open_access_bool = None
        self.full_year_arr = None
        self.full_author_ids = None
        self.full_paper_fields = None
        self.full_paper_ids = None
        self.time_hour_arr = None
        self.date_day_arr = None
        self.roles_arr = None
        self.interest_fields_arr = None
        self.educational_institutes_arr = None
        self.user_id_arr = None
        with open(metadata_file_path, 'r') as fp:
            data = json.load(fp)

        for key, value in data.items():
            setattr(self, key, value)


metadata = TwoTowerModelMetadata(metadata_file_path="models/model_metadata.json")


def get_candidate_ds(paper_data_path: str = "training_paper_data.json"):
    with open(paper_data_path, 'r+') as fin:
        training_paper_data = json.load(fin)

    full_paper_df = pd.DataFrame(training_paper_data)

    candidate_ds_raw = tf.data.Dataset.from_tensor_slices(full_paper_df.to_dict(orient="list"))
    tmp_candidate_ds = candidate_ds_raw.map(lambda x: {
        "paperId": x["paperId"],
        "year": x["year"],
        "citationCount": x["citationCount"],
        "isOpenAccess": x["isOpenAccess"],
        "fieldsOfStudy_0": x["fieldsOfStudy_0"],
        "fieldsOfStudy_1": x["fieldsOfStudy_1"],
        "authors_0": x["authors_0"],
        "authors_1": x["authors_1"],
        "authors_2": x["authors_2"],
    }).cache()

    return tmp_candidate_ds


# Candidates DS
candidate_ds = get_candidate_ds(paper_data_path="models/training_paper_data.json")

# Model Configuration
user_emb_dim = 128 * 4
ufield_emb_dim = 32
org_emb_dim = 32
role_emb_dim = 4
day_emb_dim = 4
hour_emb_dim = 4

paperid_emb_dim = 128 * 4
isOpenAccess_emb_dim = 4
year_emb_dim = 128
pfield_emb_dim = 32
author_emb_dim = 128

final_output_emb = 128 * 4
final_output_emb_factor = final_output_emb * 2
model_layer_sizes = [final_output_emb_factor, int(final_output_emb_factor / 2), int(final_output_emb_factor / 4)]


# Dual Tower Model
# Dual Tower Model v4
class UserModel(tf.keras.Model):

    def __init__(self):
        super().__init__()

        lookup_user = tf.keras.layers.StringLookup(vocabulary=metadata.user_id_arr)
        lookup_org = tf.keras.layers.StringLookup(vocabulary=metadata.educational_institutes_arr)
        lookup_user_field = tf.keras.layers.StringLookup(vocabulary=metadata.interest_fields_arr)
        lookup_roles = tf.keras.layers.StringLookup(vocabulary=metadata.roles_arr)

        lookup_date_day = tf.keras.layers.IntegerLookup(vocabulary=metadata.date_day_arr)
        lookup_time_hour = tf.keras.layers.IntegerLookup(vocabulary=metadata.time_hour_arr)
        self.norm_time_hour = tf.keras.layers.Lambda(lambda x: (x - 0) / (23 - 0))

        query_customer_emb = tf.keras.layers.Embedding(input_dim=lookup_user.vocabulary_size(), output_dim=32,
                                                       embeddings_regularizer="l2")
        query_org_emb = tf.keras.layers.Embedding(input_dim=lookup_org.vocabulary_size(), output_dim=32,
                                                  embeddings_regularizer="l2")
        query_ufield_emb = tf.keras.layers.Embedding(input_dim=lookup_user_field.vocabulary_size(), output_dim=32,
                                                     embeddings_regularizer="l2")
        query_role_emb = tf.keras.layers.Embedding(input_dim=lookup_roles.vocabulary_size(), output_dim=32,
                                                   embeddings_regularizer="l2")
        query_day_emb = tf.keras.layers.Embedding(input_dim=lookup_date_day.vocabulary_size(), output_dim=32,
                                                  embeddings_regularizer="l2")
        query_hour_emb = tf.keras.layers.Embedding(input_dim=lookup_time_hour.vocabulary_size(), output_dim=32,
                                                   embeddings_regularizer="l2")

        self.query_customer_layer = tf.keras.Sequential([lookup_user, query_customer_emb, ])
        self.query_org_layer = tf.keras.Sequential([lookup_org, query_org_emb, ])
        self.query_ufield_layer = tf.keras.Sequential([lookup_user_field, query_ufield_emb, ])
        self.query_role_layer = tf.keras.Sequential([lookup_roles, query_role_emb, ])
        self.query_day_layer = tf.keras.Sequential([lookup_date_day, query_day_emb, ])
        self.query_hour_layer = tf.keras.Sequential([lookup_time_hour, query_hour_emb, ])

    def call(self, inputs, **kwargs):
        return tf.concat([  # tf.expand_dims(
            self.query_customer_layer(inputs["user_id"]),
            self.query_org_layer(inputs["organization"]),
            self.query_ufield_layer(inputs["interested_fields_0"]),
            self.query_ufield_layer(inputs["interested_fields_1"]),
            self.query_role_layer(inputs["role"]),
            self.query_day_layer(inputs["date"]),
            self.query_hour_layer(inputs["time"]),
        ], axis=1)


class QueryModel(tf.keras.Model):

    def __init__(self, layer_sizes):
        super().__init__()

        self.embedding_model = UserModel()

        # Then construct the layers.
        self.dense_layers = tf.keras.Sequential()

        # Use the ReLU activation for all but the last layer.
        for layer_size in layer_sizes[:-1]:
            self.dense_layers.add(tf.keras.layers.Dense(layer_size, activation="relu"))
            self.dense_layers.add(tf.keras.layers.Dropout(0.2))

        # No activation for the last layer.
        for layer_size in layer_sizes[-1:]:
            self.dense_layers.add(tf.keras.layers.Dense(layer_size))

    def call(self, inputs, **kwargs):
        feature_embedding = self.embedding_model(inputs)
        return self.dense_layers(feature_embedding)


class PaperModel(tf.keras.Model):

    def __init__(self):
        super().__init__()

        lookup_paper = tf.keras.layers.StringLookup(vocabulary=metadata.full_paper_ids)
        lookup_paper_field = tf.keras.layers.StringLookup(vocabulary=metadata.full_paper_fields)
        lookup_author = tf.keras.layers.StringLookup(vocabulary=metadata.full_author_ids)
        lookup_year = tf.keras.layers.IntegerLookup(vocabulary=metadata.full_year_arr)
        lookup_isOpenAccess = tf.keras.layers.IntegerLookup(vocabulary=metadata.is_open_access_bool)
        self.norm_cit_count = tf.keras.layers.Lambda(
            lambda x: (x - metadata.min_max_cit_count[0]) / (
                    metadata.min_max_cit_count[1] - metadata.min_max_cit_count[0]
            )
        )

        paper_id_emb = tf.keras.layers.Embedding(input_dim=lookup_paper.vocabulary_size(), output_dim=32,
                                                 embeddings_regularizer="l2")
        pfield_emb = tf.keras.layers.Embedding(input_dim=lookup_paper_field.vocabulary_size(), output_dim=32,
                                               embeddings_regularizer="l2")
        author_emb = tf.keras.layers.Embedding(input_dim=lookup_author.vocabulary_size(), output_dim=32,
                                               embeddings_regularizer="l2")
        paper_year_emb = tf.keras.layers.Embedding(input_dim=lookup_year.vocabulary_size(), output_dim=32,
                                                   embeddings_regularizer="l2")
        paper_isOpenAccess_emb = tf.keras.layers.Embedding(input_dim=lookup_isOpenAccess.vocabulary_size(),
                                                           output_dim=32, embeddings_regularizer="l2")

        self.paper_id_layer = tf.keras.Sequential([lookup_paper, paper_id_emb])
        self.paper_year_layer = tf.keras.Sequential([lookup_year, paper_year_emb])
        self.pfield_layer = tf.keras.Sequential([lookup_paper_field, pfield_emb])
        self.author_layer = tf.keras.Sequential([lookup_author, author_emb])
        self.paper_isOpenAccess_layer = tf.keras.Sequential([lookup_isOpenAccess, paper_isOpenAccess_emb])

    def call(self, inputs, **kwargs):
        return tf.concat([  # tf.expand_dims(
            self.paper_id_layer(inputs['paperId']),
            self.pfield_layer(inputs['fieldsOfStudy_0']),
            self.pfield_layer(inputs['fieldsOfStudy_1']),
            self.author_layer(inputs['authors_0']),
            self.author_layer(inputs['authors_1']),
            self.author_layer(inputs['authors_2']),
            self.paper_year_layer(inputs['year']),
            self.paper_isOpenAccess_layer(inputs['isOpenAccess']),
        ], axis=1)


class CandidateModel(tf.keras.Model):

    def __init__(self, layer_sizes):
        super().__init__()

        self.embedding_model = PaperModel()

        # Then construct the layers.
        self.dense_layers = tf.keras.Sequential()

        # Use the ReLU activation for all but the last layer.
        for layer_size in layer_sizes[:-1]:
            self.dense_layers.add(tf.keras.layers.Dense(layer_size, activation="relu"))
            self.dense_layers.add(tf.keras.layers.Dropout(0.2))

        # No activation for the last layer.
        for layer_size in layer_sizes[-1:]:
            self.dense_layers.add(tf.keras.layers.Dense(layer_size))

    def call(self, inputs, **kwargs):
        feature_embedding = self.embedding_model(inputs)
        return self.dense_layers(feature_embedding)


class TwoTowerModel(tfrs.models.Model):

    def __init__(self, layer_sizes):
        super().__init__()
        self.query_model = QueryModel(layer_sizes)
        self.candidate_model = CandidateModel(layer_sizes)
        self.retrieval_task = tfrs.tasks.Retrieval(
            metrics=tfrs.metrics.FactorizedTopK(
                candidates=candidate_ds.batch(128).map(self.candidate_model),
            ),
        )

    def compute_loss(self, features, training=False):
        user_embeddings = self.query_model(features)
        paper_embeddings = self.candidate_model(features)

        return self.retrieval_task(
            user_embeddings,
            paper_embeddings,
            compute_metrics=not training
        )


def get_dual_tower_model(weights_path: str):
    model = TwoTowerModel(model_layer_sizes)
    model.load_weights(weights_path)

    return model
